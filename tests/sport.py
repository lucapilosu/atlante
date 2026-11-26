#!/usr/bin/env python3
"""Controlli del Pilu Sports Almanac (sport/index.html). Uso: python3 tests/sport.py"""
import json, re, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent.parent
idx = R / "sport/index.html"
dati = json.loads((R / "sport/data/almanacco.json").read_text(encoding="utf-8"))
ok = fail = 0
def check(nome, cond, info=""):
    global ok, fail
    if cond: ok += 1
    else: fail += 1; print("FALLITO:", nome, info)

# copia con una voce del 2027 per provare che il titolo si aggiorna da solo
d2 = json.loads(json.dumps(dati)); d2["voci"].append({**d2["voci"][-1], "id": "prova-2027", "anno": 2027})
tpl = (R / "sport/src/almanacco.html").read_text(encoding="utf-8")
tmp = Path(tempfile.mkdtemp()) / "index.html"
tmp.write_text(tpl.replace("/*DATI*/null", json.dumps(d2, ensure_ascii=False)), encoding="utf-8")

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for nome, ctx in [("pc", b.new_context(viewport={"width": 1280, "height": 800})), ("iphone", b.new_context(**p.devices["iPhone 13"]))]:
        pg = ctx.new_page(); errs = []; esterne = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("request", lambda r: (not r.url.startswith("file:") and not r.url.startswith("data:")) and esterne.append(r.url))
        pg.goto(idx.as_uri()); pg.wait_for_timeout(300)
        check(f"{nome}: titolo", pg.locator("h1").inner_text().replace("\n", " ").strip() == "Pilu Sports Almanac1896–2026" or "1896–2026" in pg.locator("h1").inner_text(), pg.locator("h1").inner_text())
        check(f"{nome}: tessere", pg.locator(".tile").count() == len(dati["voci"]))
        check(f"{nome}: intestazioni", pg.locator(".head").count() == len(dati["sport"]))
        # tessere che si sovrappongono nella stessa colonna
        rects = pg.evaluate("[...document.querySelectorAll('.tile')].map(t=>[t.offsetLeft,t.offsetTop,t.offsetWidth,t.offsetHeight])")
        sov = [(a, c) for i, a in enumerate(rects) for c in rects[i+1:] if a[0] == c[0] and a[1] < c[1] + c[3] and c[1] < a[1] + a[3]]
        check(f"{nome}: nessuna sovrapposizione", not sov, sov[:2])
        pg.locator(".head[data-sport='pallavolo']").click(); pg.wait_for_timeout(350)
        check(f"{nome}: albo pallavolo uomini", pg.locator("#panel table.albo tbody tr").count() == 16)
        pg.locator("#panel .tabs button", has_text="Donne").click()
        check(f"{nome}: albo donne, 2024 Italia oro", "Italia" in pg.locator("#panel table.albo tbody tr").first.inner_text())
        pg.locator("#panel .lista li").first.click(); pg.wait_for_timeout(350)
        check(f"{nome}: scheda da elenco", pg.locator("#panel h2").inner_text().startswith("Doppio titolo mondiale"))
        check(f"{nome}: fonti con link", pg.locator("#panel .fonti a").count() >= 1)
        check(f"{nome}: indirizzo condivisibile", "voce=volley-2025" in pg.url)
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        check(f"{nome}: chiusura", "open" not in (pg.locator("#panel").get_attribute("class") or ""))
        pg.goto(idx.as_uri() + "#sport=beach"); pg.wait_for_timeout(300)
        check(f"{nome}: apertura da indirizzo", pg.locator("#panel table.albo tbody tr").count() == 8)
        # albi d'oro v0.2: più competizioni per sport
        pg.goto(idx.as_uri() + "#sport=calcio"); pg.wait_for_timeout(300)
        check(f"{nome}: calcio, mondiali uomini", pg.locator("#panel table.albo tbody tr").count() == 23 and pg.locator("#panel table.albo tbody tr").first.inner_text().startswith("2026"))
        pg.locator("#panel .tabs button", has_text="Scudetto").click(); pg.wait_for_timeout(200)
        check(f"{nome}: calcio, scudetto", pg.locator("#panel table.albo tbody tr").count() == 125 and "stagione" in pg.locator("#panel table.albo thead").inner_text().lower())
        check(f"{nome}: scudetto 2004-05 non assegnato", "Non assegnato" in pg.locator("#panel tr[data-r='2004–05']").inner_text())
        pg.goto(idx.as_uri() + "#sport=basket&g=nba&r=2026"); pg.wait_for_timeout(400)
        check(f"{nome}: link a riga evidenziata", "Knicks" in pg.locator("#panel tr.hl").inner_text())
        larga = pg.evaluate("document.querySelector('#panel').scrollWidth <= document.querySelector('#panel').clientWidth + 1")
        check(f"{nome}: tabella NBA dentro la scheda", larga)
        # pagina di ricerca
        pg.goto(idx.as_uri()); pg.wait_for_timeout(250)
        pg.locator("#bCerca").click(); pg.wait_for_timeout(150)
        check(f"{nome}: ricerca aperta", pg.locator("#cerca").is_visible() and pg.locator("#q").is_visible())
        pg.locator("#q").fill("italia 1982"); pg.wait_for_timeout(300)
        li = pg.locator("#risultati li[data-albo^='calcio|0|0|1982']")
        check(f"{nome}: ricerca Italia 1982", li.count() == 1, pg.locator("#risultati").inner_text()[:200])
        check(f"{nome}: indirizzo della ricerca", "#cerca=italia%201982" in pg.url, pg.url)
        li.click(); pg.wait_for_timeout(400)
        check(f"{nome}: dal risultato all'albo", not pg.locator("#cerca").is_visible() and "Italia" in pg.locator("#panel tr.hl").inner_text())
        pg.goto(idx.as_uri() + "#cerca=peru"); pg.wait_for_timeout(300)
        check(f"{nome}: ricerca senza accenti", pg.locator("#cerca").is_visible() and "Perù" in pg.locator("#risultati").inner_text())
        pg.locator("#q").fill("imoco"); pg.wait_for_timeout(300)
        check(f"{nome}: ricerca Imoco", pg.locator("#risultati li").count() == 10, pg.locator("#risultati li").count())
        pg.locator("#fTipo button", has_text="Tessere").click(); pg.wait_for_timeout(100)
        check(f"{nome}: filtro tessere", pg.locator("#risultati li[data-albo]").count() == 0)
        pg.locator("#fTipo button", has_text="Tutto").click()
        pg.locator("#q").fill("olimpiadi"); pg.locator("#fSport button[data-s='beach']").click(); pg.wait_for_timeout(200)
        check(f"{nome}: filtro sport", pg.locator("#risultati li").count() > 0 and all(x.startswith("beach|") for x in pg.eval_on_selector_all("#risultati li[data-albo]", "l=>l.map(x=>x.dataset.albo)")))
        sw = pg.evaluate("document.querySelector('#cerca').scrollWidth <= document.querySelector('#cerca').clientWidth + 1")
        check(f"{nome}: ricerca senza scorrimento orizzontale", sw)
        pg.locator("#q").press("Escape"); pg.wait_for_timeout(150)
        check(f"{nome}: chiusura ricerca", not pg.locator("#cerca").is_visible())
        check(f"{nome}: nessun errore", not errs, errs)
        check(f"{nome}: nessuna risorsa esterna", not [u for u in esterne if "favicon" not in u], esterne[:3])
        ctx.close()
    pg = b.new_page(); pg.goto(tmp.as_uri()); pg.wait_for_timeout(200)
    check("titolo con voce 2027", "1896–2027" in pg.locator("h1").inner_text(), pg.locator("h1").inner_text())
    b.close()
print(f"{ok + fail} controlli, {fail} falliti"); sys.exit(1 if fail else 0)
