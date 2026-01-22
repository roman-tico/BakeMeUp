// =====================
// MENÚ HAMBURGUESA MÓVIL
// =====================
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (menuToggle) {
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
// SCROLL SUAVE
// =====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// =====================
// HEADER SCROLL EFFECT
// =====================
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    // Agregar sombra al header cuando hay scroll
    if (currentScroll > 0) {
        header.style.boxShadow = '0 2px 20px rgba(38, 18, 15, 0.15)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(38, 18, 15, 0.1)';
    }

    lastScroll = currentScroll;
});

// =====================
// ANIMACIÓN DE ENTRADA
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

// Observar tarjetas de productos
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
console.log('%c🧁 Bake me up 🧁', 'font-size: 20px; color: #535839; font-weight: bold;');
console.log('%cHecho con ❤️ para Sofía Gavito', 'font-size: 12px; color: #79879b;');
