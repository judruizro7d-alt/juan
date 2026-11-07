"""Genera los assets del sitio a partir del PDF original.
- Imágenes embebidas -> WebP (con su máscara alfa)
- Capa vectorial (tipografías de título, stickers, iconos) -> sprites WebP @2x
Uso: python3 tools/build_assets.py
"""
import json, os, pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "..", "PortFolio Juan Ruiz.pdf")
OUT = os.path.join(ROOT, "site", "public", "img")
RAW = os.path.join(ROOT, "raw")
os.makedirs(OUT, exist_ok=True)
S = 2  # factor de render de la capa vectorial

# 1) imágenes embebidas -> webp
layout = json.load(open(os.path.join(RAW, "layout.json")))
for f in sorted({o["file"] for o in layout}):
    im = Image.open(os.path.join(RAW, f))
    has_a = im.mode == "RGBA"
    q = 80 if f.startswith(("p1_x265", "p2_x371", "p2_x96")) else 86
    im.save(os.path.join(OUT, f.replace(".png", ".webp")), "WEBP", quality=q, method=6, alpha_quality=100 if has_a else 100)

# 2) zonas de texto real (se borran de la capa vectorial); coordenadas = px de diseño
CLEAR = {
 0: [(895,488,1255,610),(222,1050,885,1285),(228,1404,700,1590),(503,1762,970,1936),
     (500,2478,940,2622),(398,3868,1042,3960),(136,4362,662,5090),(145,5112,645,5188)],
 1: [(906,602,1366,1142),(92,275,266,1165),(758,1595,1245,1802),(196,3004,1178,3400),
     (214,3478,1160,3600),(505,4207,965,4274)],
}
# 3) sprites por componente (página, x0,y0,x1,y1)
COMP = {
 "portfolio":(0,170,225,1270,570), "nombre":(0,120,865,780,1060), "anos":(0,930,1120,1035,1225),
 "estudios":(0,220,1330,480,1412), "skills":(0,775,1335,1110,1665), "aporto":(0,470,1670,995,1755),
 "trabajo":(0,285,2020,1165,2375), "freelance":(0,515,3010,925,3285), "educativos":(0,180,3990,1265,4330),
 "prints":(1,215,1395,750,2200), "herramientas":(1,665,1828,1170,1876), "gracias":(1,230,3830,1190,4175),
 "iconos":(1,470,3590,960,3830), "sobre":(1,425,4200,510,4280),
 "trabajo-m":(0,285,2020,1165,2280), "nike":(1,600,2425,1145,2862),
}
sprites = {}
DESK = ["portfolio","nombre","anos","estudios","skills","aporto","trabajo","freelance","educativos","prints","gracias","iconos","herramientas"]
TOOLS = (665,1828,1170,1876)
for pn in (0, 1):
    cache = os.path.join(RAW, f"vec2x-p{pn+1}.png")
    if not os.path.exists(cache):
        import subprocess, sys
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        from vector_layer import clean_pdf
        tmp = os.path.join(RAW, "clean.pdf")
        if not os.path.exists(tmp): clean_pdf(PDF, tmp)
        subprocess.run(["pdftocairo","-png","-transp","-r",str(72*S),"-f",str(pn+1),"-l",str(pn+1),"-singlefile",tmp,cache[:-4]],check=True)
    base = Image.open(cache).convert("RGBA")
    clean = base.copy()
    for (x0,y0,x1,y1) in CLEAR[pn]:
        # el correo vive sobre la banda roja: se rellena con el rojo de la banda en vez de dejarlo transparente
        fill = (157,28,28,255) if (pn == 1 and y0 == 4207) else (0,0,0,0)
        clean.paste(fill, (x0*S, y0*S, x1*S, y1*S))
    strips_im = clean.copy()
    for k,(p,x0,y0,x1,y1) in COMP.items():
        if p != pn: continue
        src = clean
        if k == "prints":
            src = clean.copy(); src.paste((0,0,0,0), tuple(v*S for v in TOOLS))
        c = src.crop((x0*S,y0*S,x1*S,y1*S))
        name = f"s-{k}.webp"; c.save(os.path.join(OUT, name), "WEBP", quality=92, method=6, alpha_quality=100)
        sprites[name] = dict(page=pn+1, x=x0, y=y0, w=x1-x0, h=y1-y0)
        if k in DESK:
            strips_im.paste((0,0,0,0), (x0*S, y0*S, x1*S, y1*S))
    H = base.size[1] // S
    n = 0
    for y in range(0, H, 1500):
        h = min(1500, H - y)
        strip = strips_im.crop((0, y*S, 1440*S, (y+h)*S))
        name = f"vec-p{pn+1}-{n}.webp"; strip.save(os.path.join(OUT, name), "WEBP", quality=92, method=6, alpha_quality=100)
        sprites[name] = dict(page=pn+1, x=0, y=y, w=1440, h=h); n += 1
    print("page", pn+1, "height", H)
json.dump(sprites, open(os.path.join(ROOT, "tools", "sprites.json"), "w"), indent=1)
tot = sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT))
print(len(os.listdir(OUT)), "archivos,", round(tot/1e6,2), "MB")
