# Portfolio 2026 · Juan Ruiz "Yeezy"

Sitio web del portafolio, reconstruido en HTML + CSS + JavaScript (Vite) a partir del PDF original.
El PDF es la fuente de verdad: colores, tipografías, composiciones, imágenes y textos se conservan.

- **Escritorio (≥ 1000 px):** cada pieza se coloca con las coordenadas exactas del PDF y la composición completa se escala con el ancho de la pantalla.
- **Tablet / móvil:** recomposición vertical con los mismos recursos y textos reales (legibles), sin reducir la versión de escritorio.
- **Experiencia:** scroll suave (Lenis), animaciones al hacer scroll (GSAP + ScrollTrigger), revelado de imágenes con máscara, parallax suave, lightbox con teclado y gestos, menú con sección activa y barra de progreso.
- **Accesibilidad:** textos reales, `alt` en imágenes, navegación por teclado, foco visible, enlace "Saltar al contenido" y respeto de `prefers-reduced-motion`.

## Ejecutar en tu computador

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # genera /dist
npm run preview    # prueba la versión compilada
```

Requiere Node 18 o superior.

## Publicar con GitHub + Vercel

1. Crea un repositorio nuevo en GitHub y sube **la carpeta del proyecto** (la que contiene `package.json`):
   ```bash
   git init
   git add .
   git commit -m "Portafolio 2026"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```
2. En [vercel.com/new](https://vercel.com/new) importa el repositorio. Vercel detecta Vite automáticamente
   (`vercel.json` ya incluye comando de compilación `npm run build` y carpeta de salida `dist`).
3. Pulsa **Deploy**. Al terminar tendrás el enlace público del portafolio.

## Antes de publicar

- **Instagram y LinkedIn:** el PDF muestra los iconos pero no las direcciones. Ya están configuradas en `src/main.js`, objeto `SOCIAL` (Instagram, LinkedIn y el enlace de "Destino sin retorno"); puedes cambiarlas ahí
  (si se dejan vacías, los iconos se muestran sin enlace).
- **Dominio y vista previa social:** al tener la URL final, actualiza `canonical` y `og:image` en `index.html`
  con la dirección completa (por ejemplo `https://tu-dominio.com/og.jpg`).

## Estructura

```
index.html            Contenido (escritorio #stage + móvil #flow)
src/main.js           Lenis, GSAP/ScrollTrigger, menú, lightbox, cursor
src/style.css         Estilos y composición
public/img/           Imágenes extraídas del PDF y sprites de títulos (WebP)
public/favicon.svg    Icono
tools/                Scripts (Python) que regeneraron los recursos desde el PDF y pruebas funcionales (opcional)
vercel.json           Configuración de despliegue y caché
```

## Nota sobre tipografías

Poppins, Chau Philomene One se cargan localmente (paquetes `@fontsource`). Los títulos decorativos
(Anaconda Wildstyle y los lockups tipográficos del diseño) están incluidos como imágenes vectoriales
extraídas del PDF para conservar exactamente su apariencia; su texto equivalente está disponible para
lectores de pantalla.
