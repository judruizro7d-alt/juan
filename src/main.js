import "@fontsource/poppins/400.css";
import "@fontsource/poppins/600.css";
import "@fontsource/poppins/700.css";
import "@fontsource/poppins/800.css";
import "@fontsource/chau-philomene-one/400.css";
import "./style.css";

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";

gsap.registerPlugin(ScrollTrigger);

/* ------------------------------------------------------------------
   Enlaces externos del portafolio (el PDF muestra los iconos de
   Instagram y LinkedIn pero no incluye las direcciones: pégalas aquí).
   Si se dejan vacías, los iconos se muestran sin enlace.
------------------------------------------------------------------- */
export const SOCIAL = {
  instagram: "https://www.instagram.com/negrxx_________/",
  linkedin: "https://www.linkedin.com/in/juan-diego-ruiz-rodr%C3%ADguez-562900354",
  destino: "https://www.youtube.com/watch?v=Va8sCwFzLV8", // título "DESTINO SIN RETORNO"
};

const root = document.documentElement;
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
const desktopMQ = window.matchMedia("(min-width: 1000px)");
if (reduce) root.classList.add("rm");

/* escala de la composición de escritorio: 1 unidad de diseño = ancho/1440 */
function setUnit() {
  const w = Math.min(root.clientWidth, 1920);
  root.style.setProperty("--u", `${w / 1440}px`);
}
setUnit();
window.addEventListener("resize", () => { setUnit(); ScrollTrigger.refresh(); }, { passive: true });

/* ------------------------------------------------------------------ scroll suave */
let lenis = null;
if (!reduce) {
  lenis = new Lenis({ duration: 1.15, easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
}
const scrollToEl = (el, offset = -70) => {
  if (!el) return;
  if (lenis) lenis.scrollTo(el, { offset, duration: 1.6 });
  else el.scrollIntoView({ behavior: "auto", block: "start" });
};

/* ------------------------------------------------------------------ navegación */
const nav = document.getElementById("nav");
const burger = document.getElementById("burger");
const menu = document.getElementById("menu");
const progress = document.getElementById("progress");
const navLinks = [...document.querySelectorAll("[data-nav]")];

function anchorFor(key) {
  if (desktopMQ.matches) return document.getElementById(key);
  return document.getElementById("m-" + key) || document.getElementById(key === "inicio" ? "m-inicio" : key);
}
function setMenu(open) {
  menu.classList.toggle("open", open);
  burger.setAttribute("aria-expanded", String(open));
  burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  if (lenis) open ? lenis.stop() : lenis.start();
  else document.body.style.overflow = open ? "hidden" : "";
}
burger.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
navLinks.forEach((a) =>
  a.addEventListener("click", (e) => {
    e.preventDefault();
    const key = a.dataset.nav;
    if (menu.classList.contains("open")) setMenu(false);
    const target = key === "inicio" ? document.body : anchorFor(key);
    if (key === "inicio") (lenis ? lenis.scrollTo(0, { duration: 1.6 }) : window.scrollTo(0, 0));
    else scrollToEl(target);
    history.replaceState(null, "", "#" + key);
  })
);
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && menu.classList.contains("open")) { setMenu(false); burger.focus(); }
});
// ocultar al bajar, mostrar al subir
let lastY = 0;
function onScroll() {
  const y = window.scrollY;
  const max = root.scrollHeight - window.innerHeight;
  progress.style.transform = `scaleX(${max > 0 ? Math.min(1, y / max) : 0})`;
  nav.classList.toggle("compact", y > 160);
  lastY = y;
}
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

/* sección activa en el menú */
let spyRaf = 0;
function spyItems() {
  const keys = ["inicio", "sobre-mi", "estudios", "trabajo", "educativos", "capital", "prints", "contacto"];
  return keys.map((k) => [k, k === "inicio" ? document.getElementById(desktopMQ.matches ? "inicio" : "m-inicio") : anchorFor(k)]).filter(([, el]) => el);
}
function updateSpy() {
  spyRaf = 0;
  const line = window.innerHeight * 0.45;
  let cur = "inicio";
  for (const [k, el] of spyItems()) if (el.getBoundingClientRect().top <= line) cur = k;
  navLinks.forEach((a) => a.classList.toggle("on", a.dataset.nav === cur && !a.classList.contains("brand")));
}
function setupSpy() { updateSpy(); }
window.addEventListener("scroll", () => { if (!spyRaf) spyRaf = requestAnimationFrame(updateSpy); }, { passive: true });

