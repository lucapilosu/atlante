#!/usr/bin/env python3
"""Controlli del Pilu Sports Almanac (sport/index.html). Uso: python3 tests/sport.py"""
import functools, http.server, json, re, socketserver, sys, tempfile, threading
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
atleti = json.loads((R / "sport/atleti.json").read_text(encoding="utf-8"))
# la pagina scarica atleti.json e versione.json: serve un piccolo server locale
class Muto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Muto, directory=str(R)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
U = f"http://127.0.0.1:{srv.server_address[1]}/sport/"
TOCCO = """([sel, dy]) => { const el = document.querySelector(sel), r = el.getBoundingClientRect(), x = r.left + 30, y = r.top + 10;
  const t = yy => new Touch({identifier: 1, target: el, clientX: x, clientY: yy});
  el.dispatchEvent(new TouchEvent('touchstart', {touches: [t(y)], bubbles: true, cancelable: true}));
  for (let i = 1; i <= 6; i++) el.dispatchEvent(new TouchEvent('touchmove', {touches: [t(y + dy * i / 6)], bubbles: true, cancelable: true}));
  el.dispatchEvent(new TouchEvent('touchend', {touches: [], bubbles: true, cancelable: true})); }"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for nome, ctx in [("pc", b.new_context(viewport={"width": 1280, "height": 800})), ("iphone", b.new_context(**p.devices["iPhone 13"]))]:
        pg = ctx.new_page(); errs = []; esterne = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("request", lambda r: (not r.url.startswith(U) and not r.url.startswith("data:")) and esterne.append(r.url))
        pg.goto(U); pg.wait_for_timeout(300)
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
        pg.goto(U + "#sport=beach"); pg.wait_for_timeout(300)
        check(f"{nome}: apertura da indirizzo", pg.locator("#panel table.albo tbody tr").count() == 8)
        # albi d'oro v0.2: più competizioni per sport
        pg.goto(U + "#sport=calcio"); pg.wait_for_timeout(300)
        check(f"{nome}: calcio, mondiali uomini", pg.locator("#panel table.albo tbody tr").count() == 23 and pg.locator("#panel table.albo tbody tr").first.inner_text().startswith("2026"))
        pg.locator("#panel .tabs button", has_text="Scudetto").click(); pg.wait_for_timeout(200)
        check(f"{nome}: calcio, scudetto", pg.locator("#panel table.albo tbody tr").count() == 125 and "stagione" in pg.locator("#panel table.albo thead").inner_text().lower())
        check(f"{nome}: scudetto 2004-05 non assegnato", "Non assegnato" in pg.locator("#panel tr[data-r='2004–05']").inner_text())
        pg.goto(U + "#sport=basket&g=nba&r=2026"); pg.wait_for_timeout(400)
        check(f"{nome}: link a riga evidenziata", "Knicks" in pg.locator("#panel tr.hl").inner_text())
        larga = pg.evaluate("document.querySelector('#panel').scrollWidth <= document.querySelector('#panel').clientWidth + 1")
        check(f"{nome}: tabella NBA dentro la scheda", larga)
        # pagina di ricerca
        pg.goto(U); pg.wait_for_timeout(250)
        pg.locator("#bCerca").click(); pg.wait_for_timeout(150)
        check(f"{nome}: ricerca aperta", pg.locator("#cerca").is_visible() and pg.locator("#q").is_visible())
        pg.locator("#q").fill("italia 1982"); pg.wait_for_timeout(300)
        li = pg.locator("#risultati li[data-albo^='calcio|0|0|1982']")
        check(f"{nome}: ricerca Italia 1982", li.count() == 1, pg.locator("#risultati").inner_text()[:200])
        check(f"{nome}: indirizzo della ricerca", "#cerca=italia%201982" in pg.url, pg.url)
        li.click(); pg.wait_for_timeout(400)
        check(f"{nome}: dal risultato all'albo", not pg.locator("#cerca").is_visible() and "Italia" in pg.locator("#panel tr.hl").inner_text())
        pg.goto(U + "#cerca=peru"); pg.wait_for_timeout(300)
        check(f"{nome}: ricerca senza accenti", pg.locator("#cerca").is_visible() and "Perù" in pg.locator("#risultati").inner_text())
        pg.locator("#q").fill("imoco"); pg.wait_for_timeout(300)
        check(f"{nome}: ricerca Imoco", pg.locator("#risultati li").count() == 10, pg.locator("#risultati li").count())
        if nome == "iphone":
            check(f"{nome}: filtri chiusi nella riga Filtri", not pg.locator("#filtri").is_visible() and pg.locator("#fBtn").is_visible())
            pg.locator("#fBtn").click(); pg.wait_for_timeout(100)
        pg.locator("#filtri [data-f=cosa] button", has_text="Tessere").click(); pg.wait_for_timeout(100)
        check(f"{nome}: filtro tessere", pg.locator("#risultati li[data-albo]").count() == 0)
        pg.locator("#filtri [data-f=cosa] button", has_text="Tutto").click()
        pg.locator("#q").fill("olimpiadi"); pg.locator("#filtri [data-f=sport] button[data-k='beach']").click(); pg.wait_for_timeout(200)
        check(f"{nome}: filtro sport", pg.locator("#risultati li").count() > 0 and all(x.startswith("beach|") for x in pg.eval_on_selector_all("#risultati li[data-albo]", "l=>l.map(x=>x.dataset.albo)")))
        sw = pg.evaluate("document.querySelector('#cerca').scrollWidth <= document.querySelector('#cerca').clientWidth + 1")
        check(f"{nome}: ricerca senza scorrimento orizzontale", sw)
        check(f"{nome}: riassunto dei filtri", "beach volley" in pg.locator("#fRiass").inner_text())
        # filtri combinati: Brasile, pallavolo, oro -> solo righe con il Brasile nella casella dell'oro
        pg.locator("#azzera").click(); pg.locator("#q").fill(""); pg.wait_for_timeout(100)
        pg.select_option("#fPaese", "Brasile"); pg.locator("#filtri [data-f=sport] button[data-k='pallavolo']").click()
        pg.locator("#filtri [data-f=esito] button[data-k='oro']").click(); pg.locator("#filtri [data-f=cosa] button", has_text="Albi d'oro").click(); pg.wait_for_timeout(200)
        chiavi = pg.eval_on_selector_all("#risultati li[data-albo]", "l=>l.map(x=>x.dataset.albo)")
        attese = sorted(f"pallavolo|{gi}|{ti}|{r.get('stag') or r['anno']}" for gi, g in enumerate(dati["albi"]["pallavolo"]["gruppi"]) for ti, t in enumerate(g["tornei"]) if t["tipo"] == "torneo" for r in t["righe"] if "Brasile" in r["oro"])
        check(f"{nome}: Brasile oro nella pallavolo", sorted(chiavi) == attese and len(attese) > 5, (len(chiavi), len(attese)))
        pg.locator("#filtri [data-f=gen] button[data-k='Donne']").click(); pg.locator("#fDa").fill("2000"); pg.wait_for_timeout(200)
        chiavi = pg.eval_on_selector_all("#risultati li[data-albo]", "l=>l.map(x=>x.dataset.albo)")
        attese = sorted(f"pallavolo|{gi}|{ti}|{r['anno']}" for gi, g in enumerate(dati["albi"]["pallavolo"]["gruppi"]) for ti, t in enumerate(g["tornei"]) if t["tipo"] == "torneo" and t["nome"] == "Donne" for r in t["righe"] if "Brasile" in r["oro"] and r["anno"] >= 2000)
        check(f"{nome}: ... donne dal 2000", sorted(chiavi) == attese and len(attese) >= 2, (chiavi, attese))
        pg.locator("#azzera").click(); pg.wait_for_timeout(100)
        # atleti
        pg.locator("#q").fill("bolt"); pg.wait_for_timeout(1200)
        check(f"{nome}: ricerca atleta Bolt", pg.locator("#risultati li[data-atleta='usain-bolt']").count() == 1 and pg.locator("#risultati li[data-albo^='atletica|']").count() == 6, pg.locator("#risultati").inner_text()[:150])
        pg.locator("#q").fill("yuri chechi"); pg.wait_for_timeout(300)
        check(f"{nome}: ricerca con altro nome (Yuri Chechi)", pg.locator("#risultati li[data-atleta='jury-chechi']").count() == 1)
        pg.locator("#q").fill(""); pg.locator("#filtri [data-f=cosa] button", has_text="Atleti").click(); pg.locator("#filtri [data-f=gen] button[data-k='Donne']").click(); pg.wait_for_timeout(200)
        check(f"{nome}: atlete", pg.locator("#risultati li[data-atleta]").count() == sum(a["genere"] == "Donne" for a in atleti))
        pg.locator("#azzera").click()
        pg.locator("#q").press("Escape"); pg.wait_for_timeout(150)
        check(f"{nome}: chiusura ricerca", not pg.locator("#cerca").is_visible())
        # vista dell'atleta: solo i suoi sport, medaglie sull'asse, collegamento all'albo
        pg.goto(U + "#atleta=karch-kiraly"); pg.wait_for_timeout(900)
        check(f"{nome}: Kiraly, solo pallavolo e beach", pg.eval_on_selector_all(".head", "l=>l.map(x=>x.dataset.sport)") == ["pallavolo", "beach"])
        check(f"{nome}: Kiraly, medaglie da atleta e da allenatore", pg.locator(".mk.all").count() >= 3 and pg.locator(".mk:not(.all)").count() >= 4)
        check(f"{nome}: Kiraly, scheda palmarès", "da allenatore" in pg.locator("#panel").inner_text().lower() and pg.locator("#panel .palm li").count() == len(next(a for a in atleti if a["id"] == "karch-kiraly")["palmares"]))
        pg.locator("#panel .palm button[data-albo='beach|olimpiadi|0|1996']").click(); pg.wait_for_timeout(400)
        check(f"{nome}: dal palmarès all'albo", "Kiraly" in pg.locator("#panel tr.hl").inner_text())
        pg.locator("#vistaEsci").click(); pg.wait_for_timeout(300)
        check(f"{nome}: tutti gli sport di nuovo", pg.locator(".head").count() == len(dati["sport"]))
        # atletica: genere e gara
        pg.goto(U + "#sport=atletica"); pg.wait_for_timeout(400)
        check(f"{nome}: atletica 100 m uomini", pg.locator("#panel table.albo tbody tr").first.inner_text().startswith("2024") and "Lyles" in pg.locator("#panel table.albo tbody tr").first.inner_text())
        pg.locator("#panel .tabs button[data-gen='Donne']").click(); pg.wait_for_timeout(150)
        check(f"{nome}: stessa gara, donne", pg.locator("#panel .tabs.disc button.on").inner_text() == "100 m" and "Alfred" in pg.locator("#panel table.albo tbody tr").first.inner_text())
        check(f"{nome}: oro 2000 non riassegnato", "non riassegnato" in pg.locator("#panel tr[data-r='2000']").inner_text())
        pg.goto(U + "#sport=atletica&g=olimpiadi&t=8&r=2020"); pg.wait_for_timeout(400)
        hl = pg.locator("#panel tr.hl")
        check(f"{nome}: Tamberi e Barshim, oro ex aequo, con bandierina", "Tamberi" in hl.inner_text() and "ex aequo" in hl.inner_text() and hl.locator(".ita").count() == 1)
        check(f"{nome}: niente evidenziazione verde per l'Italia", pg.locator("#panel tr.ita").count() == 0)
        # stile salvato
        pg.locator("#bStile").click(); pg.locator("#stili [data-stile=pastello]").click(); pg.reload(); pg.wait_for_timeout(300)
        check(f"{nome}: stile Pastello ricordato", pg.evaluate("document.documentElement.dataset.stile") == "pastello")
        pg.evaluate("stile('notte')")
        # nuova versione
        pg.route("**/versione.json", lambda r: r.fulfill(status=200, content_type="application/json", body='{"v":"diversa"}'))
        pg.evaluate("ultimoControllo = 0; controllaVersione()"); pg.wait_for_timeout(300)
        check(f"{nome}: avviso di nuova versione", pg.locator("#nuova").is_visible())
        pg.unroute("**/versione.json")
        if nome == "iphone":
            pg.goto(U + "#voce=volley-2025"); pg.wait_for_timeout(400)
            pg.evaluate(TOCCO, [".pin-close", 200]); pg.wait_for_timeout(400)
            check(f"{nome}: scheda chiusa tirandola giù", "open" not in (pg.locator("#panel").get_attribute("class") or ""))
            pg.evaluate(TOCCO, ["#bar", 140]); pg.wait_for_timeout(800)
            check(f"{nome}: barra tirata giù, pagina ricaricata", "v=" in pg.url, pg.url)
        check(f"{nome}: nessun errore", not errs, errs)
        check(f"{nome}: nessuna risorsa esterna", not [u for u in esterne if "favicon" not in u], esterne[:3])
        ctx.close()
    for f in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "atleti.json", "versione.json"):
        check(f"file {f}", (R / "sport" / f).exists())
    pg = b.new_page(); pg.goto(tmp.as_uri()); pg.wait_for_timeout(200)
    check("titolo con voce 2027", "1896–2027" in pg.locator("h1").inner_text(), pg.locator("h1").inner_text())
    b.close()
print(f"{ok + fail} controlli, {fail} falliti"); sys.exit(1 if fail else 0)
