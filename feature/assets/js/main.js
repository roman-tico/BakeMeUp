// =====================
// MENÚ HAMBURGUESA MÓVIL
// =====================
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        nav.classList.toggle('active');
    });

    // Cerrar menú al hacer click en un link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            nav.classList.remove('active');
        });
    });
}

// =====================
// SCROLL SUAVE PARA ANCLAS
// =====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');

        // Evitar interferir con links vacíos
        if (targetId === '#') return;

        const target = document.querySelector(targetId);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// =====================
// HEADER SCROLL BEHAVIOR
// (sombra + auto-hide)
// =====================
const header = document.querySelector('.header');
let lastScrollY = window.scrollY;
const scrollThreshold = 10;

window.addEventListener('scroll', () => {
    if (!header) return;

    // Si el menú móvil está abierto, no ocultar header
    if (nav && nav.classList.contains('active')) return;

    const currentScrollY = window.scrollY;

    // 🔹 Sombra del header
    if (currentScrollY > 0) {
        header.style.boxShadow = '0 2px 20px rgba(38, 18, 15, 0.15)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(38, 18, 15, 0.1)';
    }

    // 🔹 Evitar micro movimientos
    if (Math.abs(currentScrollY - lastScrollY) < scrollThreshold) return;

    // 🔹 Ocultar al bajar / mostrar al subir
    if (currentScrollY > lastScrollY && currentScrollY > 100) {
        header.classList.add('header--hidden');
    } else {
        header.classList.remove('header--hidden');
    }

    lastScrollY = currentScrollY;
});

// =====================
// ANIMACIONES DE ENTRADA (IntersectionObserver)
// =====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observar tarjetas de productos (si existen)
const productCards = document.querySelectorAll('.producto-card');
productCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = `all 0.6s ease ${index * 0.1}s`;
    observer.observe(card);
});

// =====================
// PRELOADER (opcional)
// =====================
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// =====================
// CONSOLA DE BIENVENIDA
// =====================
console.log('%c🧁 Bake Me Up 🧁', 'font-size: 20px; color: #535839; font-weight: bold;');
console.log('%cHecho con ❤️', 'font-size: 12px; color: #79879b;');
