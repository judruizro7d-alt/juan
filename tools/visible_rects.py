"""Mide la zona realmente visible de cada imagen del PDF (el PDF las recorta con máscaras de recorte
que layout.json no refleja). Renderiza la capa sin imágenes y otra con UNA imagen restaurada; la diferencia es su zona visible."""
import json, os, re, subprocess, sys, pymupdf
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from vector_layer import clean_pdf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "..", "PortFolio Juan Ruiz.pdf")
L = json.load(open(os.path.join(ROOT, "raw", "layout.json")))
TMP = "/tmp/vis"; os.makedirs(TMP, exist_ok=True)

def render(pdf, page, box, out):
    x0, y0, x1, y1 = box
    subprocess.run(["pdftocairo", "-png", "-transp", "-r", "72", "-f", str(page), "-l", str(page), "-x", str(x0), "-y", str(y0),
                    "-W", str(x1 - x0), "-H", str(y1 - y0), "-singlefile", pdf, out], check=True)
    return np.array(Image.open(out + ".png").convert("RGBA")).astype(int)

doc = pymupdf.open(PDF)
base = os.path.join(TMP, "base.pdf"); clean_pdf(PDF, base)
res = {}
for i, o in enumerate(L):
    f = o["file"]
    m = re.match(r"p(\d)_x(\d+)\.png", f); pg, xr = int(m[1]), int(m[2])
    if xr == 379: continue  # marcos de polaroid (se gestionan aparte)
    smask = doc.xref_get_key(xr, "SMask")
    keep = {xr}
    if smask[0] == "xref": keep.add(int(smask[1].split()[0]))
    kp = os.path.join(TMP, f"k{xr}.pdf"); clean_pdf(PDF, kp, keep=keep)
    x0, y0, x1, y1 = o["bbox"]
    W, H = (1440, 6000 if pg == 1 else 4875)
    box = (max(0, int(x0) - 120), max(0, int(y0) - 120), min(W, int(x1) + 120), min(H, int(y1) + 120))
    if box[2] <= box[0] or box[3] <= box[1]: continue
    a = render(base, pg, box, os.path.join(TMP, "a")); b = render(kp, pg, box, os.path.join(TMP, "b"))
    d = (np.abs(a - b).sum(axis=2) > 24)
    ys, xs = np.where(d)
    if len(xs) < 50: res[i] = None; continue
    res[i] = [box[0] + int(xs.min()), box[1] + int(ys.min()), box[0] + int(xs.max()) + 1, box[1] + int(ys.max()) + 1]
    print(i, f, [round(v) for v in o["bbox"]], "->", res[i], flush=True)
json.dump(res, open(os.path.join(ROOT, "tools", "visible.json"), "w"))
