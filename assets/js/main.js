// =============================
// UTILIDADES
// =============================
const $ = (selector, scope = document) => scope.querySelector(selector);
const $$ = (selector, scope = document) => scope.querySelectorAll(selector);

// =============================
// CARGAR COMPONENTES (HEADER / FOOTER)
// =============================
async function loadComponent(id, path) {
    const el = document.getElementById(id);
    if (!el) return;

    try {
        const res = await fetch(path);
        if (res.ok) {
            el.innerHTML = await res.text();
        }
    } catch (err) {
        console.error("No se pudo cargar:", path, err);
    }
}

// =============================
// MARCAR ENLACE ACTIVO EN NAV
// =============================
function initActiveNavLink() {
    const rawPath = window.location.pathname.split('/').pop();
    const currentPage = rawPath === '' ? 'index.html' : rawPath;

    $$('.nav-link, .nav-cta').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            if (link.classList.contains('nav-link')) {
                link.classList.add('active');
            }
            link.setAttribute('aria-current', 'page');
        }
    });
}

// =============================
// MENÚ HAMBURGUESA (MÓVIL)
// =============================
function initMobileMenu() {
    const menuToggle = $('.menu-toggle');
    const nav = $('.nav');

    if (!menuToggle || !nav) return;

    const closeMenu = () => {
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('active');
        document.body.classList.remove('menu-open');
    };

    const toggleMenu = () => {
        const isOpen = nav.classList.toggle('active');
        menuToggle.classList.toggle('active', isOpen);
        menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        document.body.classList.toggle('menu-open', isOpen);
    };

    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.addEventListener('click', toggleMenu);

    // Cerrar al tocar cualquier enlace del menú (incluyendo el CTA)
    $$('.nav-link, .nav-cta', nav).forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Cerrar con tecla Escape
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && nav.classList.contains('active')) {
            closeMenu();
        }
    });

    // Cerrar si la pantalla cambia a escritorio
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && nav.classList.contains('active')) {
            closeMenu();
        }
    }, { passive: true });
}

// =============================
// SCROLL SUAVE
// =============================
function initSmoothScroll() {
    $$('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', e => {
            const targetId = anchor.getAttribute('href');
            if (!targetId || targetId === '#') return;

            const target = $(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// =============================
// HEADER SCROLL BEHAVIOR
// =============================
function initHeaderScroll() {
    const header = $('.header');
    const nav = $('.nav');

    if (!header) return;

    let lastScroll = window.scrollY;
    const threshold = 10;

    window.addEventListener('scroll', () => {
        if (nav && nav.classList.contains('active')) return;

        const current = window.scrollY;

        // Sombra dinámica al hacer scroll
        header.style.boxShadow =
            current > 10
                ? '0 4px 22px rgba(38, 18, 15, 0.12)'
                : '0 1px 3px rgba(38, 18, 15, 0.08)';

        if (Math.abs(current - lastScroll) < threshold) return;

        if (current > lastScroll && current > 110) {
            header.classList.add('header--hidden');
        } else {
            header.classList.remove('header--hidden');
        }

        lastScroll = current;
    }, { passive: true });
}

// =============================
// ANIMACIONES SCROLL (SUAVES)
// =============================
function initScrollAnimations() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const animatedElements = $$(
        '.producto-card, .cake-row, .mv-card, .value-card, .about-quote-card, .step-card, .faq-card'
    );
    if (!animatedElements.length) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    animatedElements.forEach((el, index) => {
        el.classList.add('reveal-on-scroll');
        // Escalonamiento sutil para elementos en grilla
        const delay = (index % 3) * 0.08;
        el.style.transitionDelay = `${delay}s`;
        observer.observe(el);
    });
}

// =============================
// PRELOADER
// =============================
function initPreloader() {
    if (document.readyState === 'complete') {
        document.body.classList.add('loaded');
    } else {
        window.addEventListener('load', () => {
            document.body.classList.add('loaded');
        });
    }
}

// =============================
// INIT APP
// =============================
document.addEventListener('DOMContentLoaded', async () => {
    // Evitar doble inicialización accidental
    if (window.__bmuInitialized) return;
    window.__bmuInitialized = true;

    // Cargar componentes compartidos
    await Promise.all([
        loadComponent("header-placeholder", "components/header.html"),
        loadComponent("footer-placeholder", "components/footer.html")
    ]);

    // Inicializar módulos
    initActiveNavLink();
    initMobileMenu();
    initSmoothScroll();
    initHeaderScroll();
    initScrollAnimations();
    initPreloader();
});

// =============================
// CONSOLA
// =============================
console.log('%c🧁 Bake Me Up 🧁', 'font-size:20px;color:#535839;font-weight:bold;');
console.log('%cHecho con ❤️', 'font-size:12px;color:#79879b;');
