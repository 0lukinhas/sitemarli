document.addEventListener("DOMContentLoaded", (event) => {

    // ─── HERO ANIMATION (GSAP Timeline — no ScrollTrigger, fires immediately) ───
    gsap.registerPlugin(ScrollTrigger);

    const heroTimeline = gsap.timeline({ defaults: { ease: "power3.out" } });
    heroTimeline
        .from(".hero-text-large h1", {
            y: 80,
            opacity: 0,
            duration: 1.4,
            delay: 0.2,
        })
        .from(".hero-subtitle *", {
            y: 25,
            opacity: 0,
            duration: 0.9,
            stagger: 0.12
        }, "-=0.8");

    // ─── NAVBAR SCROLL EFFECT ───
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        lastScrollY = window.scrollY;

        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            navbar.style.background = 'rgba(252, 249, 234, 0.98)';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.color = '#1B3731';
            navbar.style.padding = '0.4rem max(5vw, 40px)';
            navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
            navbar.querySelectorAll('a, button').forEach(el => {
                el.style.color = '#1B3731';
                el.style.textShadow = 'none';
            });
        } else {
            navbar.classList.remove('scrolled');
            navbar.style.background = 'transparent';
            navbar.style.backdropFilter = 'none';
            navbar.style.color = 'white';
            navbar.style.padding = '0.8rem max(5vw, 40px)';
            navbar.style.boxShadow = 'none';
            navbar.querySelectorAll('a, button').forEach(el => {
                el.style.color = 'white';
                el.style.textShadow = '0 1px 3px rgba(0,0,0,0.5)';
            });
        }
    });

    // ─── MOBILE MENU ───
    const mobileMenu = document.getElementById('mobileMenu');
    const menuToggle = document.querySelector('.menu-toggle');
    const closeMenu = document.getElementById('closeMenu');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    if (menuToggle && mobileMenu && closeMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        closeMenu.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ─── INTERSECTION OBSERVER — CSS-based reveal (100% reliable) ───
    // Elements start visible. When they enter viewport, add class that plays animation.
    // No opacity:0 trap. No ScrollTrigger dependency.

    const revealItems = document.querySelectorAll(
        '.t-card, .testimonial-card, .gallery-card, ' +
        '.science-text h2, .science-text p, .science-text .link-arrow, ' +
        '.science-image, .mentorship-text h2, .mentorship-text p, ' +
        '.differentials-header h2'
    );

    const observerOptions = {
        rootMargin: '0px 0px -40px 0px', // trigger 40px before bottom edge
        threshold: 0.05 // just 5% visible is enough to trigger
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target); // fire once only
            }
        });
    }, observerOptions);

    revealItems.forEach((el, index) => {
        // stagger delay via CSS custom property
        el.style.setProperty('--reveal-delay', `${(index % 6) * 0.08}s`);
        el.classList.add('reveal-on-scroll');
        revealObserver.observe(el);
    });

    // ─── CAROUSEL NAVIGATION ───
    const carouselSections = document.querySelectorAll('.testimonials-section, .experience-section');
    carouselSections.forEach(section => {
        const prevBtn = section.querySelector('.prev-btn');
        const nextBtn = section.querySelector('.next-btn');
        const container = section.querySelector('.testimonials-carousel, .gallery-carousel');

        if (prevBtn && nextBtn && container) {
            prevBtn.addEventListener('click', () => {
                const card = container.querySelector('div');
                const cardWidth = card ? card.offsetWidth + 20 : 340;
                container.scrollBy({ left: -cardWidth, behavior: 'smooth' });
            });
            nextBtn.addEventListener('click', () => {
                const card = container.querySelector('div');
                const cardWidth = card ? card.offsetWidth + 20 : 340;
                container.scrollBy({ left: cardWidth, behavior: 'smooth' });
            });
        }
    });

    // ─── SMOOTH SCROLLING ───
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// ─── PROMO MODAL ───
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('promoModal');
    const closeBtn = document.querySelector('.promo-close');
    const declineBtn = document.getElementById('btnDeclinePromo');

    if (modal) {
        setTimeout(() => { modal.classList.add('active'); }, 3000);
        const closeModal = () => modal.classList.remove('active');
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        if (declineBtn) declineBtn.addEventListener('click', closeModal);
        window.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
    }
});
