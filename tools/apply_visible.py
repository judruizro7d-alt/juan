"""Recorta las fotos a su zona visible real en el PDF (el PDF las recorta con máscaras de recorte)
y actualiza layout.json. Idempotente: parte de raw/orig/ y de raw/layout.orig.json."""
import json, os, shutil
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw"); ORIG = os.path.join(RAW, "orig"); os.makedirs(ORIG, exist_ok=True)
lj = os.path.join(RAW, "layout.json"); lo = os.path.join(RAW, "layout.orig.json")
if not os.path.exists(lo): shutil.copy(lj, lo)
L = json.load(open(lo)); V = json.load(open(os.path.join(ROOT, "tools", "visible.json")))
PHOTOS = set(range(7, 24)) | {45, 46, 47, 48}
n = 0
for k, v in V.items():
    i = int(k)
    if i not in PHOTOS or v is None: continue
    o = L[i]; x0, y0, x1, y1 = o["bbox"]
    if max(abs(v[0]-x0), abs(v[1]-y0), abs(v[2]-x1), abs(v[3]-y1)) <= 4: continue
    f = o["file"]; src = os.path.join(ORIG, f)
    if not os.path.exists(src): shutil.copy(os.path.join(RAW, f), src)
    im = Image.open(src); W, H = im.size
    sx, sy = W / (x1 - x0), H / (y1 - y0)
    box = tuple(max(0, min(m, round(c))) for c, m in zip(((v[0]-x0)*sx, (v[1]-y0)*sy, (v[2]-x0)*sx, (v[3]-y0)*sy), (W, H, W, H)))
    c = im.crop(box); c.save(os.path.join(RAW, f))
    o["bbox"] = [float(v[0]), float(v[1]), float(v[2]), float(v[3])]; o["size"] = list(c.size); n += 1
    print("recortada", i, f, box)
json.dump(L, open(lj, "w"))
print(n, "imágenes recortadas")
