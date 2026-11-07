"""Pruebas funcionales del sitio (Playwright). uso: python3 tools/test_interactions.py http://localhost:4173"""
import sys, asyncio
from playwright.async_api import async_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4173"
ok = lambda c, m: print(("OK   " if c else "FAIL ") + m)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        errs = []
        # ---------- escritorio
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL, wait_until="networkidle"); await pg.wait_for_timeout(2500)
        ok(await pg.evaluate("document.title.length>5"), "título: " + await pg.title())
        # menú: cada enlace lleva a su sección
        links = await pg.evaluate("[...document.querySelectorAll('.menu a')].map(a=>a.textContent.trim())")
        ok(len(links) >= 6, f"menú con {len(links)} enlaces: {links}")
        prev = -1
        for i, t in enumerate(links):
            await pg.locator(".menu a").nth(i).click(); await pg.wait_for_timeout(2300)
            y = await pg.evaluate("scrollY"); on = await pg.evaluate("document.querySelector('.menu a.on')?.textContent.trim()")
            ok(y > prev or i == 0, f"'{t}' → scrollY={round(y)} activo='{on}'")
            prev = y
        # barra de progreso
        sc = await pg.evaluate("getComputedStyle(document.getElementById('progress')).transform")
        ok(sc != "none" and not sc.startswith("matrix(0,"), "barra de progreso: " + sc)
        # lightbox
        await pg.evaluate("window.scrollTo(0,2700)"); await pg.wait_for_timeout(2500)
        await pg.evaluate("document.querySelector('.g-free .ph').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(1800)
        await pg.locator(".g-free .ph").first.click(); await pg.wait_for_timeout(900)
        vis = await pg.evaluate("(()=>{const l=document.querySelector('.lb');return l&&!l.hidden&&getComputedStyle(l).visibility!=='hidden'&&getComputedStyle(l).opacity>0.5})()")
        ok(vis, "lightbox abre al hacer clic")
        s1 = await pg.evaluate("document.querySelector('.lb img').src")
        await pg.keyboard.press("ArrowRight"); await pg.wait_for_timeout(700)
        s2 = await pg.evaluate("document.querySelector('.lb img').src")
        ok(s1 != s2, "→ cambia de imagen"); await pg.keyboard.press("ArrowLeft"); await pg.wait_for_timeout(700)
        s3 = await pg.evaluate("document.querySelector('.lb img').src"); ok(s3 == s1, "← vuelve a la anterior")
        foc = await pg.evaluate("document.querySelector('.lb').contains(document.activeElement)"); ok(foc, "foco dentro del lightbox")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(700)
        hid = await pg.evaluate("(()=>{const l=document.querySelector('.lb');return l.hidden||getComputedStyle(l).visibility==='hidden'||getComputedStyle(l).opacity==0})()")
        ok(hid, "Esc cierra el lightbox")
        # correo
        ok(await pg.evaluate("document.querySelector('a.mail').href.startsWith('mailto:judruizro7d')"), "enlace mailto correcto")
        # imágenes rotas
        await pg.evaluate("document.querySelectorAll('img').forEach(i=>{if(i.getClientRects().length)i.loading='eager'})"); await pg.wait_for_timeout(2500)
        br = await pg.evaluate("[...document.images].filter(i=>i.getClientRects().length&&i.complete&&!i.naturalWidth).map(i=>i.src)")
        ok(not br, f"sin imágenes rotas {br}")
        ov = await pg.evaluate("document.documentElement.scrollWidth<=innerWidth"); ok(ov, "sin scroll horizontal (1440)")
        await pg.close()
        # ---------- móvil
        ctx = await b.new_context(viewport={"width": 390, "height": 800}, is_mobile=True, has_touch=True, device_scale_factor=2)
        m = await ctx.new_page()
        m.on("pageerror", lambda e: errs.append("M " + str(e)))
        await m.goto(URL, wait_until="networkidle"); await m.wait_for_timeout(2000)
        ok(await m.evaluate("document.documentElement.scrollWidth<=innerWidth"), "móvil: sin scroll horizontal")
        await m.locator("#burger").click(); await m.wait_for_timeout(700)
        ok(await m.evaluate("getComputedStyle(document.getElementById('menu')).visibility!=='hidden'"), "móvil: menú hamburguesa abre")
        await m.locator(".menu a").nth(3).click(); await m.wait_for_timeout(2500)
        ok(await m.evaluate("scrollY")>1500, f"móvil: enlace navega (y={round(await m.evaluate('scrollY'))})")
        for w in (768, 1024, 1920):
            t = await b.new_page(viewport={"width": w, "height": 900}); await t.goto(URL, wait_until="networkidle"); await t.wait_for_timeout(800)
            ok(await t.evaluate("document.documentElement.scrollWidth<=innerWidth"), f"{w}px: sin scroll horizontal"); await t.close()
        print("errores de consola:", errs[:5] or "ninguno")
        await b.close()
asyncio.run(main())