/* ------------------------------------------------------------------ cursor */
if (finePointer && !reduce) {
  const c = document.getElementById("cursor");
  const pos = { x: -100, y: -100, tx: -100, ty: -100 };
  window.addEventListener("pointermove", (e) => { pos.tx = e.clientX; pos.ty = e.clientY; c.classList.add("vis"); }, { passive: true });
  document.addEventListener("pointerleave", () => c.classList.remove("vis"));
  gsap.ticker.add(() => {
    pos.x += (pos.tx - pos.x) * 0.22; pos.y += (pos.ty - pos.y) * 0.22;
    c.style.transform = `translate3d(${pos.x}px,${pos.y}px,0)`;
  });
  c.querySelector("span") || c.insertAdjacentHTML("beforeend", "<span>VER</span>");
  document.addEventListener("pointerover", (e) => {
    const t = e.target.closest?.(".ph:not(.static), .pol, [data-lb]");
    const l = e.target.closest?.("a, button:not([data-lb])");
    c.classList.toggle("zoom", !!t);
    c.classList.toggle("link", !t && !!l);
  });
}

/* ------------------------------------------------------------------ lightbox */
const lb = document.getElementById("lb");
const lbImg = document.getElementById("lb-img");
const lbCap = document.getElementById("lb-cap");
const lbCount = document.getElementById("lb-c");
let group = [], idx = 0, opener = null;

function lbShow(i, dir = 0) {
  idx = (i + group.length) % group.length;
  const it = group[idx];
  const swap = () => {
    lbImg.src = it.dataset.src; lbImg.alt = it.dataset.alt || "";
    lbCap.textContent = it.dataset.alt || "";
    lbCount.textContent = `${idx + 1} / ${group.length}`;
    if (!reduce) gsap.fromTo(lbImg, { autoAlpha: 0, x: dir * 40, scale: 0.98 }, { autoAlpha: 1, x: 0, scale: 1, duration: 0.5, ease: "power3.out" });
  };
  reduce || !lbImg.src ? swap() : gsap.to(lbImg, { autoAlpha: 0, x: -dir * 30, duration: 0.18, onComplete: swap });
  // precarga vecinas
  [idx - 1, idx + 1].forEach((j) => { const n = group[(j + group.length) % group.length]; if (n) { const p = new Image(); p.src = n.dataset.src; } });
  document.getElementById("lb-p").style.display = document.getElementById("lb-n").style.display = group.length > 1 ? "" : "none";
}
function lbOpen(btn) {
  const g = btn.dataset.lb;
  group = [...document.querySelectorAll(`[data-lb="${g}"]`)].filter((n) => n.offsetParent !== null);
  idx = Math.max(0, group.indexOf(btn));
  opener = btn;
  lbImg.removeAttribute("src");
  lb.hidden = false;
  if (lenis) lenis.stop(); else document.body.style.overflow = "hidden";
  if (!reduce) gsap.fromTo(lb, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.35, ease: "power2.out" });
  lbShow(idx);
  const fx = () => document.getElementById("lb-x").focus({ preventScroll: true });
  reduce ? fx() : gsap.delayedCall(0.08, fx);
}
function lbClose() {
  const done = () => { lb.hidden = true; if (lenis) lenis.start(); else document.body.style.overflow = ""; opener && opener.focus({ preventScroll: true }); };
  reduce ? done() : gsap.to(lb, { autoAlpha: 0, duration: 0.25, onComplete: done });
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-lb]");
  if (b && !lb.contains(b)) { e.preventDefault(); lbOpen(b); }
});
document.getElementById("lb-x").addEventListener("click", lbClose);
document.getElementById("lb-p").addEventListener("click", () => lbShow(idx - 1, -1));
document.getElementById("lb-n").addEventListener("click", () => lbShow(idx + 1, 1));
lb.addEventListener("click", (e) => { if (e.target === lb) lbClose(); });
window.addEventListener("keydown", (e) => {
  if (lb.hidden) return;
  if (e.key === "Escape") lbClose();
  else if (e.key === "ArrowLeft") lbShow(idx - 1, -1);
  else if (e.key === "ArrowRight") lbShow(idx + 1, 1);
  else if (e.key === "Tab") { // foco atrapado dentro del visor
    const f = [...lb.querySelectorAll("button")].filter((n) => n.style.display !== "none");
    const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
});
// deslizar en móvil
let sx = 0;
lb.addEventListener("touchstart", (e) => { sx = e.changedTouches[0].clientX; }, { passive: true });
lb.addEventListener("touchend", (e) => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) lbShow(idx + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1); }, { passive: true });

