"""Genera site/index.html a partir de layout.json (posiciones reales extraídas del PDF).

Dos composiciones con el mismo contenido:
  - #stage : escritorio. Cada pieza se coloca con las coordenadas exactas del PDF (px de diseño, 1440 de ancho).
  - #flow  : tablet / móvil. Recomposición vertical con los mismos recursos y textos reales.
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(ROOT, "raw", "layout.json")))
SP = json.load(open(os.path.join(ROOT, "tools", "sprites.json")))
img = lambda f: "/img/" + f.replace(".png", ".webp")
SIZES = {o["file"]: o["size"] for o in L}


def box(x, y, w, h):
    return f"--x:{x:.1f};--y:{y:.1f};--w:{w:.1f};--h:{h:.1f}"


def pl(i):
    o = L[i]
    x0, y0, x1, y1 = o["bbox"]
    return o["file"], x0, y0, x1 - x0, y1 - y0


# ---------------------------------------------------------------- textos
def lns(lines, last_left=True):
    """Líneas del PDF: en escritorio cada una ocupa su renglón (justificado como en el original)."""
    out = []
    for i, t in enumerate(lines):
        cls = "ln e" if (i == len(lines) - 1 and last_left) else "ln"
        out.append(f'<span class="{cls}">{t}</span>')
    return " ".join(out)


B = lambda t: f"<b>{t}</b>"

INTRO = ["Soy Juan Ruiz, también conocido", "como yeezy. Ilustro, dibujo y diseño", "porque me encanta darle forma a", "las ideas."]
BIO1 = ["Buena! Soy estudiante de Diseño Digital, un creativo curioso al", "que le gusta experimentar, explorar ideas y convertirlas en algo", "visual. Me mueve la innovación, el arte, la tecnología y todo", "aquello que tenga una identidad propia."]
BIO2 = ["Disfruto especialmente del diseño de marcas, la creación de", "conceptos, la composición visual y la exploración de diferentes", "estilos. Me gusta jugar con las ideas, salir de lo convencional y", "encontrar ese detalle que hace que un proyecto sea diferente."]
BULLETS = [
    "Creatividad para generar ideas y conceptos originales.",
    "Innovación y curiosidad para explorar nuevas posibilidades.",
    "Buen sentido estético y atención al detalle.",
    "Habilidad para el dibujo y la expresión visual.",
    "Eficacia para desarrollar ideas y convertirlas en propuestas.",
    "Capacidad para experimentar sin perder de vista el propósito del diseño.",
]
BLURB_TRABAJO = f"{B('Ideas')} que se convierten {B('en proyectos')}. Una selección de trabajos {B('freelance, proyectos creativos y experiencias')} académicas donde exploro, experimento y pongo {B('a prueba mis ideas')} a través del diseño."
DIFERENTES = ["Diferentes procesos.", "Diferentes perspectivas.", "Una misma pasión por crear."]
MARIPOSAS = [
    f"{B('Las mariposas')} son el {B('punto de partida')} de muchas {B('de mis ilustraciones')}.",
    f"Me inspiran por su forma, delicadeza y simbolismo: {B('cada trazo')} es una",
    f"manera de {B('explorar la transformación, la libertad y la creatividad.')}",
]
NACIO = [
    f"{B('Nació en clase')}, como un {B('ejercicio')}", f"{B('para construir una historia')} con un", "giro inesperado. De tantas ideas que",
    "surgieron en el equipo, esta fue la", "que más nos atrapó, todos", "compartíamos el gusto por el thriller",
    "y por esas narrativas de persecución", "que no te dejan soltar la pantalla.", f"Quisimos {B('que el espectador entrara')}",
    f"{B('con intriga')}, se perdiera un poco en la", "confusión de lo que está pasando, y", f"saliera sorprendido con el final. {B('Fue')}",
    B("un proyecto universitario hecho con"), f"{B('recursos muy limitados')}, pero con {B('la')}", f"{B('intención')} de aplicar todo lo",
    "aprendido, fotografía, guion,", f"narrativa, composición, sonido, {B('para')}", B("construir una pieza que realmente"),
    B("se sintiera atractiva de ver."),
]
CAPITAL = [
    f"Es un ensayo fotográfico que explora {B('los')}", B("monumentos de Bogotá y su relación con"),
    f"{B('la historia, la cultura y la sociedad.')} A través", "de diferentes fotografías, buscamos", "mostrar cómo estas construcciones",
    "representan recuerdos, acontecimientos y", f"personajes importantes, {B('además de')}", B("transmitir emociones y generar distintas"),
    f"{B('percepciones en quienes las observan.')} El", "proyecto invita a reflexionar sobre su", "significado y el papel que desempeñan en",
    "la memoria colectiva de la ciudad.", "o con el final. Fue un proyecto universitario", "hecho con recursos muy limitados, pero",
    "con la intención de aplicar todo lo", "aprendido, fotografía, guion, narrativa,", "composición, sonido, para construir una",
    "pieza que realmente se sintiera atractiva de", "ver.",
]
PRINTS_A = ["Una selección de piezas gráficas que destacan por su estética", "minimalista y claridad visual. Aunque hacen parte de un universo", "creativo mucho más amplio, estos trabajos representan mi", "manera de explorar la comunicación visual."]
PRINTS_B = ["Detrás de algunas de estas piezas también hay análisis de medios,", "estrategias de marketing y decisiones pensadas para conectar", "con el público."]
PRINTS_C = [B("No se trata solo de diseñar, sino de entender qué queremos"), B("comunicar y cómo hacerlo.")]
CIERRE_1 = ["Detrás de cada proyecto hay una idea, una intención y muchas", "ganas de crear. Este portafolio reúne una parte de lo que soy, de", "lo que me gusta y de todo lo que he aprendido a través del", "diseño."]
CIERRE_2 = [f"{B('Soy Juan Diego')}, también conocido como {B('Yeezy')}. Me gusta", "experimentar, explorar nuevas posibilidades y convertir ideas en", "algo tangible. Todavía tengo mucho por aprender, imaginar y", "construir, y precisamente ahí está lo interesante de este camino."]
CIERRE_3 = [B("Esto es lo que soy hoy, pero no todo lo que puedo"), B("llegar a crear, creemos juntos.")]
EMAIL = "judruizro7d@gmail.com"

ALT = {
    "p1_x37": "Patrón ilustrado en blanco y negro mostrado en una pantalla", "p1_x38": "Ilustración de una mariposa en blanco y negro",
    "p1_x39": "Ilustración de una flor en blanco y negro sobre fondo negro", "p1_x40": "Tableta mostrando una ilustración de flor, en un cuarto oscuro",
    "p1_x41": "Tableta gráfica con una ilustración de mariposa durante el proceso", "p1_x42": "Tableta con una mariposa roja ilustrada",
    "p1_x43": "Ilustración de una mariposa roja", "p1_x44": "Ilustración de una mariposa con flores en blanco y negro",
    "p1_x45": "Ilustración de flores y una mariposa en blanco y negro", "p1_x284": "Afiche de Destino sin retorno",
    "p2_x92": "Afiche para Levi's", "p2_x93": "Afiche WildGreen", "p2_x94": "Afiche LOLA RENNT", "p2_x614": "Afiche para Nike",
}
STILLS = ["p1_x30", "p1_x31", "p1_x32", "p1_x33", "p1_x288", "p1_x35", "p1_x36"]
for k, f in enumerate(STILLS, 1):
    ALT[f] = f"Fotograma del rodaje de Destino sin retorno ({k} de 7)"
CAP = ["p2_x376", "p2_x382", "p2_x387", "p2_x392", "p2_x398", "p2_x403"]
for k, f in enumerate(CAP, 1):
    ALT[f] = f"Fotografía en blanco y negro de un monumento de Bogotá ({k} de 6)"


def photo(f, cls="", extra="", group="", lazy=True, style="", frame=None):
    w, h = SIZES[f + ".png"]
    alt = html.escape(ALT.get(f, ""))
    src = f"/img/{f}.webp"
    inner = f'<img src="{src}" alt="{alt}" width="{w}" height="{h}" {"loading=lazy " if lazy else ""}decoding="async" draggable="false">'
    if group:
        return (f'<button type="button" class="ph {cls}" data-lb="{group}" data-src="{src}" data-alt="{alt}" aria-label="Ampliar imagen: {alt}" style="{style}" {extra}>{inner}</button>')
    return f'<div class="ph static {cls}" style="{style}" {extra}>{inner}</div>'


def decor(f, o=None, cls="", extra="", style="", lazy=True):
    w, h = SIZES[f + ".png"]
    op = f"opacity:{o};" if o is not None else ""
    return f'<img class="dec {cls}" src="/img/{f}.webp" alt="" width="{w}" height="{h}" {"loading=lazy " if lazy else ""}decoding="async" aria-hidden="true" style="{op}{style}" {extra}>'


def spr(name, alt="", cls="", extra="", lazy=True, style=""):
    d = SP[name + ".webp"] if name + ".webp" in SP else None
    w, h = (d["w"], d["h"]) if d else (0, 0)
    return f'<img class="spr {cls}" src="/img/{name}.webp" alt="{html.escape(alt)}" width="{w}" height="{h}" {"loading=lazy " if lazy else ""}decoding="async" style="{style}" {extra}>'


# ---------------------------------------------------------------- ESCRITORIO
def A(x, y, w, h, inner, cls="", extra=""):
    return f'<div class="a {cls}" style="{box(x, y, w, h)}" {extra}>{inner}</div>'


def desktop():
    P1, P2 = [], []
    # --- página 1: fondos y decoración (en orden de apilado del PDF)
    f, x, y, w, h = pl(0); P1.append(A(x, y, w, h, decor("p1_x538", 0.15, lazy=False), "d-year", 'data-r="fade"'))
    for i in (1, 2):
        f, x, y, w, h = pl(i); P1.append(A(x, y, w, h, decor("p1_x265", 0.10), "bg"))
    f, x, y, w, h = pl(3); P1.append(A(x, y, w, h, decor("p1_x22"), "d-plant", 'data-p="-0.06"'))
    f, x, y, w, h = pl(4); P1.append(A(x, y, w, h, decor("p1_x63", None), "d-dice", 'data-p="0.05" data-rot="-3"'))
    f, x, y, w, h = pl(5); P1.append(A(x, y, w, h, decor("p1_x24", 0.22), "d-rays", 'data-r="fade"'))
    f, x, y, w, h = pl(6); P1.append(A(x, y, w, h, decor("p1_x28"), "d-burst1", 'data-p="-0.05"'))
    # póster y fotogramas
    f, x, y, w, h = pl(7); P1.append(A(x, y, w, h, photo("p1_x284", group="destino"), "g-destino", 'data-r="mask"'))
    for k, i in enumerate(range(8, 15)):
        f, x, y, w, h = pl(i)
        P1.append(A(x, y, w, h, photo(f[:-4], group="stills"), "g-still", 'data-r="mask"'))
    # galería de mariposas / proceso
    for i in range(15, 24):
        f, x, y, w, h = pl(i)
        P1.append(A(x, y, w, h, photo(f[:-4], group="freelance"), "g-free", 'data-r="mask"'))
    f, x, y, w, h = pl(24); P1.append(A(x, y, w, h, decor("p1_x47"), "d-spike", 'data-p="0.04"'))
    f, x, y, w, h = pl(25); P1.append(A(x, y, w, h, decor("p1_x48", lazy=False), "d-portrait", 'data-r="portrait"'))
    f, x, y, w, h = pl(26); P1.append(A(x, y, w, h, decor("p1_x62"), "d-splat", 'data-p="0.04"'))
    f, x, y, w, h = pl(27); P1.append(A(x, y, w, h, decor("p1_x63"), "d-dice r", 'data-p="-0.05" data-rot="4"'))
    # títulos (sprites) de la página 1
    for k, alt, r in (("portfolio", "Portfolio · Yeezy", "title"), ("nombre", "Juan Diego “Yeezy” Ruiz Rodríguez", "title"), ("anos", "21 años", "title"),
                      ("estudios", "Estudios", "title"), ("skills", "Skills · habilidades: Photoshop, Illustrator, Figma — 4 de 5 estrellas", "title"),
                      ("aporto", "¿Qué aporto para el diseño?", "title"), ("trabajo", "Mi trabajo — Freelance, Creativo, Proyectos Educativos", "title"),
                      ("freelance", "Freelance", "title"), ("educativos", "Proyectos educativos", "title")):
        d = SP[f"s-{k}.webp"]
        P1.append(A(d["x"], d["y"], d["w"], d["h"], spr(f"s-{k}", alt, "", "", lazy=(k != "portfolio")), "tt", f'data-r="{r}"'))
    # capa vectorial restante (formas, viñetas, estrellas) por tiras
    for n in range(4):
        s = SP[f"vec-p1-{n}.webp"]
        P1.append(f'<img class="vec" src="/img/vec-p1-{n}.webp" alt="" width="{s["w"]}" height="{s["h"]}" decoding="async" aria-hidden="true" style="{box(s["x"], s["y"], s["w"], s["h"])}">')
    # textos reales
    T = []
    T.append(A(895, 491, 354, 118, f'<p class="t t20 right" data-r="lines">{lns(INTRO, False)}</p>'))
    T.append(A(227, 1056, 652, 230, f'<p class="t t20 just" data-r="lines">{lns(BIO1)}</p><p class="t t20 just p2" data-r="lines">{lns(BIO2)}</p>', "bio"))
    est = ('<p class="t t17 b">Primaria y Bachillerato:</p><p class="t t17">Título de bachiller técnico comercial&nbsp; con enfoque en<br>diseño gráfico</p>'
           '<p class="t t17 b">Gimnasio Academico Regional&nbsp; 2012 / 2023</p><p class="t t17 b gap">Universidad Sergio Arboleda:</p>'
           '<p class="t t17">Diseño Digital con énfasis en creación de contenidos</p><p class="t t17 b">2023/2027</p>')
    T.append(A(234, 1406, 470, 190, est, "est", 'data-r="up"'))
    bl = BULLETS[:5] + [lns(["Capacidad para experimentar sin perder de vista el", "propósito del diseño."])]
    items = "".join(f"<li>{t}</li>" for t in bl)
    T.append(A(508, 1766.3, 456, 176, f'<ul class="t t17 bl" data-r="lines">{items}</ul>', "bul"))
    T.append(A(500, 2482.4, 440, 140, "".join(f'<p class="t t33 b center"><span class="ln">{t}</span></p>' for t in DIFERENTES), "dif", 'data-r="up"'))
    T.append(A(397, 3873, 646, 90, f'<p class="t t20 center" data-r="lines">{lns(MARIPOSAS, False)}</p>'))
    T.append(A(140, 4370.2, 517, 725, f'<p class="t t31 just" data-r="lines">{lns(NACIO)}</p>', "nacio"))
    T.append(A(149, 5120, 500, 80, '<p class="t destino"><span class="k">DESTINO</span> <span class="r">SIN RETORNO</span></p>', "dst", 'data-r="up"'))
    # --- sección 'trabajo': texto accesible del bloque horneado + etiquetas
    T.append(A(285, 2280, 450, 90, f'<p class="sr">{BLURB_TRABAJO}</p>'))
    page1 = "\n".join(P1 + T)

    # --- página 2
    f, x, y, w, h = pl(28); P2.append(A(x, y, w, h, decor("p2_x371", 0.10), "bg"))
    f, x, y, w, h = pl(29); P2.append(A(x, y, w, h, decor("p2_x76"), "d-burst2", 'data-p="0.05"'))
    # polaroids: ventana = marco
    frames = [(31, 30), (33, 32), (35, 34), (37, 36), (40, 39), (42, 41)]
    order = [(30, 31), (32, 33), (34, 35), (36, 37)]
    def polaroid(ph_i, fr_i, k):
        pf, px, py, pw, ph = pl(ph_i)
        ff, fx, fy, fw, fh = pl(fr_i)
        w_, h_ = SIZES[pf]
        alt = html.escape(ALT[pf[:-4]])
        src = f"/img/{pf[:-4]}.webp"
        st = f"left:{(px - fx) / fw * 100:.3f}%;top:{(py - fy) / fh * 100:.3f}%;width:{pw / fw * 100:.3f}%;height:{ph / fh * 100:.3f}%"
        return A(fx, fy, fw, fh,
                 f'<button type="button" class="pol" data-lb="capital" data-src="{src}" data-alt="{alt}" aria-label="Ampliar imagen: {alt}"><span class="win"><img src="{src}" alt="{alt}" width="{w_}" height="{h_}" loading="lazy" decoding="async" draggable="false" style="{st}"></span><img class="frm" src="/img/p2_x379.webp" alt="" width="491" height="520" loading="lazy" decoding="async" aria-hidden="true"></button>',
                 "g-pol", 'data-r="mask"')
    for k, (a, b) in enumerate(order): P2.append(polaroid(a, b, k))
    f, x, y, w, h = pl(38); P2.append(A(x, y, w, h, decor("p2_x85"), "d-flower", 'data-p="0.05"'))
    P2.append(polaroid(39, 40, 4))
    P2.append(polaroid(41, 42, 5))
    f, x, y, w, h = pl(43); P2.append(A(x, y, w, h, decor("p2_x371", 0.10), "bg"))
    f, x, y, w, h = pl(44); P2.append(A(x, y, w, h, decor("p2_x91"), "d-redflower", 'data-p="-0.05"'))
    for i, f_ in ((47, "p2_x94"), (45, "p2_x92"), (46, "p2_x93"), (48, "p2_x614")):
        f, x, y, w, h = pl(i); P2.append(A(x, y, w, h, photo(f_, group="posters"), "g-poster", 'data-r="mask"'))
    f, x, y, w, h = pl(49); P2.append(A(x, y, w, h, decor("p2_x96"), "d-bottom"))
    f, x, y, w, h = pl(50); P2.append(A(x, y, w, h, decor("p2_x98", lazy=False), "d-camera", 'data-p="0.04" data-rot="-2"'))
    f, x, y, w, h = pl(51); P2.append(A(x, y, w, h, decor("p2_x109"), "d-pin", 'data-rot="6"'))
    P2.append(A(0, 4006, 1440, 468.5, '', 'band'))  # banda roja de fondo: evita costuras entre la capa vectorial y los sprites
    for k, alt, r in (("prints", "Prints — posters", "title"), ("herramientas", "Photoshop, Illustrator, Figma, Canva Pro", "fade"), ("gracias", "Gracias · atte: Yeezy", "title"), ("iconos", "Instagram y LinkedIn", "fade")):
        d = SP[f"s-{k}.webp"]
        P2.append(A(d["x"], d["y"], d["w"], d["h"], spr(f"s-{k}", alt), "tt", f'data-r="{r}"'))
    for n in range(4):
        s = SP[f"vec-p2-{n}.webp"]
        P2.append(f'<img class="vec" src="/img/vec-p2-{n}.webp" alt="" width="{s["w"]}" height="{s["h"]}" loading="lazy" decoding="async" aria-hidden="true" style="{box(s["x"], s["y"], s["w"], s["h"])}">')
    T2 = []
    T2.append(A(912, 610.4, 448, 540, f'<p class="t t23 just" data-r="lines">{lns(CAPITAL)}</p>'))
    T2.append(A(92, 275, 172, 890, '<h2 class="cap-title"><span>LA CAPITAL:</span><span>UN MUNDO DE VARIAS MEMORIAS</span></h2>', "", 'data-r="fade"'))
    T2.append(A(762, 1600.6, 478, 205, f'<p class="t t16 just" data-r="lines">{lns(PRINTS_A)}</p><p class="t t16 just" data-r="lines">{lns(PRINTS_B)}</p><p class="t t16 gap3" data-r="lines">{lns(PRINTS_C, False)}</p>', "prb"))
    T2.append(A(665, 1830, 510, 48, '<p class="sr">Photoshop, Illustrator, Figma, Canva Pro</p>'))
    T2.append(A(201, 3011.6, 971, 175, f'<p class="t t34 just" data-r="lines">{lns(CIERRE_1)}</p>', "c1"))
    T2.append(A(206, 3228.6, 961, 175, f'<p class="t t34 just" data-r="lines">{lns(CIERRE_2)}</p>', "c2"))
    T2.append(A(216, 3486, 939, 125, f'<p class="t t43 center" data-r="up">{lns(CIERRE_3, False)}</p>', "c3"))
    T2.append(A(509, 4211, 460, 72, f'<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>', "mailbox"))
    page2 = "\n".join(P2 + T2)
    return f'''
<main id="stage" class="stage" aria-label="Portafolio de Juan Diego Ruiz Rodríguez">
  <section id="inicio" class="page p1" style="--H:6000">
    <h1 class="sr">Portfolio 2026 · Juan Diego Ruiz Rodríguez “Yeezy”</h1>
    <div class="anchor" id="sobre-mi" style="--y:860"></div><div class="anchor" id="estudios" style="--y:1330"></div>
    <div class="anchor" id="aporto" style="--y:1670"></div><div class="anchor" id="trabajo" style="--y:2020"></div>
    <div class="anchor" id="freelance" style="--y:2660"></div><div class="anchor" id="educativos" style="--y:3990"></div>
    {page1}
  </section>
  <section id="capital" class="page p2" style="--H:4875">
    <div class="anchor" id="prints" style="--y:1380"></div><div class="anchor" id="contacto" style="--y:3830"></div>
    {page2}
  </section>
</main>'''


# ---------------------------------------------------------------- TABLET / MÓVIL
def flow():
    s = []
    # HERO
    s.append(f'''
<section class="f-sec f-hero" id="m-inicio">
  <div class="f-hero-art">{spr("s-portfolio", "Portfolio · Yeezy", "f-portfolio", 'data-r="title"', lazy=False)}
    {decor("p1_x538", 0.15, "f-year", lazy=False)}</div>
  <p class="t f-intro right" data-r="up">{" ".join(INTRO)}</p>
  {decor("p1_x63", None, "f-dice f-dice-r", 'data-p="-0.04"', lazy=False)}
</section>''')
    # SOBRE MÍ
    s.append(f'''
<section class="f-sec f-about" id="m-sobre-mi">
  {decor("p1_x62", None, "f-splat")}
  {decor("p1_x22", None, "f-plant", 'data-p="-0.04"')}
  <div class="f-portrait-wrap">{decor("p1_x48", None, "f-portrait", 'data-r="portrait"', lazy=False)}{spr("s-anos", "21 años", "f-anos", 'data-r="title"')}</div>
  {spr("s-nombre", "Juan Diego “Yeezy” Ruiz Rodríguez", "f-nombre", 'data-r="title"')}
  <div class="f-text" data-r="up"><p class="t">{" ".join(BIO1)}</p><p class="t">{" ".join(BIO2)}</p></div>
</section>''')
    # ESTUDIOS + SKILLS
    s.append(f'''
<section class="f-sec f-est" id="m-estudios">
  {spr("s-estudios", "Estudios", "f-estudios", 'data-r="title"')}
  <div class="f-text" data-r="up">
    <p class="t b">Primaria y Bachillerato:</p><p class="t">Título de bachiller técnico comercial con enfoque en diseño gráfico</p>
    <p class="t b">Gimnasio Academico Regional 2012 / 2023</p>
    <p class="t b gap">Universidad Sergio Arboleda:</p><p class="t">Diseño Digital con énfasis en creación de contenidos</p><p class="t b">2023/2027</p>
  </div>
  {spr("s-skills", "Skills · habilidades: Photoshop, Illustrator, Figma — 4 de 5 estrellas", "f-skills", 'data-r="title"')}
</section>''')
    items = "".join(f"<li>{t}</li>" for t in BULLETS)
    s.append(f'''
<section class="f-sec f-aporto" id="m-aporto">
  {spr("s-aporto", "¿Qué aporto para el diseño?", "f-aporto-t", 'data-r="title"')}
  <ul class="t f-bullets" data-r="lines">{items}</ul>
</section>''')
    # TRABAJO + FREELANCE
    free = list(range(15, 24))
    gal = "".join(f'<div class="f-cell" data-r="mask">{photo(L[i]["file"][:-4], group="m-freelance")}</div>' for i in free)
    s.append(f'''
<section class="f-sec f-trabajo" id="m-trabajo">
  {decor("p1_x24", 0.22, "f-rays")}
  {spr("s-trabajo-m", "Mi trabajo — Freelance, Creativo, Proyectos Educativos", "f-trabajo-t", 'data-r="title"')}
  <p class="t f-blurb" data-r="up">{BLURB_TRABAJO}</p>
  <div class="t f-dif" data-r="up">{"".join(f"<p>{t}</p>" for t in DIFERENTES)}</div>
</section>
<section class="f-sec f-free" id="m-freelance">
  {spr("s-freelance", "Freelance", "f-free-t", 'data-r="title"')}
  <div class="f-masonry">{gal}</div>
  <p class="t f-mar center" data-r="up">{" ".join(MARIPOSAS)}</p>
</section>''')
    # EDUCATIVOS
    stills = "".join(f'<div class="f-cell" data-r="mask">{photo(f, group="m-stills")}</div>' for f in STILLS)
    s.append(f'''
<section class="f-sec f-edu" id="m-educativos">
  {spr("s-educativos", "Proyectos educativos", "f-edu-t", 'data-r="title"')}
  <div class="f-poster" data-r="mask">{photo("p1_x284", group="m-destino")}</div>
  <p class="t f-nacio just" data-r="up">{" ".join(NACIO)}</p>
  <p class="t destino f-destino" data-r="up"><span class="k">DESTINO</span> <span class="r">SIN RETORNO</span></p>
  <div class="f-grid2">{stills}</div>
  {decor("p1_x28", None, "f-burst")}
</section>''')
    # LA CAPITAL
    def mpol(ph_i, fr_i):
        pf, px, py, pw, ph = pl(ph_i); ff, fx, fy, fw, fh = pl(fr_i)
        w_, h_ = SIZES[pf]; alt = html.escape(ALT[pf[:-4]]); src = f"/img/{pf[:-4]}.webp"
        st = f"left:{(px - fx) / fw * 100:.3f}%;top:{(py - fy) / fh * 100:.3f}%;width:{pw / fw * 100:.3f}%;height:{ph / fh * 100:.3f}%"
        return (f'<div class="f-cell" data-r="mask"><button type="button" class="pol" data-lb="m-capital" data-src="{src}" data-alt="{alt}" aria-label="Ampliar imagen: {alt}"><span class="win"><img src="{src}" alt="{alt}" width="{w_}" height="{h_}" loading="lazy" decoding="async" draggable="false" style="{st}"></span>'
                '<img class="frm" src="/img/p2_x379.webp" alt="" width="491" height="520" loading="lazy" decoding="async" aria-hidden="true"></button></div>')
    pols = "".join(mpol(a, b) for a, b in [(30, 31), (32, 33), (34, 35), (36, 37), (39, 40), (41, 42)])
    s.append(f'''
<section class="f-sec f-cap" id="m-capital">
  {decor("p2_x98", None, "f-camera", 'data-p="-0.03"')}
  <h2 class="f-cap-title" data-r="up">LA CAPITAL:<br>UN MUNDO DE VARIAS MEMORIAS</h2>
  <div class="f-grid2 pols">{pols}</div>
  <p class="t f-cap-p" data-r="up">{" ".join(CAPITAL)}</p>
</section>''')
    # PRINTS
    posters = "".join(f'<div class="f-cell" data-r="mask">{photo(f, group="m-posters")}</div>' for f in ("p2_x94", "p2_x92", "p2_x93"))
    nk = SP["s-nike.webp"]
    pf, px, py, pw, ph = pl(48)
    nike = (f'<div class="f-nike" data-r="mask" style="aspect-ratio:{nk["w"]}/{nk["h"]}"><button type="button" class="ph nk" data-lb="m-posters" data-src="/img/p2_x614.webp" data-alt="Afiche para Nike" aria-label="Ampliar imagen: Afiche para Nike" '
            f'style="left:{(px - nk["x"]) / nk["w"] * 100:.3f}%;top:{(py - nk["y"]) / nk["h"] * 100:.3f}%;width:{pw / nk["w"] * 100:.3f}%;height:{ph / nk["h"] * 100:.3f}%"><img src="/img/p2_x614.webp" alt="Afiche para Nike" width="512" height="640" loading="lazy" decoding="async" draggable="false"></button>'
            f'{spr("s-nike", "", "nkspr")}</div>')
    s.append(f'''
<section class="f-sec f-prints" id="m-prints">
  {decor("p2_x91", 0.13, "f-redflower")}
  {spr("s-prints", "Prints — posters", "f-prints-t", 'data-r="title"')}
  <div class="f-prb" data-r="up"><p class="t">{" ".join(PRINTS_A)}</p><p class="t">{" ".join(PRINTS_B)}</p><p class="t b">{" ".join(PRINTS_C)}</p></div>
  {spr("s-herramientas", "Photoshop, Illustrator, Figma, Canva Pro", "f-tools", 'data-r="up"')}
  <div class="f-grid2 posts">{posters}</div>
  {nike}
</section>''')
    # CIERRE
    s.append(f'''
<section class="f-sec f-close" id="m-contacto">
  <p class="t f-c1" data-r="up">{" ".join(CIERRE_1)}</p>
  <p class="t f-c1" data-r="up">{" ".join(CIERRE_2)}</p>
  <p class="t f-c3 center" data-r="up">{" ".join(CIERRE_3)}</p>
  <div class="f-icons">{spr("s-iconos", "Instagram y LinkedIn", "f-icons-s", 'data-r="up"')}</div>
  <div class="f-gracias">{spr("s-gracias", "Gracias · atte: Yeezy", "f-gracias-s", 'data-r="title"')}{decor("p2_x109", None, "f-pin")}</div>
  <div class="f-band"><a class="mail f-mail" href="mailto:{EMAIL}"><span class="envelope" aria-hidden="true">{spr("s-sobre", "", "", "")}</span><span>{EMAIL}</span></a></div>
  <div class="f-foot">{decor("p2_x96", None, "", "", "", True)}</div>
</section>''')
    return f'<main id="flow" class="flow" aria-label="Portafolio de Juan Diego Ruiz Rodríguez">\n<h1 class="sr">Portfolio 2026 · Juan Diego Ruiz Rodríguez “Yeezy”</h1>\n' + "\n".join(s) + "\n</main>"


NAV = [("inicio", "Inicio"), ("sobre-mi", "Sobre mí"), ("estudios", "Estudios"), ("trabajo", "Trabajo"), ("educativos", "Proyectos"), ("capital", "La Capital"), ("prints", "Prints"), ("contacto", "Contacto")]


def nav():
    links = "".join(f'<li><a href="#{k}" data-nav="{k}">{v}</a></li>' for k, v in NAV)
    return f'''
<header class="nav" id="nav">
  <a class="brand" href="#inicio" data-nav="inicio" aria-label="Ir al inicio">Yeezy</a>
  <button class="burger" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú"><span></span><span></span></button>
  <nav id="menu" class="menu" aria-label="Principal"><ul>{links}</ul></nav>
</header>
<div class="progress" aria-hidden="true"><i id="progress"></i></div>
<div class="cursor" id="cursor" aria-hidden="true"><span></span></div>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Visor de imágenes" hidden>
  <button class="lb-x" id="lb-x" aria-label="Cerrar">×</button>
  <button class="lb-p" id="lb-p" aria-label="Anterior">‹</button>
  <figure><img id="lb-img" alt=""><figcaption id="lb-cap"></figcaption></figure>
  <button class="lb-n" id="lb-n" aria-label="Siguiente">›</button>
  <div class="lb-c" id="lb-c" aria-live="polite"></div>
</div>'''


PAGE = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Juan Ruiz “Yeezy” · Portfolio 2026 — Diseño digital, ilustración y proyectos creativos</title>
<meta name="description" content="Portafolio 2026 de Juan Diego Ruiz Rodríguez “Yeezy”, estudiante de Diseño Digital: ilustración, freelance, proyectos educativos y piezas gráficas.">
<meta name="author" content="Juan Diego Ruiz Rodríguez">
<meta name="theme-color" content="#b40000">
<link rel="canonical" href="/">
<meta property="og:type" content="website">
<meta property="og:title" content="Juan Ruiz “Yeezy” · Portfolio 2026">
<meta property="og:description" content="Ilustro, dibujo y diseño porque me encanta darle forma a las ideas.">
<meta property="og:image" content="/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" as="image" href="/img/s-portfolio.webp">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Person","name":"Juan Diego Ruiz Rodríguez","alternateName":"Yeezy","jobTitle":"Estudiante de Diseño Digital","email":"mailto:{EMAIL}","alumniOf":{{"@type":"CollegeOrUniversity","name":"Universidad Sergio Arboleda"}}}}</script>
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
{nav()}
<div id="contenido" tabindex="-1">
{desktop()}
{flow()}
</div>
<noscript><style>[data-r]{{opacity:1!important}}</style></noscript>
<script type="module" src="/src/main.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, "site", "index.html"), "w").write(PAGE)
print("index.html", len(PAGE), "bytes")
