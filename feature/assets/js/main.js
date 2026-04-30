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
        el.innerHTML = await res.text();
    } catch (err) {
        console.error("No se pudo cargar:", path);
    }
}

// =============================
// MENÚ HAMBURGUESA
// =============================
function initMobileMenu() {

    const menuToggle = $('.menu-toggle');
    const nav = $('.nav');

    if (!menuToggle || !nav) return;

    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        nav.classList.toggle('active');
    });

    $$('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            nav.classList.remove('active');
        });
    });

}

// =============================
// SCROLL SUAVE
// =============================
function initSmoothScroll() {

    $$('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener('click', e => {

            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

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

        // sombra
        header.style.boxShadow =
            current > 0
                ? '0 2px 20px rgba(38,18,15,0.15)'
                : '0 2px 10px rgba(38,18,15,0.1)';

        if (Math.abs(current - lastScroll) < threshold) return;

        if (current > lastScroll && current > 100) {
            header.classList.add('header--hidden');
        } else {
            header.classList.remove('header--hidden');
        }

        lastScroll = current;

    });

}

// =============================
// ANIMACIONES SCROLL
// =============================
function initScrollAnimations() {

    const cards = $$('.producto-card');
    if (!cards.length) return;

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }

        });

    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    cards.forEach((card, i) => {

        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${i * 0.1}s`;

        observer.observe(card);

    });

}

// =============================
// PRELOADER
// =============================
function initPreloader() {

    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

}

// =============================
// INIT APP
// =============================
document.addEventListener('DOMContentLoaded', async () => {

    // cargar componentes
    await loadComponent("header-placeholder", "feature/components/header.html");
    await loadComponent("footer-placeholder", "feature/components/footer.html");

    // inicializar módulos
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