/* ------------------------------------------------------------------ iconos sociales (enlace solo si hay URL) */
function wireSocial(scope) {
  scope.querySelectorAll(".spr[src*='s-iconos']").forEach((img) => {
    const wrap = img.parentElement;
    if (wrap.dataset.social) return;
    wrap.dataset.social = "1";
    const mk = (href, label, left) => {
      if (!href) return;
      const a = document.createElement("a");
      a.href = href; a.target = "_blank"; a.rel = "noopener noreferrer"; a.setAttribute("aria-label", label);
      a.style.cssText = `position:absolute;top:0;bottom:0;${left ? "left:0;width:46%" : "right:0;width:46%"}`;
      wrap.style.position = "absolute" === getComputedStyle(wrap).position ? "absolute" : "relative";
      wrap.appendChild(a);
    };
    mk(SOCIAL.instagram, "Instagram", true);
    mk(SOCIAL.linkedin, "LinkedIn", false);
  });
  // título "DESTINO SIN RETORNO" -> enlace al proyecto (si hay URL)
  if (SOCIAL.destino) {
    scope.querySelectorAll(".destino").forEach((p) => {
      if (p.querySelector("a")) return;
      const a = document.createElement("a");
      a.href = SOCIAL.destino; a.target = "_blank"; a.rel = "noopener noreferrer";
      a.className = "destino-link"; a.setAttribute("aria-label", "Ver el proyecto Destino sin retorno (se abre en una pestaña nueva)");
      while (p.firstChild) a.appendChild(p.firstChild);
      p.appendChild(a);
    });
  }
}

/* ------------------------------------------------------------------ animaciones al hacer scroll */
const ease = "power3.out";
function setupAnimations(scope) {
  const mkST = (el, extra = {}) => ({ trigger: el, start: "top 88%", once: true, ...extra });

  // textos: aparición por líneas escalonadas
  scope.querySelectorAll('[data-r="lines"]').forEach((el) => {
    const lines = el.querySelectorAll(".ln, li, p");
    const tg = lines.length ? lines : el;
    gsap.fromTo(tg, { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.9, ease, stagger: 0.07, scrollTrigger: mkST(el) });
    gsap.set(el, { visibility: "visible" });
  });
  scope.querySelectorAll('[data-r="up"]').forEach((el) => {
    gsap.fromTo(el, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1, ease, scrollTrigger: mkST(el) });
  });
  scope.querySelectorAll('[data-r="fade"]').forEach((el) => {
    gsap.fromTo(el, { autoAlpha: 0 }, { autoAlpha: 1, duration: 1.4, ease: "power2.out", scrollTrigger: mkST(el, { start: "top 92%" }) });
  });
  // títulos (sprites): barrido de izquierda a derecha con desplazamiento
  scope.querySelectorAll('[data-r="title"]').forEach((el) => {
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(el, { clipPath: "inset(0 100% 0 0)", x: -28 }, { clipPath: "inset(0 0% 0 0)", x: 0, duration: 1.25, ease: "power3.inOut", scrollTrigger: mkST(el, { start: "top 90%" }) });
  });
  // fotografías: revelado con máscara + zoom
  scope.querySelectorAll('[data-r="mask"]').forEach((el) => {
    const inner = el.querySelector("img:not(.frm)");
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(el, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 1.15, ease: "power3.inOut", scrollTrigger: mkST(el, { start: "top 90%" }) });
    if (inner) gsap.fromTo(inner, { scale: 1.28 }, { scale: 1, duration: 1.6, ease: "power3.out", clearProps: "transform", scrollTrigger: mkST(el, { start: "top 90%" }) });
  });
  // retrato principal
  scope.querySelectorAll('[data-r="portrait"]').forEach((el) => {
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(el, { clipPath: "inset(100% 0 0 0)", y: 30 }, { clipPath: "inset(0% 0 0 0)", y: 0, duration: 1.5, ease: "power3.inOut", scrollTrigger: mkST(el, { start: "top 92%" }) });
  });
  // profundidad: parallax suave y giros mínimos en recursos decorativos
  scope.querySelectorAll("[data-p]").forEach((el) => {
    const f = parseFloat(el.dataset.p) || 0.04;
    const rot = parseFloat(el.dataset.rot) || 0;
    const to = { y: () => -f * window.innerHeight * 2.2, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: 0.6, invalidateOnRefresh: true } };
    if (rot) to.rotation = rot;
    gsap.fromTo(el, { y: () => f * window.innerHeight * 2.2, rotation: rot ? -rot : 0 }, to);
  });
  scope.querySelectorAll(".d-pin, .d-dice").forEach((el) => {
    const img = el.querySelector("img"); if (!img) return;
    el.addEventListener("pointerenter", () => gsap.to(img, { rotation: gsap.utils.random(-6, 6), scale: 1.04, duration: 0.5, ease: "power3.out" }));
    el.addEventListener("pointerleave", () => gsap.to(img, { rotation: 0, scale: 1, duration: 0.7, ease: "elastic.out(1,.5)" }));
  });

  // recursos decorativos: flotación muy lenta (solo desplazamiento vertical, sin tocar su posición original)
  scope.querySelectorAll(".d-dice, .d-pin, .d-camera, .d-spike, .d-flower, .d-redflower, .d-splat, .f-dice, .f-pin, .f-camera, .f-plant, .f-redflower, .f-rays, .f-burst").forEach((el, i) => {
    const img = el.tagName === "IMG" ? el : el.querySelector("img"); if (!img) return;
    gsap.to(img, { y: i % 2 ? 9 : -9, duration: 3.2 + (i % 4) * 0.5, ease: "sine.inOut", yoyo: true, repeat: -1, delay: (i % 5) * 0.3 });
  });

  // galerías: entrada escalonada con ligera inclinación (se suma al revelado por máscara)
  scope.querySelectorAll(".g-free, .g-still, .g-pol, .g-poster, .f-cell").forEach((el, i) => {
    const x = parseFloat(getComputedStyle(el).getPropertyValue("--x")) || (i % 3) * 480;
    const rot = ((i * 37) % 7 - 3) * 0.55;
    gsap.fromTo(el, { y: 70, rotation: rot, scale: 0.96 }, { y: 0, rotation: 0, scale: 1, duration: 1.3, ease: "power3.out", delay: Math.min(0.35, (x / 1440) * 0.3), clearProps: "transform", scrollTrigger: mkST(el, { start: "top 92%" }) });
  });

  // inclinación sutil 3D al pasar el cursor por fotos y polaroids
  if (finePointer) {
    scope.querySelectorAll(".g-free, .g-still, .g-pol, .g-poster, .g-destino").forEach((el) => {
      const set = gsap.quickTo(el, "rotationY", { duration: 0.6, ease: "power3.out" });
      const setX = gsap.quickTo(el, "rotationX", { duration: 0.6, ease: "power3.out" });
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        gsap.set(el, { transformPerspective: 1000 });
        set(((e.clientX - r.left) / r.width - 0.5) * 7); setX(-((e.clientY - r.top) / r.height - 0.5) * 7);
      });
      el.addEventListener("pointerleave", () => { set(0); setX(0); });
    });
  }

  // portada: el título se aleja suavemente al salir de pantalla
  scope.querySelectorAll("#inicio .tt:first-of-type, .f-hero-art").forEach((el) => {
    gsap.to(el, { yPercent: -10, scale: 0.97, ease: "none", scrollTrigger: { trigger: el, start: "top top", end: "bottom top", scrub: 0.6 } });
  });
}

