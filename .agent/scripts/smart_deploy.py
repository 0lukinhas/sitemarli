#!/usr/bin/env python3
"""
smart_deploy.py — Deploy inteligente com geração automática de commit message.
Uso: python .agent/scripts/smart_deploy.py [diretório-do-projeto]
Se nenhum diretório for passado, usa o diretório atual.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────
# CORES NO TERMINAL
# ─────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
GRAY   = "\033[90m"

def p(msg): print(msg)
def ok(msg):   print(f"{GREEN}  ✅ {msg}{RESET}")
def warn(msg): print(f"{YELLOW}  ⚠️  {msg}{RESET}")
def err(msg):  print(f"{RED}  ❌ {msg}{RESET}")
def step(msg): print(f"\n{BOLD}{CYAN}▶ {msg}{RESET}")
def line():    print(f"{GRAY}{'─' * 50}{RESET}")


# ─────────────────────────────────────────────
# HELPERS GIT
# ─────────────────────────────────────────────
def run(cmd, cwd=None, capture=True):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=capture, text=True
    )
    return result.stdout.strip(), result.returncode


def is_git_repo(path):
    _, code = run("git rev-parse --is-inside-work-tree", cwd=path)
    return code == 0


def has_remote(path):
    out, _ = run("git remote", cwd=path)
    return bool(out.strip())


def get_changed_files(path):
    """Retorna lista de arquivos alterados (staged + unstaged + untracked)."""
    out, _ = run("git status --porcelain", cwd=path)
    files = []
    for line in out.splitlines():
        if len(line) >= 3:
            status = line[:2].strip()
            fname  = line[3:].strip().split(" -> ")[-1]  # renomear → pegar destino
            files.append((status, fname))
    return files


def get_diff_stats(path):
    """Retorna (+linhas, -linhas) do diff total."""
    out, _ = run("git diff HEAD --shortstat", cwd=path)
    if not out:
        out, _ = run("git diff --cached --shortstat", cwd=path)
    added = deleted = 0
    for part in out.split(","):
        part = part.strip()
        if "insertion" in part:
            added = int(part.split()[0])
        elif "deletion" in part:
            deleted = int(part.split()[0])
    return added, deleted


# ─────────────────────────────────────────────
# GERADOR INTELIGENTE DE COMMIT MESSAGE
# ─────────────────────────────────────────────
CATEGORY_MAP = {
    # Web
    ".html": ("feat", "página HTML"),
    ".css":  ("style", "estilos CSS"),
    ".js":   ("feat", "lógica JavaScript"),
    ".ts":   ("feat", "TypeScript"),
    ".jsx":  ("feat", "componente React"),
    ".tsx":  ("feat", "componente React/TS"),
    ".vue":  ("feat", "componente Vue"),
    ".svelte": ("feat", "componente Svelte"),
    # Config / Infra
    ".json": ("chore", "configuração JSON"),
    ".env":  ("chore", "variáveis de ambiente"),
    ".yml":  ("ci", "configuração YAML"),
    ".yaml": ("ci", "configuração YAML"),
    ".toml": ("chore", "configuração TOML"),
    ".lock": ("chore", "dependências"),
    # Docs
    ".md":   ("docs", "documentação"),
    ".txt":  ("docs", "arquivo de texto"),
    # Imagens e assets
    ".png":  ("assets", "imagem PNG"),
    ".jpg":  ("assets", "imagem JPG"),
    ".jpeg": ("assets", "imagem JPG"),
    ".svg":  ("assets", "ícone SVG"),
    ".webp": ("assets", "imagem WebP"),
    ".gif":  ("assets", "animação GIF"),
    ".ico":  ("assets", "ícone"),
    ".mp4":  ("assets", "vídeo"),
    ".woff": ("assets", "fonte"),
    ".woff2":("assets", "fonte"),
    # Backend
    ".py":   ("feat", "Python"),
    ".php":  ("feat", "PHP"),
    ".rb":   ("feat", "Ruby"),
    ".go":   ("feat", "Go"),
    ".rs":   ("feat", "Rust"),
    ".java": ("feat", "Java"),
    ".sh":   ("chore", "script shell"),
}

STATUS_VERBS = {
    "M":  "atualiz",    # Modified
    "A":  "adicionou",  # Added
    "D":  "removeu",    # Deleted
    "R":  "renomeou",   # Renamed
    "C":  "copiou",     # Copied
    "?":  "adicionou",  # Untracked (new file)
}

def smart_commit_message(files):
    """
    Gera mensagem de commit inteligente baseada nos arquivos alterados.
    """
    if not files:
        return "chore: atualização geral do projeto"

    # Agrupa por categoria
    by_category = defaultdict(list)
    for status, fname in files:
        ext = Path(fname).suffix.lower()
        cat_type, cat_label = CATEGORY_MAP.get(ext, ("chore", "arquivo"))
        verb_key = status[0] if status else "M"
        verb = STATUS_VERBS.get(verb_key, "atualiz")
        by_category[cat_type].append((fname, cat_label, verb, status))

    # Categoria principal (a mais frequente)
    main_cat = max(by_category, key=lambda k: len(by_category[k]))
    main_files = by_category[main_cat]

    # Nomes dos arquivos alterados (máx 3)
    file_names = [Path(f).name for f, _, _, _ in main_files[:3]]
    files_str = ", ".join(file_names)
    if len(main_files) > 3:
        files_str += f" e mais {len(main_files) - 3}"

    # Verbo predominante
    verbs = [v for _, _, v, _ in main_files]
    verb = max(set(verbs), key=verbs.count)

    # Monta prefixo do commit
    prefix = main_cat

    # Monta sumário secundário (outras categorias)
    other_cats = [k for k in by_category if k != main_cat]
    extra_parts = []
    for cat in other_cats[:2]:
        count = len(by_category[cat])
        labels = list(set(lbl for _, lbl, _, _ in by_category[cat]))
        extra_parts.append(f"{count} {labels[0]}")

    # Monta a mensagem
    if verb == "atualiz":
        action = f"atualiza {files_str}"
    elif verb == "adicionou":
        action = f"adiciona {files_str}"
    elif verb == "removeu":
        action = f"remove {files_str}"
    elif verb == "renomeou":
        action = f"renomeia {files_str}"
    else:
        action = f"modifica {files_str}"

    msg = f"{prefix}: {action}"

    if extra_parts:
        msg += f" + {', '.join(extra_parts)}"

    # Limitar para 72 chars (boa prática de git)
    if len(msg) > 72:
        msg = msg[:69] + "..."

    return msg


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    # Determina o diretório do projeto
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    project_dir = str(Path(project_dir).resolve())
    project_name = Path(project_dir).name

    # ── Banner ──────────────────────────────
    print(f"\n{BOLD}{CYAN}{'═' * 50}")
    print(f"  🚀  SMART DEPLOY  —  {project_name}")
    print(f"{'═' * 50}{RESET}")
    print(f"{GRAY}  📁 {project_dir}")
    print(f"  🕐 {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}{RESET}\n")

    # ── Verificações ────────────────────────
    step("Verificando repositório...")
    if not is_git_repo(project_dir):
        err("Este diretório não é um repositório Git!")
        err("Execute primeiro: git init && git remote add origin <url>")
        sys.exit(1)
    ok("Repositório Git detectado")

    if not has_remote(project_dir):
        err("Nenhum repositório remoto configurado (origin).")
        err("Execute: git remote add origin https://github.com/usuario/repo.git")
        sys.exit(1)
    ok("Repositório remoto encontrado")

    # ── Detecta mudanças ────────────────────
    step("Analisando alterações...")
    changed_files = get_changed_files(project_dir)

    if not changed_files:
        warn("Nenhuma alteração detectada. Nada para publicar!")
        sys.exit(0)

    # Mostra o que mudou
    added   = [f for s, f in changed_files if "A" in s or "?" in s]
    modified= [f for s, f in changed_files if "M" in s]
    deleted = [f for s, f in changed_files if "D" in s]

    if added:
        print(f"  {GREEN}+ Novos:     {', '.join(Path(f).name for f in added[:4])}{RESET}")
    if modified:
        print(f"  {YELLOW}~ Alterados: {', '.join(Path(f).name for f in modified[:4])}{RESET}")
    if deleted:
        print(f"  {RED}− Removidos: {', '.join(Path(f).name for f in deleted[:4])}{RESET}")

    total = len(changed_files)
    ok(f"{total} arquivo(s) com mudanças")

    # ── Gera commit message ──────────────────
    step("Gerando descrição automática...")
    commit_msg = smart_commit_message(changed_files)
    print(f"\n  {BOLD}📝 Commit: {YELLOW}{commit_msg}{RESET}")

    # ── Git add ─────────────────────────────
    step("Preparando arquivos (git add)...")
    _, code = run("git add .", cwd=project_dir)
    if code != 0:
        err("Falha no git add")
        sys.exit(1)
    ok("Todos os arquivos adicionados")

    # ── Git commit ───────────────────────────
    step("Criando commit...")
    _, code = run(f'git commit -m "{commit_msg}"', cwd=project_dir)
    if code != 0:
        err("Falha no git commit")
        sys.exit(1)
    ok("Commit criado com sucesso")

    # ── Git push ─────────────────────────────
    step("Publicando no GitHub...")
    _, code = run("git push", cwd=project_dir, capture=False)
    if code != 0:
        # Tenta setar upstream automaticamente
        out, _ = run("git branch --show-current", cwd=project_dir)
        branch = out.strip() or "main"
        _, code2 = run(f"git push --set-upstream origin {branch}", cwd=project_dir, capture=False)
        if code2 != 0:
            err("Falha no push. Verifique sua conexão e autenticação no GitHub.")
            sys.exit(1)

    # ── Sucesso ──────────────────────────────
    line()
    print(f"\n{BOLD}{GREEN}  ✅ PUBLICADO COM SUCESSO!{RESET}")
    print(f"\n  📝 Commit:  {YELLOW}{commit_msg}{RESET}")
    print(f"  📁 Projeto: {project_name}")
    print(f"  📂 {total} arquivo(s) atualizado(s)")

    # Tenta exibir a URL do GitHub Pages
    remote_url, _ = run("git remote get-url origin", cwd=project_dir)
    if "github.com" in remote_url:
        repo_path = remote_url.replace("https://github.com/", "").replace(".git", "")
        parts = repo_path.split("/")
        if len(parts) >= 2:
            username, reponame = parts[0], parts[1]
            print(f"\n  🌐 GitHub:       https://github.com/{username}/{reponame}")
            print(f"  🚀 GitHub Pages: https://{username}.github.io/{reponame}")

    print(f"\n{GRAY}  O site estará atualizado em ~2 minutos.{RESET}\n")


if __name__ == "__main__":
    main()
