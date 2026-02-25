---
description: Publicar alterações no GitHub com geração automática de commit message. Use /publicar para fazer deploy inteligente de qualquer projeto.
---

# /publicar — Smart Deploy Global

$ARGUMENTS

---

## O que este comando faz

1. **Analisa** automaticamente todos os arquivos alterados
2. **Gera** uma mensagem de commit descritiva e inteligente
3. **Publica** no GitHub com `git add → commit → push`
4. **Exibe** os links do repositório e do GitHub Pages

---

## Como usar

```
/publicar              → publica o projeto atual
/publicar ./meu-site  → publica um projeto específico
```

---

## Execução

// turbo
1. Run the smart deploy script for the current project:

```bash
python3 "/Users/lucasumpr/Documents/Site Marli/.agent/scripts/smart_deploy.py"
```

Se o usuário especificou um diretório diferente como argumento ($ARGUMENTS), use:

```bash
python3 "/Users/lucasumpr/Documents/Site Marli/.agent/scripts/smart_deploy.py" $ARGUMENTS
```

---

## Casos de Erro Comuns

| Erro | Solução |
|------|---------|
| "Não é um repositório Git" | Execute `git init` e conecte ao GitHub primeiro |
| "Nenhum remote configurado" | Execute `git remote add origin <url>` |
| "Falha no push" | Verifique autenticação GitHub (token ou SSH) |
| "Nada para publicar" | Não há alterações desde o último push |

---

## Exemplo de Saída

```
══════════════════════════════════════
  🚀  SMART DEPLOY  —  site-marli  
══════════════════════════════════════

▶ Analisando alterações...
  ~ Alterados: index.html, styles.css
  ✅ 2 arquivo(s) com mudanças

▶ Gerando descrição automática...
  📝 Commit: style: atualiza styles.css + 1 página HTML

▶ Publicando no GitHub...
  ✅ PUBLICADO COM SUCESSO!

  🌐 GitHub:       https://github.com/0lukinhas/sitemarli
  🚀 GitHub Pages: https://0lukinhas.github.io/sitemarli
```
