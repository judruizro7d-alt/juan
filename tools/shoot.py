"""Capturas del sitio (Playwright + Chrome del sistema) para verificar contra el PDF.
uso: python3 tools/shoot.py <url> <ancho> <salida.png> [alto_viewport]
Fuerza el estado final de las animaciones haciendo scroll por toda la página."""
import sys, asyncio
from playwright.async_api import async_playwright
url, width, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
vh = int(sys.argv[4]) if len(sys.argv) > 4 else 900
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        import os
        pg = await b.new_page(viewport={"width": width, "height": vh}, reduced_motion="reduce" if os.environ.get("RM") else "no-preference")
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        await pg.goto(url, wait_until="networkidle")
        await pg.wait_for_timeout(800)
        H = await pg.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < H:
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(120); y += vh // 2
        await pg.wait_for_timeout(2500)
        await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>{if(i.getClientRects().length>0)i.loading='eager'})")
        await pg.wait_for_function("[...document.images].filter(i=>i.getClientRects().length>0).every(i=>i.complete && i.naturalWidth>0)", timeout=30000)
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(600)
        await pg.screenshot(path=out, full_page=True)
        print("height", H, "errors:", errs[:8])
        await b.close()
asyncio.run(main())
