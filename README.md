# BakeMeUp — Sitio web (Estático)

Repositorio para la web estática de BakeMeUp: landing + menú + "About us".

Estructura:
- index.html — Página principal / landing.
- menu.html — Página con catálogo / menú.
- about.html — Página "Sobre nosotros".
- assets/ — CSS, JavaScript e imágenes.

Cómo usar localmente:
1. Clona el repo:
   git clone https://github.com/roman-tico/BakeMeUp.git
2. Entra en la carpeta y abre `index.html` en el navegador.
   (No necesitas servidor; para desarrollo puedes usar `Live Server` en VSCode o `npx http-server`.)

Recomendaciones:
- Sustituye las imágenes en `assets/images/` por tus fotos optimizadas (webp o jpg comprimido).
- Edita textos (dirección, horario, redes) en los HTML.
- Para formularios de contacto simples usa mailto: o un servicio externo si lo necesitas (no incluimos formularios por ahora).

Despliegue:
- Opción rápida: GitHub Pages
  - Sube el repo a GitHub y en Settings → Pages elige la rama `main` y la carpeta `/ (root)`.
  - Espera unos minutos y la web estará online en https://<tu-usuario>.github.io/BakeMeUp
- Opción alternativa: Netlify / Vercel
  - Conecta el repositorio y despliegas automáticamente (buenas para añadir funciones futuras).

Contacto:
- Si quieres, puedo:
  - Añadir imágenes de muestra mejoradas.
  - Preparar el repo y crear el deploy en Netlify por ti.