/* hero: entrada inicial */
function heroIntro(scope) {
  const first = scope.querySelectorAll("#inicio .spr, .f-portfolio");
  const intro = scope.querySelector(".f-intro, .a .t20.right");
  gsap.set(first, { autoAlpha: 1 });
  gsap.timeline({ defaults: { ease: "power3.out" } })
    .fromTo(first, { clipPath: "inset(0 100% 0 0)", x: -40 }, { clipPath: "inset(0 0% 0 0)", x: 0, duration: 1.5, ease: "power3.inOut" }, 0.15)
    .fromTo(scope.querySelectorAll(".d-year, .f-year"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 1.2 }, 0.5);
}

/* ------------------------------------------------------------------ montaje */
let mm;
function mount() {
  mm && mm.revert();
  ScrollTrigger.getAll().forEach((t) => t.kill());
  mm = gsap.matchMedia();
  const initFor = (scopeSel) => {
    const scope = document.querySelector(scopeSel);
    wireSocial(scope);
    if (reduce) { setupSpy(); return; }
    setupAnimations(scope);
    setupSpy();
    heroIntro(scope);
  };
  mm.add("(min-width: 1000px)", () => { initFor("#stage"); });
  mm.add("(max-width: 999.98px)", () => { initFor("#flow"); });
  ScrollTrigger.refresh();
}
const start = () => { mount(); root.classList.add("ready"); };
if (document.fonts && document.fonts.ready) document.fonts.ready.then(start); else start();
// recalcular al cargar imágenes diferidas
window.addEventListener("load", () => ScrollTrigger.refresh());
// al cruzar el punto de corte entre escritorio y móvil
desktopMQ.addEventListener("change", () => { setUnit(); mount(); });

// enlace profundo (#seccion)
if (location.hash) {
  const key = location.hash.slice(1);
  window.addEventListener("load", () => setTimeout(() => { const el = anchorFor(key); el && scrollToEl(el); }, 400));
}

/* si una imagen falla al cargar (red inestable), se reintenta una vez */
document.addEventListener("error", (e) => {
  const im = e.target;
  if (im && im.tagName === "IMG" && !im.dataset.retry) {
    im.dataset.retry = "1";
    const u = im.getAttribute("src");
    setTimeout(() => { im.loading = "eager"; im.src = u + (u.includes("?") ? "&" : "?") + "r=1"; }, 600);
  }
}, true);
