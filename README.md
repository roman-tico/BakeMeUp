# Bake Me Up 🧁 - Documentación Técnica y Arquitectura

Bienvenido a la documentación oficial y detallada del proyecto **Bake Me Up**. Este repositorio contiene el código fuente de una aplicación web estática, altamente optimizada y sin dependencias externas complejas (sin React, Angular, ni Node.js modules). Está construida puramente con **HTML5, CSS3 y JavaScript Vanilla**.

El objetivo de esta arquitectura es ofrecer un rendimiento altísimo, ser fácilmente indexable por motores de búsqueda (SEO) y mantener una curva de aprendizaje mínima para futuros desarrollos.

---

## 📁 Arquitectura Completa del Repositorio

El proyecto está dividido en tres pilares fundamentales que viven en la raíz del repositorio: **Vistas Principales (HTML)**, **Recursos Estáticos (`assets/`)** y **Módulos Reutilizables (`components/`)**.

A continuación se detalla cada componente y cómo contribuye al ecosistema del sitio web:

### 1. Vistas Principales (Raíz)
Estos son los archivos de entrada o "páginas" a las que acceden los usuarios directamente.
- `index.html`: La página de inicio (Landing Page). Contiene el gancho visual (Hero), un resumen de la esencia de la marca, una cuadrícula con productos destacados y la información de horarios/ubicación.
- `about.html`: Página "Sobre nosotras". Cuenta con un diseño alternado por colores (crema, verde oliva, oscuro) que narra la historia, misión, visión y valores de la marca mediante un diseño tipográfico de columnas.
- `menu.html`: El catálogo digital de los productos. Está diseñado para que los clientes puedan revisar las categorías (bebidas calientes, pasteles, etc.).
- `custom-cake.html`: Página interactiva y detallada sobre la personalización de pasteles.

### 2. Recursos Estáticos (`/assets`)
Aquí vive toda la capa visual, interactiva y de medios visuales. Todo lo que embellece y da funcionalidad a la página está aquí.

#### `/assets/css/` (Hojas de Estilo Modulares)
El CSS no está en un solo archivo gigante, sino que está modularizado para evitar conflictos y facilitar la lectura:
- **`styles.css`:** Es el "Corazón del Diseño". Aquí se definen:
  - **Variables Globales (`:root`)**: Los colores oficiales de la marca (`--verde-oliva`, `--dorado`, `--cafe-oscuro`, `--crema`, `--blanco`). Si cambias un color aquí, cambiará en todo el sitio de forma automática.
  - **Tipografía Global y Reseteos**: Asegura que la fuente `Armany` se vea igual en todos los navegadores.
  - **Estilos de Componentes Compartidos**: Estilos del menú de navegación, botones globales (`.btn-primary`), títulos de secciones y el diseño del Footer y Header.
- **`home.css`:** Contiene clases estrictamente utilizadas en `index.html` (ej. el Hero principal, la cuadrícula de productos, sección Welcome).
- **`about.css`:** Estilos exclusivos para la narración visual de `about.html` (textos en columnas, tarjetas con sombras dinámicas sobre fondos verdes).
- **`custom-cake.css`:** Reglas CSS dedicadas únicamente al diseño de la página de pasteles personalizados.

#### `/assets/js/` (Lógica e Interactividad)
- **`main.js`:** El único controlador de JavaScript. Su función es vital y se divide en:
  1. **Inyección Dinámica:** Busca los `divs` con IDs especiales (`#header-placeholder`) y mediante una petición `fetch`, carga el código HTML directamente desde la carpeta `/components`.
  2. **Interacciones UI:** Activa el menú de hamburguesa en pantallas de celular.
  3. **Animaciones al hacer Scroll (Intersection Observer):** Detecta cuando el usuario baja por la página y hace aparecer suavemente las tarjetas de productos (`.producto-card`) desde abajo.
  4. **Navegación Suave (Smooth Scroll):** Para los anclajes de la página.

#### `/assets/images/` y `/assets/fonts/`
- **`fonts/`:** Tipografías locales (`Armany` y `Bake Script`). Al estar locales en el repositorio, la web no depende de Google Fonts, aumentando la velocidad de carga y privacidad.
- **`images/`:** Fotografías de productos (optimizadas en formato `.webp` para que pesen poco), íconos SVG y logotipos en alta resolución.

### 3. Módulos Reutilizables (`/components`)
Esta carpeta soluciona el clásico problema de tener que copiar y pegar el mismo Header y Footer en cada una de las páginas HTML.

- **`header.html`:** Contiene el logotipo, los enlaces de navegación y el botón del menú de hamburguesa.
- **`footer.html`:** Contiene los horarios dinámicos, enlaces de redes sociales y derechos de autor.

**¿Cómo funciona esta inyección?**
Cuando abres `index.html` en el navegador, el navegador lee la etiqueta vacía `<div id="header-placeholder"></div>`. Inmediatamente después, `main.js` entra en acción, va a la carpeta `components/`, copia el código de `header.html` y lo rellena dentro de ese `div`. Esto significa que **si un día necesitas agregar una nueva pestaña al menú, solo editas `header.html` una vez**, y se actualizará instantáneamente en todo el sitio web.

---

## 🛠️ Guía de Desarrollo Local

Debido a que el JavaScript utiliza la API `fetch` para traer los componentes (Header y Footer), **no puedes simplemente dar doble clic a `index.html` para verlo en tu navegador.** Los navegadores modernos bloquean estas peticiones por seguridad (política de CORS) cuando se usan bajo el protocolo `file://`.

Necesitas levantar un servidor local ligero:

### Método 1: Python (Para Mac/Linux o Windows con Python instalado)
1. Abre tu terminal (Símbolo del sistema, PowerShell, Terminal de MacOS).
2. Navega con el comando `cd` hasta la carpeta donde descargaste este repositorio.
3. Ejecuta el comando mágico:
   ```bash
   python -m http.server 8080
   ```
4. Abre tu navegador favorito y escribe: `http://localhost:8080`.

### Método 2: VS Code (La forma más visual)
1. Descarga el editor **Visual Studio Code**.
2. Instala la extensión llamada **"Live Server"** (de Ritwick Dey).
3. Abre la carpeta de este proyecto en VS Code.
4. Haz clic derecho sobre el archivo `index.html` y selecciona **"Open with Live Server"**. Se abrirá una ventana automática en tu navegador.

---

## 🚀 Despliegue en Producción

El sitio es estático, lo que significa que el alojamiento puede ser completamente gratuito, extremadamente rápido e inmune a los clásicos ataques de bases de datos.

Recomendamos **GitHub Pages** (es gratis y está integrado):
1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a la pestaña **Settings** (Configuración) de tu repositorio.
3. Selecciona **Pages** en el menú lateral izquierdo.
4. En **Source** o **Branch**, selecciona la rama `main` y guarda.
5. GitHub procesará tu código y en menos de 2 minutos tu página estará viva en Internet en el enlace proporcionado.

---
*Documentación técnica redactada para garantizar la escalabilidad y mantenibilidad de Bake Me Up a futuro.*
