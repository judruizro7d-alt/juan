"""Genera un PDF con la capa vectorial de una página: sin fotos y sin fondo blanco.
Los flujos de contenido (opacidades, trazos, sombras) no se alteran; solo se vacían las imágenes."""
import re, pymupdf

def clean_pdf(pdf, out, keep=None):
    """keep: xref de una imagen que NO se vacía (sirve para medir su zona visible)."""
    doc = pymupdf.open(pdf)
    # 1) el rectángulo blanco de fondo de página se define pero no se pinta
    for pg in doc:
        for xr in pg.get_contents():
            data = doc.xref_stream(xr)
            new = re.sub(rb"(0 0 1920 \d+ re\n)f\b", rb"\1n", data)
            if new != data:
                doc.update_stream(xr, new)
    # máscara transparente compartida
    mx = doc.get_new_xref()
    doc.update_object(mx, "<< /Type /XObject /Subtype /Image /Width 1 /Height 1 /ColorSpace /DeviceGray /BitsPerComponent 8 >>")
    doc.update_stream(mx, b"\x00", new=True)
    # 2) todas las imágenes (incluidas las anidadas) -> 1x1 transparente
    for xr in range(1, doc.xref_length()):
        try:
            if doc.xref_get_key(xr, "Subtype")[1] != "/Image":
                continue
        except Exception:
            continue
        is_mask = False
        cs = doc.xref_get_key(xr, "ColorSpace")[1]
        for k in ("Filter", "DecodeParms", "Decode", "Mask", "Intent", "SMaskInData", "Interpolate"):
            doc.xref_set_key(xr, k, "null")
        if xr == mx or (keep and xr in keep): continue
        doc.xref_set_key(xr, "Width", "1"); doc.xref_set_key(xr, "Height", "1"); doc.xref_set_key(xr, "BitsPerComponent", "8")
        gray = "Gray" in cs or cs == "/DeviceGray"
        doc.xref_set_key(xr, "ColorSpace", "/DeviceGray" if gray else "/DeviceRGB")
        doc.update_stream(xr, b"\x00" if gray else b"\x00\x00\x00", new=True)
        if not gray or True:
            doc.xref_set_key(xr, "SMask", f"{mx} 0 R")
    doc.save(out, garbage=0)

if __name__ == "__main__":
    import sys
    clean_pdf(sys.argv[1], sys.argv[2])
