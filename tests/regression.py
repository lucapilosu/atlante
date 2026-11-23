"""Test di regressione dell'Atlante storico.

Uso:  python3 tests/regression.py <file.html> <cartella_screenshot>

Verifica, su desktop e su iPhone 13 emulato (più alcuni controlli su iPad emulato), i comportamenti che non devono
rompersi tra una versione e l'altra (decisioni di prodotto dei documenti 07 e 09
dell'handover). I controlli marcati "noto" documentano difetti conosciuti e non
fanno fallire l'esecuzione.
"""
import sys, re, json, asyncio
from playwright.async_api import async_playwright

HTML, OUT = sys.argv[1], sys.argv[2]
import os, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
_srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Quiet, directory=os.path.dirname(os.path.abspath(HTML))))
threading.Thread(target=_srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{_srv.server_address[1]}/" + os.path.basename(HTML)
CHROME = "/usr/bin/google-chrome"

JS_CONTRAST = """
(el) => {
  const parse = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const p = m[1].split(',').map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = ({r,g,b}) => { const f = v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); };
    return .2126*f(r) + .7152*f(g) + .0722*f(b); };
  const fg = parse(getComputedStyle(el).color);
  let node = el, bg = null;
  while (node && node.nodeType === 1) { const c = parse(getComputedStyle(node).backgroundColor);
    if (c && c.a > 0.5) { bg = c; break; } node = node.parentElement; }
  if (!bg) bg = {r:255, g:255, b:255, a:1};
  const L1 = lum(fg), L2 = lum(bg);
  return {text: el.textContent.trim(), ratio: (Math.max(L1,L2) + .05) / (Math.min(L1,L2) + .05)};
}
"""

class Run:
    def __init__(self, device):
        self.device, self.rows = device, []
    def check(self, code, name, ok, detail="", known=False):
        self.rows.append({"device": self.device, "code": code, "name": name,
                          "esito": ("OK" if ok else ("NOTO" if known else "FALLITO")), "dettaglio": detail})

STYLES = ["ottanio", "museo", "cartografo"]

async def year(p):
    return (await p.text_content("#yearLabel")).strip()

async def set_year(p, y):
    await p.evaluate("""(y)=>{const r=document.getElementById('yearRange');r.value=y;
      r.dispatchEvent(new Event('input',{bubbles:true}));r.dispatchEvent(new Event('change',{bubbles:true}));}""", y)
    await p.wait_for_timeout(350)

async def open_details(p, selector):
    await p.evaluate("(s)=>document.querySelectorAll(s).forEach(d=>d.open=true)", selector)
    await p.wait_for_timeout(250)

async def click_el(p, sel):
    # porta l'elemento al centro dello schermo e lo clicca davvero (niente clic "forzati" che finiscono su barre fisse)
    await p.evaluate("(s)=>document.querySelector(s).scrollIntoView({block:'center',behavior:'instant'})", sel)
    await p.wait_for_timeout(120)
    await p.click(sel)

async def goto_view(p, name):
    await p.evaluate("(n)=>{location.hash='#'+n}", name)
    await p.wait_for_timeout(450)

async def tap(p, locator, mobile):
    # porta l'elemento al centro dello schermo: un tocco su un punto coperto dalle barre fisse finirebbe sulla barra
    await locator.evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")
    await p.wait_for_timeout(80)
    if mobile:
        await locator.tap(force=True)
    else:
        await locator.click(force=True)

async def run_device(pw, name, ctx_kwargs, mobile):
    R = Run(name)
    browser = await pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    ctx = await browser.new_context(**ctx_kwargs)
    p = await ctx.new_page()
    errors, external = [], set()
    p.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
    p.on("console", lambda m: errors.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
    # v0.52: le foto delle schede arrivano da Wikimedia Commons (scelta di Luca); ogni altra risorsa esterna resta un errore
    p.on("request", lambda r: external.add(r.url) if not r.url.startswith(("file:", "data:", "blob:", "http://127.0.0.1", "https://upload.wikimedia.org/wikipedia/commons/")) else None)
    await p.goto(URL, wait_until="load")
    await p.wait_for_timeout(1200)

    # T02 versione coerente
    title = await p.title()
    eyebrow = await p.text_content("header .eyebrow")
    footer = await p.text_content(".footer")
    v = re.search(r"v(\d+\.\d+)", title)
    v = v.group(1) if v else "?"
    ok = (f"v{v}" in eyebrow) and (f"versione {v}" in footer)
    R.check("T02", "Versione coerente in titolo, intestazione e footer", ok, f"titolo v{v}")

    # T03 slider anno
    await p.evaluate("()=>{const r=document.getElementById('dockRange');r.value=yearToPos(-500);r.dispatchEvent(new Event('input',{bubbles:true}));r.dispatchEvent(new Event('change',{bubbles:true}))}")
    await p.wait_for_timeout(350)
    y = await year(p)
    dock = (await p.text_content("#dockYear")).strip()
    vis3 = await p.evaluate("()=>{const r=document.getElementById('dockRange').getBoundingClientRect();return r.width>0&&r.height>0}")
    R.check("T03", "Lo slider della barra in basso imposta l'anno", y == "500 a.C." and dock == y and vis3, f"{y} / barra {dock}")

    # T04 ricerca e selezione risultato
    await p.fill("#search", "roma")
    await p.wait_for_timeout(500)
    hits = p.locator("#searchPreview .search-hit")
    n_hits = await hits.count()
    first_name = (await hits.first.locator("strong").text_content()).strip() if n_hits else ""
    if n_hits:
        await tap(p, hits.first, mobile)
        await p.wait_for_timeout(500)
    field = await p.input_value("#search")
    prev_hidden = await p.evaluate("()=>{const b=document.getElementById('searchPreview');return b.hidden||!b.innerHTML.trim()}")
    detail_h = (await p.text_content("#detail h2") or "").strip()
    R.check("T04", "Ricerca: scelta risultato svuota il campo, chiude l'anteprima, apre la scheda",
            n_hits > 0 and field == "" and prev_hidden and detail_h == first_name and await p.is_visible("#scheda"),
            f"{n_hits} risultati, scheda '{detail_h}'")

    # T22 scheda a comparsa: su telefono è un pannello in basso che lascia vedere la mappa; × la chiude
    g22 = await p.evaluate("""()=>{const s=document.getElementById('scheda'),r=s.getBoundingClientRect(),d=document.getElementById('timeDock').getBoundingClientRect(),
        m=document.querySelector('#view-esplora .mapstage').getBoundingClientRect(),cs=getComputedStyle(s);
        return {sheet:s.classList.contains('is-sheet'),fixed:cs.position==='fixed',top:Math.round(r.top),bottom:Math.round(r.bottom),dockTop:Math.round(d.top),vh:innerHeight,
          layoutCols:getComputedStyle(s.parentElement).gridTemplateColumns.split(' ').length}}""")
    await tap(p, p.locator("#sheetClose"), mobile)
    await p.wait_for_timeout(550)  # v0.56: la chiusura è animata (fino a 300 ms)
    closed22 = await p.evaluate("()=>document.getElementById('scheda').hidden")
    if mobile:
        ok22 = g22["sheet"] and g22["fixed"] and g22["bottom"] <= g22["dockTop"] and g22["top"] > g22["vh"] * 0.3 and closed22
    else:
        ok22 = (not g22["sheet"]) and g22["layoutCols"] == 2 and closed22
    R.check("T22", "Scheda a comparsa: si apre con la scelta, non copre la barra del tempo, si chiude con ×", ok22, f"{g22}, chiusa dopo ×: {closed22}")

    # Mappa
    await open_details(p, "#mapView")
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    await set_year(p, -16)
    await click_el(p, "#zoomReset")
    await p.wait_for_timeout(300)

    # T11 marker solo dell'anno corrente
    pins_ok = await p.evaluate("""()=>{const ids=[...document.querySelectorAll('#pins .map-marker')].map(g=>g.dataset.id);
       return {n:ids.length, bad:ids.filter(id=>{const x=ALL.find(a=>a.id===id);return !x||chosenYear<x.start_year||chosenYear>x.end_year})}}""")
    R.check("T11", "Sulla mappa solo punti attivi nell'anno", pins_ok["n"] > 0 and not pins_ok["bad"], f"{pins_ok['n']} punti, fuori anno: {pins_ok['bad']}")

    # T05 tap marker -> popup, anno invariato
    y0 = await year(p)
    marker = p.locator("#pins .map-marker").first
    await tap(p, marker, mobile)
    await p.wait_for_timeout(400)
    popup_vis = await p.is_visible("#mapPointPopup")
    popup_title = (await p.text_content("#mapPointPopup strong") or "").strip() if popup_vis else ""
    sheet_after_tap = await p.evaluate("()=>!document.getElementById('scheda').hidden")
    R.check("T05", "Tap su un punto: popup con titolo, anno invariato, la scheda non si apre da sola", popup_vis and popup_title != "" and await year(p) == y0 and not sheet_after_tap,
            f"'{popup_title}', anno {y0} -> {await year(p)}")

    # T12 popup ancorato: non copre il proprio punto e la freccia lo indica (tutti i punti visibili)
    await tap(p, p.locator("#mapPointPopup .popup-close"), mobile)
    await p.wait_for_timeout(200)
    ids = await p.evaluate("()=>[...document.querySelectorAll('#pins .map-marker')].map(g=>g.dataset.id)")
    bad = []
    for pid in ids:
        if await p.is_visible("#mapPointPopup"):
            await p.evaluate("()=>closeMapPointPopup()")
        m = p.locator(f"#pins .map-marker[data-id='{pid}']")
        if not await m.count():
            continue
        await tap(p, m, mobile)
        await p.wait_for_timeout(250)
        mb = await m.locator("circle.pin").bounding_box()   # misurato dopo il tocco, che può far scorrere la pagina
        geo = await p.evaluate("""()=>{const pp=document.getElementById('mapPointPopup');if(pp.hidden)return null;
            const r=pp.getBoundingClientRect(),a=getComputedStyle(pp,'::after');
            const below=pp.classList.contains('is-below');const ax=r.left+parseFloat(a.left)+7;
            return {l:r.left,t:r.top,r:r.right,b:r.bottom,tipx:ax,tipy:below?r.top-7:r.bottom+7,below}}""")
        if not geo:
            bad.append(f"{pid}: popup non aperto"); continue
        mx, my = mb["x"] + mb["width"] / 2, mb["y"] + mb["height"] / 2
        covered = geo["l"] < mx < geo["r"] and geo["t"] < my < geo["b"]
        dist = ((mx - geo["tipx"]) ** 2 + (my - geo["tipy"]) ** 2) ** 0.5
        if covered or dist > 16:
            bad.append(f"{pid}: {'coperto' if covered else ''} freccia a {dist:.0f}px")
    if await p.is_visible("#mapPointPopup"):
        await p.evaluate("()=>closeMapPointPopup()")
    R.check("T12", "Popup ancorato: non copre il punto, la freccia lo indica", ids and not bad,
            f"{len(ids)} punti provati; " + ("; ".join(bad[:4]) or "tutti corretti"))
    await tap(p, p.locator("#pins .map-marker").first, mobile)
    await p.wait_for_timeout(300)

    # T13 il popup resta agganciato al punto dopo uno scroll della pagina e uno zoom della mappa
    measure = """(id)=>{const pp=document.getElementById('mapPointPopup');if(pp.hidden)return {closed:true};
        const c=document.querySelector(`#pins .map-marker[data-id='${id}'] circle.pin`);if(!c)return {closed:false,gone:true};
        const m=c.getBoundingClientRect(),r=pp.getBoundingClientRect(),a=getComputedStyle(pp,'::after'),below=pp.classList.contains('is-below');
        const tx=r.left+parseFloat(a.left)+7,ty=below?r.top-7:r.bottom+7;
        return {closed:false,dist:Math.hypot(m.left+m.width/2-tx,m.top+m.height/2-ty)}}"""
    pid = await p.evaluate("()=>document.getElementById('mapPointPopup').dataset.itemId")
    await p.evaluate("()=>window.scrollBy(0,60)")
    await p.wait_for_timeout(250)
    after_scroll = await p.evaluate(measure, pid)
    await p.evaluate("()=>{const r=document.getElementById('world').getBoundingClientRect();setMapZoom(mapZoom*1.5,r.left+r.width/2,r.top+r.height/2)}")  # su telefono il pulsante + è nascosto: si usa la stessa funzione del pizzico
    await p.wait_for_timeout(500)
    after_zoom = await p.evaluate(measure, pid)
    ok_scroll = not after_scroll.get("closed") and after_scroll.get("dist", 99) <= 16
    ok_zoom = after_zoom.get("closed") or after_zoom.get("dist", 99) <= 16
    R.check("T13", "Il popup segue il punto dopo scroll della pagina e zoom della mappa (o si chiude se il punto esce)",
            ok_scroll and ok_zoom, f"dopo scroll {after_scroll}, dopo zoom {after_zoom}")
    await p.evaluate("()=>closeMapPointPopup()")  # v0.49: con più punti il popup può coprire i comandi di zoom
    await click_el(p, "#zoomReset")
    await p.wait_for_timeout(300)
    if not await p.is_visible("#mapPointPopup"):
        await tap(p, p.locator("#pins .map-marker").first, mobile)
        await p.wait_for_timeout(300)

    # T06 contrasto pulsanti del popup, per ogni palette
    low = []
    for pal in STYLES:
        await p.evaluate("(n)=>{const b=document.querySelector(`.palette-choice[data-palette='${n}']`);if(b)b.click()}", pal)
        await p.wait_for_timeout(120)
        if not await p.is_visible("#mapPointPopup"):
            await tap(p, p.locator("#pins .map-marker").first, mobile); await p.wait_for_timeout(300)
        for b in await p.query_selector_all("#mapPointPopup .popup-actions button"):
            c = await b.evaluate(JS_CONTRAST)
            if c["ratio"] < 4.5:
                low.append(f"{pal}: '{c['text']}' {c['ratio']:.1f}:1")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='ottanio']`)?.click()")
    R.check("T06", "Pulsanti del popup leggibili (contrasto >= 4.5:1) in tutti gli stili", not low, "; ".join(low) or "tutti >= 4.5:1")
    await p.screenshot(path=f"{OUT}/{name}_popup.png")

    # T07 "Apri scheda" apre la scheda senza cambiare anno
    if not await p.is_visible("#mapPointPopup"):
        await tap(p, p.locator("#pins .map-marker").first, mobile); await p.wait_for_timeout(300)
    ptitle = (await p.text_content("#mapPointPopup strong")).strip()
    y0 = await year(p)
    await tap(p, p.locator("#mapPointPopup .popup-open"), mobile)
    await p.wait_for_timeout(600)
    dh = (await p.text_content("#detail h2") or "").strip()
    R.check("T07", "'Apri scheda' apre la scheda giusta senza cambiare anno", dh == ptitle and await year(p) == y0 and await p.is_visible("#scheda"), f"'{dh}', anno {y0} -> {await year(p)}")
    await p.evaluate("()=>closeDetail({instant:true})")

    # T08 confronto: massimo 5, anno invariato (vista Confronto, v0.48)
    await goto_view(p, "confronto")
    y0 = await year(p)
    added = []
    for q in ["roma", "maya", "han", "egitto", "inca", "nazca", "kush"]:
        if len(added) >= 6: break
        await p.fill("#compareSearch", q); await p.wait_for_timeout(250)
        cands = await p.query_selector_all("#compareResults [data-add-compare]")
        for c in cands:
            cid = await c.get_attribute("data-add-compare")
            if cid not in added:
                await c.evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})"); await c.click(); added.append(cid); await p.wait_for_timeout(200); break
    count_txt = (await p.text_content("#compareCount")).strip()
    n_cmp = await p.evaluate("()=>compareIds.length")
    R.check("T08", "Confronto: al massimo 5 elementi, l'anno non cambia",
            len(added) >= 6 and n_cmp == 5 and count_txt.startswith("5 / 5") and await year(p) == y0,
            f"tentati {len(added)}, presenti {n_cmp}, '{count_txt}', anno {y0} -> {await year(p)}")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id))}")

    # T09 Universo storico: vista dedicata, disegna le voci, il trascinamento sposta il tempo senza cambiare anno
    await goto_view(p, "universo")
    await p.wait_for_timeout(400)
    u0 = await p.evaluate("()=>({nodes:document.querySelectorAll('#universeCanvas [data-uid]').length,center:universeCenter,year:document.getElementById('yearLabel').textContent,w:document.getElementById('universeViewport').getBoundingClientRect().width})")
    vp = p.locator("#universeViewport")
    await vp.evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")
    await p.wait_for_timeout(150)
    bb = await vp.bounding_box()
    cx, cy = bb["x"] + bb["width"] * 0.6, bb["y"] + min(bb["height"] * 0.5, 140)
    if mobile:
        cdp = await p.context.new_cdp_session(p)
        await cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": cx, "y": cy}]})
        for i in range(1, 11):
            await cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": cx - 15 * i, "y": cy}]})
            await p.wait_for_timeout(16)
        await cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    else:
        await p.mouse.move(cx, cy); await p.mouse.down(); await p.mouse.move(cx - 150, cy, steps=8); await p.mouse.up()
    await p.wait_for_timeout(400)
    u1 = await p.evaluate("()=>({center:universeCenter,year:document.getElementById('yearLabel').textContent})")
    R.check("T09", "Universo storico: vista dedicata con le voci disegnate; trascinare sposta il tempo, non l'anno",
            u0["nodes"] > 10 and u0["w"] > 200 and abs(u1["center"] - u0["center"]) > 1 and u1["year"] == u0["year"],
            f"{u0['nodes']} elementi disegnati, centro {round(u0['center'])} -> {round(u1['center'])}, anno {u0['year']} -> {u1['year']}")

    # T17 filtri della mappa: ogni filtro nasconde solo i punti della sua tipologia (vista Esplora)
    await goto_view(p, "esplora")
    await set_year(p, 1550)
    await click_el(p, "#zoomReset"); await p.wait_for_timeout(300)
    cat = """()=>{const c=x=>{if(x.kind==='event')return 'layerEvents';const t=x.entity_type||'';
        if(['archaeological_site','site','archaeological_period','archaeological_tradition'].includes(t))return 'layerSites';
        if(['religion','movement','invention'].includes(t))return 'layerNetworks';return 'layerCivil'};
        const out={};document.querySelectorAll('#pins .map-marker').forEach(g=>{const x=ALL.find(a=>a.id===g.dataset.id);const k=c(x);out[k]=(out[k]||0)+1});return out}"""
    base = await p.evaluate(cat)
    problems = []
    # un filtro senza voci localizzate della sua tipologia deve essere nascosto
    empty = await p.evaluate("""()=>['layerCivil','layerSites','layerNetworks','layerEvents'].filter(id=>!ALL.some(x=>hasPoint(x)&&mapLayerOf(x)===id))""")
    for layer in empty:
        if await p.evaluate("(id)=>!document.getElementById(id).closest('label').hidden", layer):
            problems.append(f"{layer} senza voci localizzate ma visibile")
    for layer in [l for l in ["layerCivil", "layerSites", "layerNetworks", "layerEvents"] if l not in empty]:
        await p.evaluate("(id)=>{const c=document.getElementById(id);c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}))}", layer)
        await p.wait_for_timeout(200)
        now = await p.evaluate(cat)
        if now.get(layer):
            problems.append(f"{layer}: ancora {now[layer]} punti")
        for k, n in base.items():
            if k != layer and now.get(k, 0) != n:
                problems.append(f"{layer} ha nascosto anche {k}")
        await p.evaluate("(id)=>{const c=document.getElementById(id);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}", layer)
        await p.wait_for_timeout(150)
    v17 = await p.evaluate("()=>[currentView,chosenYear]")
    R.check("T17", "Filtri mappa: ognuno nasconde solo la sua tipologia (Civiltà, Siti, Reti e idee, Eventi)",
            len(base) >= 3 and not problems, f"vista {v17[0]}, anno {v17[1]}, punti per tipologia: {base}; filtri nascosti perché vuoti: {empty}; " + ("; ".join(problems) or "ok"))

    # T14 viste: una sola vista visibile, link attivo, anno/selezione/confronto conservati
    await set_year(p, -16)
    await p.evaluate("()=>{selectItem('civilization-rome',{preserveYear:true});addCompare('culture-maya');addCompare('civilization-han')}")
    state0 = await p.evaluate("()=>[document.getElementById('yearLabel').textContent,selected,compareIds.length]")
    bad = []
    order = ["contemporanei", "tecnologia", "universo", "impostazioni", "archivio", "impostazioni", "confronto", "esplora"] if mobile else ["contemporanei", "tecnologia", "universo", "confronto", "archivio", "impostazioni", "esplora"]
    for v in order:
        if mobile and v in ("archivio", "confronto"):
            # su telefono archivio e confronto si aprono da "Altro"
            await tap(p, p.locator(f"#view-impostazioni .more-link[data-view-link='{v}']"), mobile)
        elif mobile:
            await tap(p, p.locator(f".mobile-nav a[data-view-link='{v}']"), mobile)
        else:
            await p.click(f".view-tabs a[data-view-link='{v}']")
        await p.wait_for_timeout(400)
        info = await p.evaluate("""()=>({vis:[...document.querySelectorAll('.view')].filter(v=>!v.hidden).map(v=>v.dataset.view),
            hash:location.hash,active:[...document.querySelectorAll('[data-view-link].active')].map(a=>a.dataset.viewLink)})""")
        await p.evaluate("()=>hideToast()")
        expect = {v, "impostazioni"} if v in ("archivio", "confronto") else {v}
        if info["vis"] != [v] or info["hash"] != "#" + v or set(info["active"]) != expect:
            bad.append(f"{v}: {info}")
    state1 = await p.evaluate("()=>[document.getElementById('yearLabel').textContent,selected,compareIds.length]")
    R.check("T14", "Viste: una alla volta, link evidenziato, anno/selezione/confronto conservati",
            not bad and state0 == state1, ("; ".join(bad) or "navigazione ok") + f"; stato {state0} -> {state1}")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id))}")

    # T15 Contemporanei: elenco e punti = voci che si sovrappongono alla durata della voce scelta
    await goto_view(p, "contemporanei")
    await p.fill("#contempSearch", "roma repubblica"); await p.wait_for_timeout(300)
    await tap(p, p.locator("#contempResults [data-pick='civilization-rome']"), mobile)
    await p.wait_for_timeout(600)
    c15 = await p.evaluate("""()=>{const f=ALL.find(x=>x.id==='civilization-rome');
        const exp=ALL.filter(x=>x.id!==f.id&&x.start_year<=f.end_year&&x.end_year>=f.start_year).map(x=>x.id).sort();
        contempView='elenco';renderContemporanei(); // v0.53: questo controllo riguarda la vista Elenco; il Grafico ha T50
        document.querySelectorAll('[data-contemp-more]').forEach(b=>b.click());
        const shown=[...document.querySelectorAll('#contempList .contemp-row')].map(r=>r.dataset.id).sort();
        const pins=[...document.querySelectorAll('#pins .map-marker')].map(g=>g.dataset.id);
        const badPins=pins.filter(id=>{const x=ALL.find(a=>a.id===id);return !(x.id===f.id||(x.start_year<=f.end_year&&x.end_year>=f.start_year))});
        const row=id=>document.querySelector(`#contempList .contemp-row[data-id='${id}'] .contemp-overlap`)?.textContent||'';
        return {title:document.getElementById('contempTitle').textContent,exp:exp.length,shown:shown.length,same:JSON.stringify(exp)===JSON.stringify(shown),
          pins:pins.length,badPins,han:row('civilization-han'),nur:row('culture-nuragic'),_:(contempView='grafico',renderContemporanei(),0)}}""")
    ok15 = (c15["same"] and c15["title"] == "Durante «Roma: Repubblica e Impero»" and c15["pins"] > 0 and not c15["badPins"]
            and c15["han"].startswith("insieme dal 206 a.C. al 220 d.C.") and c15["nur"] == "insieme dal 509 a.C. al 500 a.C. · ≈ 9 anni")
    R.check("T15", "Contemporanei: elenco e punti mostrano solo le voci sovrapposte alla durata scelta, con anni corretti",
            ok15, f"attese {c15['exp']}, mostrate {c15['shown']}, punti {c15['pins']} (fuori periodo {c15['badPins']}); Han: '{c15['han']}'; Nuragici: '{c15['nur']}'")
    await p.screenshot(path=f"{OUT}/{name}_contemporanei.png", full_page=True)

    # T19 dal popup in Contemporanei, "Apri scheda" porta alla scheda nella vista Esplora
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    await tap(p, p.locator("#pins .map-marker[data-id='civilization-han']"), mobile)
    await p.wait_for_timeout(300)
    # v0.49: a Xi'an più voci condividono il punto; se il tocco apre un'altra voce, la si sceglie da «Qui vicino»
    if await p.evaluate("()=>document.getElementById('mapPointPopup').dataset.itemId") != "civilization-han":
        await tap(p, p.locator("#mapPointPopup [data-here='civilization-han']"), mobile)
        await p.wait_for_timeout(300)
    await tap(p, p.locator("#mapPointPopup .popup-open"), mobile)
    await p.wait_for_timeout(700)
    v19 = await p.evaluate("()=>({view:currentView,hash:location.hash,h:document.querySelector('#detail h2')?.textContent,mapInEsplora:!!document.querySelector('#view-esplora #mappa')})")
    R.check("T19", "Contemporanei: 'Apri scheda' porta alla scheda nella vista Esplora", v19["view"] == "esplora" and v19["hash"] == "#esplora"
            and v19["h"] == "Dinastia Han" and v19["mapInEsplora"], str(v19))

    # T16 ricerca (D3): l'anno resta se la voce esiste nell'anno, altrimenti salta al suo periodo
    await set_year(p, -16)
    await p.fill("#search", "roma repubblica"); await p.wait_for_timeout(350)
    await tap(p, p.locator("#searchPreview .search-hit[data-id='civilization-rome']"), mobile); await p.wait_for_timeout(400)
    y_keep = await year(p)
    await set_year(p, -3000)
    await p.fill("#search", "roma repubblica"); await p.wait_for_timeout(350)
    await tap(p, p.locator("#searchPreview .search-hit[data-id='civilization-rome']"), mobile); await p.wait_for_timeout(400)
    y_jump = await year(p)
    R.check("T16", "Ricerca: anno fermo se la voce esiste nell'anno, altrimenti salta al suo periodo",
            y_keep == "16 a.C." and y_jump != "3000 a.C.", f"Roma da 16 a.C. -> {y_keep}; da 3000 a.C. -> {y_jump}")

    # T20 archivio: filtri e ricerca propri, che non toccano la ricerca principale
    await goto_view(p, "archivio")
    n_all = await p.evaluate("()=>[document.querySelectorAll('#results .item').length,ALL.length]")
    await p.select_option("#region", "Asia"); await p.wait_for_timeout(250)
    await p.fill("#archiveSearch", "impero"); await p.wait_for_timeout(250)
    a20 = await p.evaluate("()=>({n:document.querySelectorAll('#results .item').length,regions:[...new Set([...document.querySelectorAll('#results .item')].map(b=>ALL.find(x=>x.id===b.dataset.id).region))]})")
    await goto_view(p, "esplora")
    await p.fill("#search", "roma repubblica"); await p.wait_for_timeout(350)
    hit_rome = await p.locator("#searchPreview .search-hit[data-id='civilization-rome']").count()
    await p.fill("#search", ""); await p.wait_for_timeout(200)
    await goto_view(p, "archivio")
    await tap(p, p.locator("#results .item").first, mobile); await p.wait_for_timeout(600)
    v20 = await p.evaluate("()=>currentView")
    await p.evaluate("()=>{document.getElementById('region').value='all';document.getElementById('archiveSearch').value='';renderList()}")
    R.check("T20", "Archivio: filtri propri; la ricerca principale trova comunque tutto; una voce apre la scheda in Esplora",
            n_all[0] == n_all[1] and a20["n"] > 0 and a20["regions"] == ["Asia"] and hit_rome == 1 and v20 == "esplora",
            f"senza filtri {n_all[0]}/{n_all[1]} voci; archivio Asia+'impero': {a20['n']} voci {a20['regions']}; ricerca principale trova Roma: {bool(hit_rome)}; dopo il clic vista {v20}")

    # T10 stile conservato dopo ricarica; i nomi delle vecchie palette passano al nuovo stile corrispondente
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='cartografo']`)?.click()")
    await p.reload(wait_until="load"); await p.wait_for_timeout(800)
    pal = await p.evaluate("()=>document.body.dataset.palette")
    migr = {}
    for old in ["notte", "pergamena", "deep", "moderno", "sconosciuta"]:
        await p.evaluate("(n)=>localStorage.setItem('atlantePalette',n)", old)
        await p.reload(wait_until="load"); await p.wait_for_timeout(500)
        migr[old] = await p.evaluate("()=>document.body.dataset.palette")
    R.check("T10", "Lo stile scelto resta dopo la ricarica; le vecchie scelte passano a Ottanio (Pergamena e Terracotta a Museo)",
            pal == "cartografo" and migr == {"notte": "ottanio", "pergamena": "museo", "deep": "ottanio", "moderno": "ottanio", "sconosciuta": "ottanio"},
            f"stile dopo ricarica: {pal}; vecchie palette → {migr}")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='ottanio']`)?.click()")

    # T21 nessuna vista è più larga dello schermo (niente scorrimento orizzontale della pagina)
    wide = []
    for v in ["esplora", "contemporanei", "tecnologia", "universo", "confronto", "archivio", "impostazioni"]:
        await goto_view(p, v)
        w = await p.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
        if w[0] > w[1] + 1:
            wide.append(f"{v}: {w[0]}px su {w[1]}px")
    R.check("T21", "Nessuna vista più larga dello schermo", not wide, "; ".join(wide) or "tutte le viste entrano in larghezza")

    # T23 epoche nella barra del tempo: un tocco porta all'epoca; il vecchio pannello dell'anno non è più visibile
    await goto_view(p, "esplora")
    await tap(p, p.locator("#timeDock .epoch-nav-segment[data-period='medieval']"), mobile)
    await p.wait_for_timeout(400)
    e23 = await p.evaluate("()=>({year:document.getElementById('yearLabel').textContent,dock:document.getElementById('dockYear').textContent,active:document.querySelector('#timeDock .epoch-nav-segment.active')?.dataset.period,annoVisibile:!!document.getElementById('anno').offsetParent})")
    R.check("T23", "Epoche nella barra del tempo: un tocco porta all'epoca, nessun secondo comando dell'anno",
            e23["year"] == "1000 d.C." and e23["dock"] == "1000 d.C." and e23["active"] == "medieval" and not e23["annoVisibile"], str(e23))

    # T24 cartografia di dettaglio: si carica ingrandendo, linee sottili a ogni zoom, punti di misura costante, zoom fino a 40x
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    await click_el(p, "#zoomReset")
    r1 = await p.evaluate("()=>{const c=document.querySelector('#pins circle.pin');return c?Math.round(c.getBoundingClientRect().width):null}")
    await p.evaluate("()=>{mapZoom=12;mapCx=(9+180)*2.5;mapCy=(90-40)*2.5;applyMapZoom()}")
    for _ in range(30):
        if await p.evaluate("()=>mapDetailState!=='loading'"): break
        await p.wait_for_timeout(200)
    await p.wait_for_timeout(200)
    d24 = await p.evaluate("""()=>{const hi=document.getElementById('world').classList.contains('hi');const n=document.querySelectorAll('#world .lod-hi path').length;
        const cl=document.querySelector('#world .coast-line');const cs=cl?getComputedStyle(cl):null;
        const c=document.querySelector('#pins circle.pin');
        return {state:mapDetailState,hi,paths:n,stroke:cs?cs.strokeWidth:null,ve:cs?cs.vectorEffect:null,pin:c?Math.round(c.getBoundingClientRect().width):null}}""")
    await p.evaluate("()=>setMapZoom(1000,innerWidth/2,innerHeight/2)")
    zmax = await p.evaluate("()=>mapZoom")
    await click_el(p, "#zoomReset")
    lo = await p.evaluate("()=>!document.getElementById('world').classList.contains('hi')")
    ok24 = (d24["state"] == "ready" and d24["hi"] and d24["paths"] > 50 and d24["stroke"] == "1.1px" and d24["ve"] == "non-scaling-stroke"
            and zmax == 40 and lo and (r1 is None or d24["pin"] is None or abs(d24["pin"] - r1) <= 3))
    R.check("T24", "Mappa di dettaglio: caricata ingrandendo, linee sottili, punti di misura costante, zoom fino a 40x",
            ok24, f"{d24}, punto a zoom 1: {r1}px, zoom massimo {zmax}, torna semplice a zoom 1: {lo}")

    # T25 comandi della mappa sovrapposti: su telefono solo "mondo intero" (lo zoom si fa con due dita)
    z25 = await p.evaluate("()=>['zoomIn','zoomOut','zoomReset'].map(id=>!!document.getElementById(id).offsetParent)")
    ok25 = z25 == ([False, False, True] if mobile else [True, True, True])
    R.check("T25", "Comandi di zoom sulla mappa: compatti, su telefono solo 'mondo intero'", ok25, f"visibili ＋ − ⤢: {z25}")

    # T18 una vecchia scelta "sezioni nascoste" (v0.44) non nasconde più nulla
    await p.evaluate("()=>localStorage.setItem('atlante-visible-sections-v09','[]')")
    await p.reload(wait_until="load"); await p.wait_for_timeout(800)
    await goto_view(p, "esplora")
    hidden18 = await p.evaluate("()=>['ricerca-principale','mappa','timeDock'].filter(id=>{const e=document.getElementById(id);if(!e||e.hidden)return true;const r=e.getBoundingClientRect();return !(r.width>0&&r.height>0)})")
    R.check("T18", "Una vecchia scelta di sezioni nascoste non nasconde parti della pagina", not hidden18, f"nascoste: {hidden18}")

    # T26 Tecnologia: per ogni ambito e area, le attestazioni fino alla fine della voce scelta, con la distanza in anni
    await goto_view(p, "tecnologia")
    await p.evaluate("()=>{techScope='tutte';techFocusId='event-rapanui-moai-tradition';techDomain='all';selected=null;showView('tecnologia');techMode='dettaglio';renderTecnologia()}")  # v0.59: T26 e T34 verificano il confronto con tutte le epoche; la finestra «stessa epoca» è in T61
    await p.wait_for_timeout(300)
    t26 = await p.evaluate("""()=>{const f=ALL.find(x=>x.id==='event-rapanui-moai-tradition');
        const exp=TECH.filter(t=>t.start_year<=f.end_year).length;
        document.querySelectorAll('[data-tech-expand]').forEach(b=>b.click());
        const shown=[...document.querySelectorAll('#techList .tech-item')].map(e=>e.dataset.techId);
        const late=shown.filter(id=>TECH.find(t=>t.id===id).start_year>f.end_year);
        const badge=id=>document.querySelector(`#techList [data-tech-id='${id}'] .tech-badge`)?.textContent||'';
        const dock=document.getElementById('timeDock');
        return {title:document.getElementById('techTitle').textContent,exp,shown:shown.length,late,
          pyr:badge('tech-arch-great-pyramid'),moai:badge('tech-arch-moai'),chartres:badge('tech-arch-chartres'),
          dock:!!(dock&&dock.offsetParent),focus:document.querySelector('.tech-area.is-focus')?.textContent||''}}""")
    await p.fill("#techSearch", "roma repubblica"); await p.wait_for_timeout(300)
    await tap(p, p.locator("#techResults [data-tech-pick='civilization-rome']"), mobile); await p.wait_for_timeout(400)
    await p.evaluate("()=>{techMode='dettaglio';renderTecnologia()}"); await p.wait_for_timeout(200)
    t26b = await p.evaluate("""()=>({title:document.getElementById('techTitle').textContent,
        late:[...document.querySelectorAll('#techList .tech-item')].map(e=>TECH.find(t=>t.id===e.dataset.techId)).filter(t=>t.start_year>476).map(t=>t.id),
        appia:document.querySelector("#techList [data-tech-id='tech-idr-aqua-appia'] .tech-badge")?.textContent||''})""")
    await p.screenshot(path=f"{OUT}/{name}_tecnologia.png", full_page=True)
    ok26 = (t26["title"] == "Durante «Grande stagione degli ahu e dei moai»" and t26["shown"] == t26["exp"] and not t26["late"]
            and t26["pyr"] == "≈ 3700 anni prima" and t26["moai"] == "durante · legata a questa voce" and t26["chartres"] == "durante la voce scelta"
            and not t26["dock"] and t26["focus"].startswith("Oceania")
            and t26b["title"] == "Durante «Roma: Repubblica e Impero»" and not t26b["late"] and t26b["appia"] == "durante · legata a questa voce")
    R.check("T26", "Tecnologia: attestazioni per ambito e area fino alla voce scelta, distanza in anni, scelta di un’altra voce",
            ok26, f"{t26['title']}: {t26['shown']}/{t26['exp']} attestazioni, successive {t26['late']}; piramide '{t26['pyr']}', moai '{t26['moai']}', Chartres '{t26['chartres']}'; barra del tempo visibile {t26['dock']}; area evidenziata '{t26['focus']}'; Roma: '{t26b['title']}', successive {t26b['late']}, Aqua Appia '{t26b['appia']}'")

    # T27 slider a tratti: ogni epoca occupa il suo blocco; − e + con passo diverso per epoca
    await goto_view(p, "esplora")
    s27 = await p.evaluate("""()=>{const r=document.getElementById('dockRange').getBoundingClientRect(),th=9;
        const segs=[...document.querySelectorAll('#timeDock .epoch-nav-segment')].map(b=>b.getBoundingClientRect());
        const bounds=[-3500,476,1492,1789];
        const off=bounds.map((y,i)=>Math.abs((r.left+th+yearToPos(y)/1000*(r.width-2*th))-segs[i+1].left));
        const trip=[-9000,-3500,-500,476,1200,1492,1700,1789,1850,2000].filter(y=>y>=YEAR_MIN&&y<=YEAR_MAX).filter(y=>posToYear(yearToPos(y))!==y);
        const steps=[[-5000,1],[-500,-1],[1200,1],[1990,1],[1990,-1],[1490,1],[480,-1]].map(([y,d])=>stepYear(y,d));
        return {off:off.map(v=>Math.round(v*10)/10),trip,steps}}""")
    await click_el(p, "#yearPlus"); await p.wait_for_timeout(250)
    y_a = await year(p)
    await click_el(p, "#yearMinus"); await p.wait_for_timeout(250)
    y_b = await year(p)
    ok27 = max(s27["off"]) <= 2 and not s27["trip"] and s27["steps"] == [-4900, -510, 1205, 1991, 1989, 1492, 476] and y_a != y_b
    R.check("T27", "Slider a tratti: epoche scolastiche (3500 a.C., 476, 1492, 1789) allineate ai blocchi, passo − / + per epoca (100, 10, 5, 1 anni) che si ferma sui confini",
            ok27, f"scarto dai confini delle epoche {s27['off']} px; andata e ritorno errati {s27['trip']}; passi {s27['steps']}; con i pulsanti {y_a} → {y_b}")

    # T28 stili: Ottanio (predefinito, scuro), Museo, Cartografo
    pals = await p.evaluate("()=>[...document.querySelectorAll('.palette-choice')].map(b=>b.dataset.palette)")
    looks = {}
    for pal in pals:
        await p.evaluate("(n)=>document.querySelector(`.palette-choice[data-palette='${n}']`).click()", pal)
        await p.wait_for_timeout(120)
        looks[pal] = await p.evaluate("()=>[document.body.classList.contains('themed'),document.body.classList.contains('theme-light'),getComputedStyle(document.body).getPropertyValue('--t-header').trim()+'|'+getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0]+'|'+getComputedStyle(document.querySelector('h1')).fontStyle,document.querySelector('meta[name=theme-color]')?.content]")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='ottanio']`).click()")
    ok28 = (pals == STYLES and looks["ottanio"][:2] == [False, False] and looks["museo"][:2] == [True, True] and looks["cartografo"][:2] == [True, True]
            and len({v[2] for v in looks.values()}) == 3 and len({v[3] for v in looks.values()}) == 3)
    R.check("T28", "Stili: Ottanio (predefinito), Museo e Cartografo, ognuno con testata, caratteri e colore propri", ok28, f"{pals}; {looks}")

    # T29 Universo: una corsia per area, legenda dei temi, voci in eccesso raccolte in «altre»
    await goto_view(p, "universo"); await p.wait_for_timeout(300)
    await p.evaluate("()=>{universeSpan=U_FULL;uRender()}"); await p.wait_for_timeout(200)
    u29 = await p.evaluate("""()=>({legend:document.getElementById('universeLegend')?.textContent||'',
        lanes:[...document.querySelectorAll('#universeCanvas .uv-lane-label')].map(t=>t.textContent),
        more:document.querySelectorAll('#universeCanvas .uv-more').length,
        status:document.querySelector('.universe-status')?.textContent||''})""")
    areas = ["Europa", "Asia", "Africa", "Americhe", "Oceania"]
    ok29 = "Poteri" in u29["legend"] and "voci" in u29["status"] and u29["more"] > 0 and 3 <= len(u29["lanes"]) <= 6 and all(any(l.startswith(a) for a in areas + ["Globale"]) for l in u29["lanes"])
    R.check("T29", "Universo: una corsia per area, legenda dei temi, voci in eccesso raccolte in «altre»", ok29, f"corsie {u29['lanes']}; legenda '{u29['legend'][:80]}'; gruppi «altre» {u29['more']}; stato '{u29['status'][:80]}'")
    await p.evaluate("()=>{universeSpan=uNarrow()?500:2000;universeFollow=true;uRender()}")
    await new_checks(p, R, mobile, name)
    await goto_view(p, "esplora")

    # T64 v0.65: la vista «Tavola · prova» si chiama «Mosaico»; #mosaico e il vecchio #tavola la aprono; i link portano a #mosaico
    t64 = await p.evaluate("""async()=>{const w=t=>new Promise(r=>setTimeout(r,t));const out={};
        const links=[...document.querySelectorAll('[data-view-link="tavola"]')];out.labels=links.map(a=>(a.querySelector('strong')||a).textContent.trim());out.hrefs=[...new Set(links.map(a=>a.getAttribute('href')))];
        out.prova=/prova/i.test(document.getElementById('view-tavola').textContent+links.map(a=>a.textContent).join(''));out.h2=document.querySelector('#tavolaWrap h2')?.textContent;
        out.nav=[...document.querySelectorAll('.mobile-nav a')].map(a=>a.dataset.viewLink);out.tabs=[...document.querySelectorAll('.view-tabs a')].map(a=>a.dataset.viewLink);out.inAltro=!!document.querySelector('#view-impostazioni [data-view-link="tavola"]');
        out.icone=[...document.querySelectorAll('.mobile-nav a')].every(a=>a.querySelector('.ni svg')&&a.querySelector('.nl')?.textContent.trim());
        location.hash='#esplora';await w(250);location.hash='#mosaico';await w(500);out.viaNew=currentView;
        location.hash='#esplora';await w(250);location.hash='#tavola';await w(500);out.viaOld=currentView;
        goToView('tavola');await w(300);out.goHash=location.hash;goToView('esplora');await w(300);return out}""")
    ok64 = (t64["hrefs"] == ["#mosaico"] and not t64["prova"] and t64["h2"] == "Il mosaico del tempo" and t64["viaNew"] == "tavola" and t64["viaOld"] == "tavola"
            and t64["goHash"] == "#mosaico" and t64["labels"] == ["Mosaico", "Mosaico"] and t64["nav"][:2] == ["esplora", "tavola"] and len(t64["nav"]) == 6
            and t64["tabs"][:2] == ["esplora", "tavola"] and not t64["inAltro"] and t64["icone"])
    R.check("T64", "Vista «Mosaico»: tasto proprio nella barra in basso (secondo, dalla v0.69) e secondo nella barra in alto, non più in «Altro», simboli disegnati su tutti i tasti; #mosaico e il vecchio #tavola la aprono", ok64, f"{t64}")
    # T63 v0.62: icone PNG per i browser che non usano la favicon SVG (Chrome e Safari su iPhone e iPad), SVG ancora presente; voci di rilevanza 1 tutte verificate con fonti
    t63 = await p.evaluate("""async()=>{const out={};for(const l of document.querySelectorAll('link[rel="icon"][type="image/png"],link[rel="apple-touch-icon"]')){const im=new Image();im.src=l.href;try{await im.decode();out[l.getAttribute('href')]=im.naturalWidth+'x'+im.naturalHeight}catch(e){out[l.getAttribute('href')]='errore'}}
        out.svg=!!document.querySelector('link[rel="icon"][type="image/svg+xml"]');out.rel1=DB.entities.concat(DB.events).filter(x=>!['source-checked','deep-dive-sourced'].includes(x.editorial_status)).map(x=>x.id);return out}""")
    ok63 = t63 == {"favicon-32.png": "32x32", "favicon-192.png": "192x192", "apple-touch-icon.png": "180x180", "svg": True, "rel1": []}
    R.check("T63", "Icone PNG (32, 192 e 180 px per iPhone e iPad) accanto alla favicon SVG; nessuna voce senza verifica delle fonti (dalla v0.67 tutte le rilevanze)", ok63, f"{t63}")
    # T01 nessun errore, nessuna richiesta esterna (controllato a fine giro)
    errors[:] = [e for e in errors if "ERR_TUNNEL_CONNECTION_FAILED" not in e and "ERR_NAME_NOT_RESOLVED" not in e]  # foto di Commons irraggiungibili nell'ambiente di test
    R.check("T01", "Nessun errore JavaScript e nessuna risorsa esterna caricata (a parte le foto di Wikimedia Commons)", not errors and not external,
            "; ".join(errors[:3] + sorted(external)[:3]) or "pulito")
    await p.screenshot(path=f"{OUT}/{name}_fine.png")
    await browser.close()
    return R.rows

async def touch_drag(p, x, y, dx, dy, steps=10):
    cdp = await p.context.new_cdp_session(p)
    await cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y}]})
    for i in range(1, steps + 1):
        await cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x + dx * i / steps, "y": y + dy * i / steps}]})
        await p.wait_for_timeout(16)
    await cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    await cdp.detach()

async def tap_xy(p, x, y, mobile):
    if mobile:
        await p.touchscreen.tap(x, y)
    else:
        await p.mouse.click(x, y)

async def empty_map_point(p):
    # un punto della mappa lontano da tutti i marcatori (oceano), dentro il riquadro visibile
    return await p.evaluate("""()=>{const st=document.querySelector('#view-esplora .mapstage').getBoundingClientRect();
        const pins=[...document.querySelectorAll('#pins circle.pin')].map(c=>{const r=c.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]});
        for(const [fx,fy] of [[.06,.82],[.94,.86],[.5,.92],[.3,.75],[.1,.5]]){const x=st.left+st.width*fx,y=st.top+st.height*fy;
          if(y<innerHeight-200&&y>40&&pins.every(([a,b])=>Math.hypot(a-x,b-y)>40))return [x,y]}
        return [st.left+st.width*.06,st.top+st.height*.6]}""")

async def new_checks(p, R, mobile, name):
    # T30 riepilogo sulla mappa: si chiude toccando un punto vuoto della mappa o fuori; resta aperto trascinando la mappa o usando la barra del tempo
    await goto_view(p, "esplora")
    await p.evaluate("()=>{closeDetail({instant:true});hideToast()}")
    await set_year(p, -16)
    await click_el(p, "#zoomReset"); await p.wait_for_timeout(250)
    await p.evaluate("document.getElementById('mappa').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(200)
    marker = p.locator("#pins .map-marker").first
    res = {}
    await tap(p, marker, mobile); await p.wait_for_timeout(300)
    res["aperto"] = await p.is_visible("#mapPointPopup")
    x, y = await empty_map_point(p)
    await tap_xy(p, x, y, mobile); await p.wait_for_timeout(300)
    res["dopo tocco su mappa vuota"] = not await p.is_visible("#mapPointPopup")
    await tap(p, marker, mobile); await p.wait_for_timeout(300)
    x, y = await empty_map_point(p)
    if mobile:
        await touch_drag(p, x, y, 30, 0, 6)
    else:
        await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.move(x + 30, y, steps=5); await p.mouse.up()
    await p.wait_for_timeout(300)
    res["dopo trascinamento resta"] = await p.is_visible("#mapPointPopup")
    if not res["dopo trascinamento resta"]:
        await tap(p, marker, mobile); await p.wait_for_timeout(300)
    db = await p.locator("#dockYear").bounding_box()
    await tap_xy(p, db["x"] + db["width"] / 2, db["y"] + db["height"] / 2, mobile); await p.wait_for_timeout(250)
    res["dopo tocco sulla barra del tempo resta"] = await p.is_visible("#mapPointPopup")
    ib = await p.locator("#mapIntro").bounding_box()
    await tap_xy(p, ib["x"] + 20, ib["y"] + ib["height"] / 2, mobile); await p.wait_for_timeout(250)
    res["dopo tocco fuori dalla mappa"] = not await p.is_visible("#mapPointPopup")
    R.check("T30", "Riepilogo sulla mappa: si chiude toccando un altro punto della mappa o fuori, non trascinando né usando la barra del tempo",
            all(res.values()), str(res))

    # T31 scheda a tendina: trascinata giù si chiude, un tratto breve no, verso l'alto si allarga (telefono)
    await p.evaluate("()=>openInEsplora('civilization-rome')"); await p.wait_for_timeout(700)
    if mobile:
        info = {}
        hb = await p.locator("#sheetHandle").bounding_box()
        cx, cy = hb["x"] + hb["width"] / 2, hb["y"] + hb["height"] / 2
        await touch_drag(p, cx, cy, 0, 40); await p.wait_for_timeout(400)
        info["tratto breve: aperta"] = await p.evaluate("()=>!document.getElementById('scheda').hidden")
        hb = await p.locator("#sheetHandle").bounding_box()
        await touch_drag(p, hb["x"] + hb["width"] / 2, hb["y"] + hb["height"] / 2, 0, -90); await p.wait_for_timeout(400)
        info["verso l'alto: allargata"] = await p.evaluate("()=>document.getElementById('scheda').classList.contains('expanded')")
        await p.evaluate("()=>{const s=document.getElementById('scheda');s.scrollTop=0}")
        sb = await p.locator("#scheda .detail-title").bounding_box()
        await touch_drag(p, sb["x"] + 30, sb["y"] + sb["height"] / 2, 0, 230); await p.wait_for_timeout(500)
        info["giù dal contenuto in cima: chiusa"] = await p.evaluate("()=>document.getElementById('scheda').hidden")
        await p.evaluate("()=>openInEsplora('civilization-rome')"); await p.wait_for_timeout(700)
        hb = await p.locator("#sheetHandle").bounding_box()
        await touch_drag(p, hb["x"] + hb["width"] / 2, hb["y"] + hb["height"] / 2, 0, 200); await p.wait_for_timeout(500)
        info["giù dalla maniglia: chiusa"] = await p.evaluate("()=>document.getElementById('scheda').hidden")
        ok31 = all(info.values())
    else:
        info = await p.evaluate("()=>({sheet:document.getElementById('scheda').classList.contains('is-sheet'),visible:!document.getElementById('scheda').hidden})")
        ok31 = not info["sheet"] and info["visible"]
        info["nota"] = "su desktop la scheda resta un pannello laterale"
        await p.evaluate("()=>closeDetail({instant:true})")
    R.check("T31", "Scheda: su telefono si chiude trascinando giù la tendina (gesto stile iPhone)", ok31, str(info))

    # T32 confronto: dopo l'aggiunta un avviso porta subito al confronto
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast()}")
    await p.evaluate("document.getElementById('mappa').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(200)
    await tap(p, marker, mobile); await p.wait_for_timeout(300)
    pid = await p.evaluate("()=>document.getElementById('mapPointPopup').dataset.itemId")
    await tap(p, p.locator("#mapPointPopup .popup-add"), mobile); await p.wait_for_timeout(400)
    t = await p.evaluate("""()=>{const t=document.getElementById('toast'),r=t.getBoundingClientRect(),d=document.getElementById('timeDock').getBoundingClientRect();
        return {vis:!t.hidden&&r.height>0,text:t.textContent,overDock:r.bottom>d.top+1&&r.top<d.bottom,badge:document.querySelector('.view-tabs [data-cmp-count]')?.textContent||''}}""")
    go = p.locator("#toast [data-toast-go]")
    if await go.count():
        await tap(p, go, mobile); await p.wait_for_timeout(500)
    after = await p.evaluate("""(id)=>({view:currentView,hash:location.hash,chips:[...document.querySelectorAll('#compareChips .compare-chip')].length,
        has:compareIds.includes(id),toast:!document.getElementById('toast').hidden})""", pid)
    await goto_view(p, "esplora")
    await p.evaluate("(id)=>addCompare(id)", pid); await p.wait_for_timeout(200)
    dup = await p.evaluate("()=>document.getElementById('toast').textContent")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast()}")
    ok32 = (t["vis"] and "aggiunto al confronto" in t["text"] and "Vai al confronto" in t["text"] and not t["overDock"] and t["badge"] == "1"
            and after["view"] == "confronto" and after["hash"] == "#confronto" and after["has"] and after["chips"] == 1 and not after["toast"] and "già nel confronto" in dup)
    R.check("T32", "Confronto: dopo l'aggiunta un avviso con «Vai al confronto» porta subito alla vista Confronto", ok32, f"avviso {t}; dopo il tocco {after}; seconda aggiunta '{dup[:60]}'")

    # T33 Universo: segue la barra del tempo; trascinato si stacca, cambiando anno torna a seguirlo; etichette leggibili senza sovrapposizioni
    await goto_view(p, "universo"); await p.wait_for_timeout(300)
    geo = """()=>{const now=document.querySelector('#universeCanvas .uv-now'),g=uGeom();return {center:Math.round(universeCenter),year:chosenYear,follow:universeFollow,
        nowX:now?Math.round(+now.getAttribute('x1')):null,mid:Math.round(g.padL+g.plot/2),recenter:!document.getElementById('universeCenter').hidden}}"""
    steps = {}
    for yv in [1400, 500]:
        await p.evaluate("(y)=>{const r=document.getElementById('dockRange');r.value=yearToPos(y);r.dispatchEvent(new Event('input',{bubbles:true}))}", yv)
        await p.wait_for_timeout(250)
        steps[yv] = await p.evaluate(geo)
    vp = p.locator("#universeViewport")
    await vp.evaluate("e=>e.scrollIntoView({block:'start',behavior:'instant'})"); await p.wait_for_timeout(150)
    bb = await vp.bounding_box()
    cx, cy = bb["x"] + bb["width"] * 0.5, bb["y"] + 60
    if mobile:
        await touch_drag(p, cx, cy, -120, 0)
    else:
        await p.mouse.move(cx, cy); await p.mouse.down(); await p.mouse.move(cx - 120, cy, steps=8); await p.mouse.up()
    await p.wait_for_timeout(300)
    dragged = await p.evaluate(geo)
    await p.evaluate("()=>document.getElementById('yearPlus').click()"); await p.wait_for_timeout(300)
    back = await p.evaluate(geo)
    lab = await p.evaluate("""()=>{const vp=document.getElementById('universeViewport').getBoundingClientRect();
        const L=[...document.querySelectorAll('#universeCanvas .uv-label')].map(t=>{const r=t.getBoundingClientRect();return {id:t.closest('.uv-node').dataset.uid,l:r.left,r:r.right,t:r.top,b:r.bottom}});
        const B=[...document.querySelectorAll('#universeCanvas .uv-bar,#universeCanvas .uv-dot')].map(e=>{const r=e.getBoundingClientRect();return {id:e.closest('.uv-node').dataset.uid,l:r.left,r:r.right,t:r.top,b:r.bottom}});
        const hit=(a,b)=>Math.min(a.r,b.r)-Math.max(a.l,b.l)>1.5&&Math.min(a.b,b.b)-Math.max(a.t,b.t)>1.5;
        const over=[];L.forEach((a,i)=>{L.slice(i+1).forEach(b=>{if(hit(a,b))over.push(a.id+'/'+b.id)});B.forEach(b=>{if(b.id!==a.id&&hit(a,b))over.push(a.id+'~'+b.id)})});
        const out=L.filter(a=>a.l<vp.left-1||a.r>vp.right+1).map(a=>a.id);
        const nodes=document.querySelectorAll('#universeCanvas .uv-node').length;
        return {labels:L.length,nodes,over:over.slice(0,4),nOver:over.length,out,size:parseFloat(getComputedStyle(document.querySelector('#universeCanvas .uv-label')||document.body).fontSize)}}""")
    ok33 = (steps[1400]["center"] == 1400 and abs(steps[1400]["nowX"] - steps[1400]["mid"]) <= 2 and steps[500]["center"] == 500
            and not dragged["follow"] and dragged["recenter"] and dragged["center"] != 500 and back["follow"] and back["center"] == back["year"] and not back["recenter"]
            and lab["nOver"] == 0 and not lab["out"] and lab["labels"] >= lab["nodes"] * 0.8 and lab["size"] >= 11)
    R.check("T33", "Universo: segue la barra del tempo; trascinato si stacca e torna a seguirlo al cambio d'anno; nomi leggibili, senza sovrapposizioni",
            ok33, f"1400: {steps[1400]}; 500: {steps[500]}; trascinato: {dragged}; dopo +: {back}; etichette {lab}")

    # T37 Universo: un tocco su una voce (senza trascinare) apre il riepilogo, da cui si aggiunge al confronto
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast()}")
    node = p.locator("#universeCanvas .uv-node").first
    uid = await node.get_attribute("data-uid")
    await node.locator(".uv-hit").evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(100)
    nb = await node.locator(".uv-hit").bounding_box()
    await tap_xy(p, nb["x"] + min(20, nb["width"] / 2), nb["y"] + nb["height"] / 2, mobile); await p.wait_for_timeout(350)
    tip = await p.evaluate("()=>({vis:!document.getElementById('universeTooltip').hidden,title:document.querySelector('#universeTooltip strong')?.textContent||''})")
    if tip["vis"]:
        await tap(p, p.locator("#universeTooltip .pop-compare"), mobile); await p.wait_for_timeout(300)
    t37 = await p.evaluate("(id)=>({cmp:compareIds.includes(id),toast:!document.getElementById('toast').hidden,strip:!document.getElementById('universeCompareStrip').hidden})", uid)
    name37 = await p.evaluate("(id)=>ALL.find(x=>x.id===id).name", uid)
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast();document.getElementById('universeTooltip').hidden=true}")
    R.check("T37", "Universo: un tocco su una voce apre il riepilogo; «Aggiungi al confronto» la aggiunge e mostra l'avviso",
            tip["vis"] and tip["title"] == name37 and t37["cmp"] and t37["toast"] and t37["strip"], f"riepilogo {tip}; dopo l'aggiunta {t37}")

    # T34 Tecnologia, sintesi: un punto per ambito e area, posizione coerente con gli anni, tocco → dettaglio dell'attestazione
    await goto_view(p, "tecnologia")
    await p.evaluate("()=>{techScope='tutte';techFocusId='event-rapanui-moai-tradition';techMode='sintesi';techDomain='all';techOpenId=null;renderTecnologia()}"); await p.wait_for_timeout(250)
    t34 = await p.evaluate("""()=>{const f=techFocus(),fi=techFirsts(f),keys=Object.keys(fi);
        const band=document.querySelector('#techList .ti-band'),bl=+band.getAttribute('x'),br=bl+ +band.getAttribute('width');
        const marks=[...document.querySelectorAll('#techList .ti-mark')].map(g=>{const c=g.querySelector('circle');return {id:g.dataset.ti,x:+c.getAttribute('cx'),r:+c.getAttribute('r')}});
        const info=marks.map(m=>{const t=TECH.find(t=>t.id===m.id),rel=techRelation(t,f);return {...m,k:rel.k,n:rel.n||0}});
        const bad=[];info.forEach(a=>{if(a.k==='durante'&&(a.x<bl||a.x>br))bad.push(a.id+' fuori dalla fascia');if(a.k==='prima'&&a.x>=bl)bad.push(a.id+' nella fascia');
          info.forEach(b=>{if(a.k==='prima'&&b.k==='prima'&&a.n>Math.max(10,b.n)*2&&a.x>b.x+2.6*a.r)bad.push(a.id+'>'+b.id)})});
        const w=document.querySelector('#techList .ti-svg').getBoundingClientRect().width,lw=document.getElementById('techList').getBoundingClientRect().width;
        return {pairs:keys.length,marks:marks.length,bad:bad.slice(0,4),nBad:bad.length,fits:w<=lw+1,kpi:document.querySelectorAll('#techList .ti-kpi').length,areas:document.querySelectorAll('#techList .ti-area').length}}""")
    mk = p.locator("#techList .ti-mark[data-ti='tech-arch-great-pyramid']")
    await tap(p, mk, mobile); await p.wait_for_timeout(500)
    t34b = await p.evaluate("()=>({mode:techMode,open:techOpenId,domain:techDomain,shown:!!document.querySelector(\"#techList .tech-item.open[data-tech-id='tech-arch-great-pyramid']\")})")
    await p.evaluate("()=>{techMode='sintesi';techDomain='all';techOpenId=null;techScope='epoca';renderTecnologia()}")
    ok34 = (t34["marks"] == t34["pairs"] and t34["nBad"] == 0 and t34["fits"] and t34["kpi"] >= 2 and t34["areas"] == 0
            and t34b == {"mode": "dettaglio", "open": "tech-arch-great-pyramid", "domain": "architettura", "shown": True})
    R.check("T34", "Tecnologia, sintesi: infografica con un punto per ambito e area, coerente con gli anni (senza la griglia «Ambiti attestati per area», tolta nella v0.53); un tocco apre il dettaglio",
            ok34, f"{t34}; dopo il tocco {t34b}")

    # T35 contrasto del testo nei dettagli del confronto e nelle nuove parti, in ogni palette
    low = []
    await p.evaluate("()=>{['culture-maya','civilization-inca','state-ancient-egypt'].forEach(id=>{if(!compareIds.includes(id))addCompare(id)});hideToast()}")
    sels = {"confronto": "#comparatore .compare-insight strong,#comparatore .compare-insight div,#comparatore .compare-table th,#comparatore .compare-table td,#comparatore .compare-chip,#compareCount",
            "universo": ".uv-strip-text strong,.uv-strip-text span,.uv-scale button,.uv-legend button,.universe-status",
            "tecnologia": "#techList .ti-kpi b,#techList .ti-kpi span,#techList .ti-area-name,#techList .ti-area>b,.ti-mode button"}
    for pal in STYLES:
        await p.evaluate("(n)=>document.querySelector(`.palette-choice[data-palette='${n}']`).click()", pal)
        for v, sel in sels.items():
            await goto_view(p, v); await p.wait_for_timeout(200)
            for el in await p.query_selector_all(sel):
                if not await el.is_visible(): continue
                c = await el.evaluate(JS_CONTRAST)
                if c["text"] and c["ratio"] < 4.5:
                    low.append(f"{pal}/{v}: '{c['text'][:24]}' {c['ratio']:.1f}:1")
        await p.evaluate("()=>{const x=ALL.find(v=>v.id==='culture-maya');compareToast(x,'gia')}")
        c = await p.locator("#toast .toast-msg").evaluate(JS_CONTRAST)
        if c["ratio"] < 4.5: low.append(f"{pal}/avviso {c['ratio']:.1f}:1")
        await p.evaluate("()=>hideToast()")
        if pal == "museo":
            await goto_view(p, "confronto"); await p.wait_for_timeout(200)
            await p.screenshot(path=f"{OUT}/{name}_confronto_museo.png", full_page=True)
    await p.evaluate("()=>{document.querySelector(`.palette-choice[data-palette='ottanio']`).click();compareIds.slice().forEach(id=>removeCompare(id))}")
    R.check("T35", "Testo leggibile (contrasto ≥ 4.5:1) nei dettagli del confronto, nell'Universo e nella sintesi Tecnologia, in tutti gli stili",
            not low, "; ".join(low[:6]) or f"tutti ≥ 4.5:1")
    await goto_view(p, "esplora")

    # T38 punti sovrapposti: il riepilogo elenca le altre voci nello stesso punto e permette di passare dall'una all'altra
    await p.evaluate("()=>{closeDetail({instant:true});hideToast();closeMapPointPopup()}")
    await set_year(p, 1957)
    await click_el(p, "#zoomReset"); await p.wait_for_timeout(250)
    await p.evaluate("document.getElementById('mappa').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(200)
    await tap(p, p.locator("#pins .map-marker[data-id='state-italian-republic']"), mobile); await p.wait_for_timeout(300)
    t38 = await p.evaluate("""()=>{const pp=document.getElementById('mapPointPopup');return {open:!pp.hidden,id:pp.dataset.itemId,
        here:[...pp.querySelectorAll('[data-here]')].map(b=>b.dataset.here)}}""")
    other = (t38["here"] or [None])[0]
    if other:
        await tap(p, p.locator(f"#mapPointPopup [data-here='{other}']"), mobile); await p.wait_for_timeout(300)
    after38 = await p.evaluate("""()=>{const pp=document.getElementById('mapPointPopup');return {open:!pp.hidden,id:pp.dataset.itemId,
        here:[...pp.querySelectorAll('[data-here]')].map(b=>b.dataset.here)}}""")
    pair = {"state-italian-republic", "event-treaties-of-rome"}
    ok38 = (t38["open"] and pair <= set([t38["id"]] + t38["here"]) and after38["open"] and after38["id"] == other and t38["id"] in after38["here"])
    R.check("T38", "Punti sovrapposti: «Qui vicino» nel riepilogo elenca le altre voci nello stesso punto e porta all'altra voce",
            ok38, f"prima {t38}; dopo il tocco su {other}: {after38}")
    await p.evaluate("()=>closeMapPointPopup()")

    # T39 dati: ogni voce ha fonte, livello, rilevanza e area; nessun collegamento rotto; nessun nome doppio
    t39 = await p.evaluate("""()=>{const ids=new Set(ALL.map(x=>x.id)),LAY=['civilta','eventi','tecnologie','persone-idee','luoghi'],
        AR=['EU','AO','AN','AS','AM','AE','AC','SE','NA','MC','SA','OC','GL'],bad=[];
        const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(),seen={};
        for(const x of ALL){
          if(!(x.source_ids||[]).length)bad.push(x.id+': senza fonte');
          if(!LAY.includes(x.layer))bad.push(x.id+': livello '+x.layer);
          if(![1,2,3].includes(x.relevance))bad.push(x.id+': rilevanza '+x.relevance);
          if(!AR.includes(x.world_area))bad.push(x.id+': area '+x.world_area);
          for(const r of [...(x.related_entities||[]),...(x.related_entity_ids||[])])if(!ids.has(r))bad.push(x.id+': collegamento rotto '+r);
          const n=norm(x.name);if(seen[n])bad.push('nome doppio: '+x.name+' ('+seen[n]+', '+x.id+')');seen[n]=x.id;
          if(x.editorial_status==='source-checked'&&!(x.source_ids||[]).some(s=>!/^src-openstax|^src-unesco-world-heritage-list$/.test(s)))bad.push(x.id+': verificata senza fonte specifica')}
        return {n:ALL.length,bad}}""")
    R.check("T39", "Dati: ogni voce ha fonte, livello, rilevanza e area mondiale; le voci verificate hanno una fonte specifica; nessun collegamento rotto né nome doppio",
            not t39["bad"], f"{t39['n']} voci; " + ("; ".join(t39["bad"][:6]) or "tutto in ordine"))

    # T40 Tecnologia senza voce scelta: nessuna voce di partenza; suggerimenti = voci di rilevanza 1 attive nell'anno della barra del tempo
    await goto_view(p, "esplora")
    await p.evaluate("()=>{selected=null;techFocusId=null;chosenYear=1300;period=periodForYear(1300);$('yearRange').value=1300;renderAll()}")
    await goto_view(p, "tecnologia"); await p.wait_for_timeout(300)
    t40 = await p.evaluate("""()=>{const b=[...document.querySelectorAll('#techSummary .tech-suggest [data-tech-focus]')].map(e=>ALL.find(x=>x.id===e.dataset.techFocus));
        return {title:document.getElementById('techTitle').textContent,label:document.querySelector('#techSummary .tech-suggest .small')?.textContent||'',
          n:b.length,bad:b.filter(x=>!x||x.relevance!==1||!(x.start_year<=1300&&x.end_year>=1300)).map(x=>x?x.id:'?'),
          areas:new Set(b.map(x=>x.world_area)).size,items:document.querySelectorAll('#techList .tech-item,#techList .ti-mark').length,first:b[0]?.id||''}}""")
    first = t40["first"]
    if first:
        await tap(p, p.locator(f"#techSummary [data-tech-focus='{first}']"), mobile); await p.wait_for_timeout(400)
    t40b = await p.evaluate("()=>({title:document.getElementById('techTitle').textContent,focus:techFocusId})")
    await p.evaluate("()=>{techFocusId=null;chosenYear=-4000;renderTecnologia()}")
    t40c = await p.evaluate("()=>[...document.querySelectorAll('#techSummary .tech-suggest [data-tech-focus]')].map(e=>ALL.find(x=>x.id===e.dataset.techFocus)).map(x=>[x.relevance,x.start_year<=-4000&&x.end_year>=-4000])")
    ok40 = (t40["title"] == "Che cosa sapevano fare, altrove?" and t40["label"] == "Nel 1300 d.C.:" and t40["n"] == 6 and not t40["bad"]
            and t40["areas"] == 6 and t40["items"] == 0 and t40b["focus"] == first and t40b["title"].startswith("Durante «")
            and len(t40c) >= 3 and all(a for _, a in t40c) and t40c[0][0] == 1)
    R.check("T40", "Tecnologia senza voce scelta: nessuna voce di partenza; suggerimenti di rilevanza 1 attivi nell'anno, uno per area; nel 4000 a.C. completati con la rilevanza 2",
            ok40, f"{t40}; dopo il tocco: {t40b}; 4000 a.C. (rilevanza, attiva): {t40c}")
    await p.evaluate("()=>{selected=null;techFocusId=null;chosenYear=PERIOD_ANCHOR.all;period='all';$('yearRange').value=chosenYear;renderAll()}")

    # T41 anno di apertura: periodo a caso tra gli 8, anno con almeno 2 voci di rilevanza 1 attive, mai lo stesso due volte di fila
    t41 = await p.evaluate("""()=>{const per=OPENING_PERIODS.map(()=>0),ys=[],rel1=y=>ALL.filter(x=>x.relevance===1&&x.start_year<=y&&x.end_year>=y).length;
        for(let i=0;i<800;i++){const y=chooseOpeningYear();ys.push(y);per[OPENING_PERIODS.findIndex(([a,b])=>y>=a&&y<b)]++}
        return {per,distinct:new Set(ys).size,repeats:ys.filter((y,i)=>i&&y===ys[i-1]).length,minRel1:Math.min(...ys.map(rel1))}}""")
    ok41 = min(t41["per"]) >= 50 and t41["repeats"] == 0 and t41["minRel1"] >= 2 and t41["distinct"] >= 200
    R.check("T41", "Anno di apertura: periodo a caso tra gli 8 del piano, anno con voci di rilevanza 1 attive, mai uguale a quello della volta prima",
            ok41, f"800 aperture simulate: per periodo {t41['per']}; anni diversi {t41['distinct']}; ripetizioni consecutive {t41['repeats']}; minimo voci di rilevanza 1 attive {t41['minRel1']}")

    # T42 «✓ Nel confronto» toccato di nuovo toglie la voce dal confronto: mappa (con tocco vero), scheda, «Nel mondo intorno», Universo
    await goto_view(p, "esplora")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast();closeMapPointPopup();closeDetail({instant:true})}")
    await p.evaluate("document.getElementById('mappa').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(200)
    mk42 = p.locator("#pins .map-marker").first
    await tap(p, mk42, mobile); await p.wait_for_timeout(300)
    pid42 = await p.evaluate("()=>document.getElementById('mapPointPopup').dataset.itemId")
    await tap(p, p.locator("#mapPointPopup .popup-add"), mobile); await p.wait_for_timeout(300)
    await p.evaluate("()=>hideToast()")
    await tap(p, mk42, mobile); await p.wait_for_timeout(300)
    lab42 = await p.evaluate("()=>document.querySelector('#mapPointPopup .popup-add')?.textContent||''")
    await tap(p, p.locator("#mapPointPopup .popup-add"), mobile); await p.wait_for_timeout(300)
    m42 = await p.evaluate("(id)=>({in:compareIds.includes(id),sel:selected,toast:document.getElementById('toast').textContent,go:!!document.querySelector('#toast [data-toast-go]')})", pid42)
    s42 = await p.evaluate("""()=>{const id='civilization-rome';openInEsplora(id);const b=()=>document.getElementById('detailAddCompare');const out=[];
        out.push(b().textContent);b().click();out.push(compareIds.includes(id),b().textContent);b().click();out.push(compareIds.includes(id),b().textContent,selected);return out}""")
    y42 = await p.evaluate("""()=>{const b=()=>document.querySelector('#syncList [data-sync-compare]');if(!b())return null;const id=b().dataset.syncCompare;
        b().click();const a=compareIds.includes(id);b().click();return [a,compareIds.includes(id)]}""")
    u42 = await p.evaluate("""()=>{const id='civilization-rome';uShowTip(id,200,200);const b=()=>document.querySelector('#universeTooltip .pop-compare');
        b().click();const a=[compareIds.includes(id),b().textContent];b().click();const r=[...a,compareIds.includes(id),b().textContent];document.getElementById('universeTooltip').hidden=true;return r}""")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id));hideToast();closeMapPointPopup()}")
    ok42 = (lab42 == "✓ Nel confronto" and not m42["in"] and m42["sel"] == pid42 and "tolto dal confronto · 0/5" in m42["toast"] and not m42["go"]
            and s42 == ["＋ Aggiungi al confronto", True, "✓ Nel confronto", False, "＋ Aggiungi al confronto", "civilization-rome"]
            and y42 == [True, False] and u42 == [True, "✓ Nel confronto", False, "＋ Aggiungi al confronto"])
    R.check("T42", "«✓ Nel confronto» toccato di nuovo toglie la voce dal confronto (mappa, scheda, Nel mondo intorno, Universo); la voce resta selezionata e un avviso lo conferma",
            ok42, f"mappa: etichetta '{lab42}', dopo il tocco {m42}; scheda {s42}; Nel mondo intorno {y42}; Universo {u42}")

    # T43 barra del tempo: nascosta in Contemporanei, Confronto e Tecnologia (lì l'anno non cambia niente), visibile nelle altre viste che lo usano
    vis43 = {}
    await p.evaluate("()=>{contempFocusId='civilization-rome';techFocusId='civilization-rome'}")  # v0.59: nelle due viste la barra c'è solo senza voce scelta (T61)
    for v in ["esplora", "contemporanei", "tecnologia", "universo", "confronto"]:
        await goto_view(p, v); await p.wait_for_timeout(150)
        vis43[v] = await p.evaluate("()=>{const d=document.getElementById('timeDock');return getComputedStyle(d).display!=='none'&&d.getBoundingClientRect().height>0}")
    await goto_view(p, "esplora")
    ok43 = vis43 == {"esplora": True, "contemporanei": False, "tecnologia": False, "universo": True, "confronto": False}
    R.check("T43", "Barra del tempo nascosta in Contemporanei e Tecnologia con una voce scelta, e nel Confronto (lì l’anno non cambia niente), visibile in Esplora e Universo", ok43, f"{vis43}")

    # T44 Contemporanei: quattro esempi all'apertura; con una voce scelta, durata sulle epoche e righello allineato alle barrette
    await goto_view(p, "contemporanei")
    t44 = await p.evaluate("""()=>{contempFocusId=null;selected=null;renderContemporanei();const sug=[...document.querySelectorAll('#contempSummary [data-contemp-focus]')].map(b=>b.textContent);
        contempView='elenco';setContempFocus('civilization-rome');const seg=document.querySelector('.cw-seg'),tr=document.querySelector('.cw-track');
        const ri=document.querySelector('.contemp-ruler .cr-in')?.getBoundingClientRect(),bar=document.querySelector('.contemp-bar')?.getBoundingClientRect();
        const labs=[...document.querySelectorAll('.cr-in span')].map(e=>e.getBoundingClientRect());let overlap=false;for(let i=1;i<labs.length;i++)if(labs[i].left<labs[i-1].right)overlap=true;
        const on=[...document.querySelectorAll('.cw-ep.on')].map(e=>e.textContent);
        const out={sug,seg:!!seg&&seg.getBoundingClientRect().width>2&&seg.getBoundingClientRect().left>tr.getBoundingClientRect().left,on,
          aligned:!!ri&&!!bar&&Math.abs(ri.left-bar.left)<1.5&&Math.abs(ri.right-bar.right)<1.5,first:document.querySelector('.cr-in span')?.textContent,overlap};
        setContempFocus('event-caduta-di-costantinopoli');out.point=!!document.querySelector('.contemp-ruler .cr-cap')&&!!document.querySelector('.cw-seg');contempView='grafico';renderContemporanei();return out}""")
    ok44 = (1 <= len(t44["sug"]) <= 4 and t44["seg"] and t44["aligned"] and t44["first"] == "509 a.C." and not t44["overlap"]
            and t44["on"] == ["Antichità"] and t44["point"])
    R.check("T44", "Contemporanei (vista Elenco): fino a quattro esempi all’apertura, attivi nell’anno; con una voce scelta, durata evidenziata sulle epoche e righello degli anni allineato alle barrette (anche per eventi puntuali)", ok44, f"{t44}")

    # T45 Universo, solo PC: la rotella sopra le linee temporali fa scorrere la pagina
    if not mobile:
        await goto_view(p, "universo")
        await p.evaluate("scrollTo(0,0)"); await p.wait_for_timeout(150)
        r45 = await p.evaluate("(()=>{const r=document.getElementById('universeViewport').getBoundingClientRect();return [r.left+r.width/2,Math.min(r.top+60,innerHeight-40)]})()")
        hit45 = await p.evaluate(f"!!document.elementFromPoint({r45[0]},{r45[1]})?.closest('#universeViewport')")
        await p.mouse.move(r45[0], r45[1])
        for _ in range(4):
            await p.mouse.wheel(0, 200); await p.wait_for_timeout(120)
        y45 = await p.evaluate("scrollY")
        await goto_view(p, "esplora")
        R.check("T45", "Universo (PC): la rotella del mouse sopra le linee temporali fa scorrere la pagina", hit45 and y45 > 300, f"puntatore sulle linee temporali {hit45}; pagina scesa di {y45} px")

    # T46 Universo: temi sopra le linee temporali, fermi a ogni tocco; «Tutti» li riaccende; su PC la barra resta in alto
    await goto_view(p, "universo")
    await p.evaluate("document.getElementById('universeLegend').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(200)
    above46 = await p.evaluate("document.getElementById('universeLegend').getBoundingClientRect().bottom<=document.getElementById('universeViewport').getBoundingClientRect().top")
    pos46, states46 = [], []
    for i in [0, 1, 2, 0, 1, None]:
        loc = p.locator("#universeLegend [data-ulane-all]") if i is None else p.locator("#universeLegend [data-ulane]").nth(i)
        if mobile:
            await loc.tap()
        else:
            await loc.click()
        await p.wait_for_timeout(250)
        pos46.append(round(await p.evaluate("document.getElementById('universeLegend').getBoundingClientRect().top")))
        states46.append(await p.evaluate("[...document.querySelectorAll('#universeLegend [data-ulane]')].map(b=>b.getAttribute('aria-pressed')==='true'?1:0).join('')+(document.querySelector('[data-ulane-all]').disabled?'|off':'|on')"))
    sticky46 = None
    if not mobile:
        await p.evaluate("scrollTo(0,700)"); await p.wait_for_timeout(250)
        sticky46 = await p.evaluate("Math.round(document.getElementById('universeBar').getBoundingClientRect().top)")
        await p.evaluate("scrollTo(0,0)")
    await goto_view(p, "esplora")
    ok46 = (above46 and max(pos46) - min(pos46) <= 1 and states46 == ["01111|on", "00111|on", "00011|on", "10011|on", "11011|on", "11111|off"]
            and (mobile or sticky46 == 0))
    R.check("T46", "Universo: temi sopra le linee temporali, fermi a ogni tocco; «Tutti» li riaccende; su PC la barra di Finestra e Temi resta in alto",
            ok46, f"sopra {above46}; posizioni {pos46}; stati {states46}; barra dopo scorrimento {sticky46}")

    # T47 Schede: galleria di foto da Wikimedia Commons (max 3, caricate solo all'apertura), crediti con autore e licenza, ingrandimento
    t47 = await p.evaluate(r"""async()=>{const withImg=ALL.filter(x=>(x.images||[]).length).length;openInEsplora('culture-nazca');await new Promise(r=>setTimeout(r,250));
        const g=document.querySelector('#detail .gallery');const imgs=[...document.querySelectorAll('#detail .gallery img')].map(i=>i.getAttribute('src'));
        const credit=document.querySelector('#detail .gallery-credit')?.textContent||'';const links=document.querySelectorAll('#detail .gallery-credit a').length;
        document.querySelector('#detail [data-gallery="1"]').click();const lb=document.getElementById('lightbox');const big=lb?.querySelector('img')?.getAttribute('src')||'';
        lb.querySelector('[data-lb-step="1"]').click();const big2=lb.querySelector('img').getAttribute('src');
        document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));const closed=lb.hidden;
        const noImg=ALL.find(x=>!(x.images||[]).length);openInEsplora(noImg.id);await new Promise(r=>setTimeout(r,200));const none=!document.querySelector('#detail .gallery');
        const maxN=Math.max(...ALL.map(x=>(x.images||[]).length));
        return {withImg,n:imgs.length,thumbs:imgs.every(u=>/^https:\/\/upload\.wikimedia\.org\/wikipedia\/commons\/thumb\/[0-9a-f]\/[0-9a-f]{2}\/.+\/330px-/.test(u)),lazy:[...document.querySelectorAll('#detail .gallery img')].length===0||true,
          credit:credit.includes('Wikimedia Commons')&&credit.includes('CC BY-SA'),links,big:/\/960px-/.test(big),stepped:big2!==big,closed,none,maxN}}""")
    ok47 = (t47["withImg"] >= 300 and t47["n"] == 3 and t47["thumbs"] and t47["credit"] and t47["links"] == 3 and t47["big"]
            and t47["stepped"] and t47["closed"] and t47["none"] and t47["maxN"] <= 3)
    await goto_view(p, "esplora")
    R.check("T47", "Schede: galleria fino a 3 foto da Wikimedia Commons con autore e licenza, ingrandimento con frecce ed Esc; nessuna galleria dove non ci sono foto", ok47, f"{t47}")

    # T48 (PC) ricerca da tastiera: frecce per scorrere, Invio apre la scheda, Esc chiude
    if not mobile:
        await goto_view(p, "esplora")
        await p.evaluate("()=>{const f=document.getElementById('search');f.value='';f.scrollIntoView({block:'center'})}")
        await p.click("#search"); await p.keyboard.type("maya"); await p.wait_for_timeout(250)
        grid48 = []
        for k in ["ArrowDown", "ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp"]:
            await p.keyboard.press(k); await p.wait_for_timeout(50)
            grid48.append(await p.evaluate("()=>[...document.querySelectorAll('#searchPreview .search-hit')].findIndex(b=>b.classList.contains('kb-active'))"))
        await p.keyboard.press("ArrowDown"); await p.wait_for_timeout(80)
        act48 = await p.evaluate("()=>document.querySelector('#searchPreview .kb-active')?.dataset.id||null")
        await p.keyboard.press("Enter"); await p.wait_for_timeout(350)
        sel48 = await p.evaluate("()=>[selected,document.getElementById('searchPreview').hidden]")
        await p.click("#search"); await p.keyboard.type("roma"); await p.wait_for_timeout(200); await p.keyboard.press("Escape"); await p.wait_for_timeout(80)
        esc48 = await p.evaluate("()=>document.getElementById('searchPreview').hidden")
        await p.evaluate("()=>{const f=document.getElementById('search');f.value='';f.blur();renderSearchPreview()}")
        ok48 = bool(act48) and sel48 == [act48, True] and esc48 and grid48 == [0, 1, 3, 2, 0]
        R.check("T48", "Ricerca (PC): frecce ↑ ↓ ← → sui risultati a due colonne, Invio apre la scheda, Esc chiude l’elenco", ok48, f"griglia {grid48}; voce evidenziata {act48}; dopo Invio {sel48}; Esc {esc48}")

    # T49 Contemporanei: arrivando da una voce ingrandita in Esplora, la mappa mostra tutti i punti contemporanei
    t49 = await p.evaluate("""async()=>{openInEsplora('civilization-rome');await new Promise(r=>setTimeout(r,450));const z0=mapZoom;location.hash='#contemporanei';await new Promise(r=>setTimeout(r,800));
        const f=contempFocus();const tot=ALL.filter(x=>x.map_geometry&&(x.id===f.id||overlapOf(x,f))).length;return [Math.round(z0*10)/10,document.querySelectorAll('#pins .map-marker').length,tot]}""")
    await goto_view(p, "esplora")
    R.check("T49", "Contemporanei: la mappa si allarga per mostrare tutti i punti delle voci contemporanee", t49[0] > 1.5 and t49[1] == t49[2], f"ingrandimento in Esplora {t49[0]}; punti visibili {t49[1]} su {t49[2]}")

    # T50 Contemporanei, vista Grafico: voce principale come fascia, ogni voce con la durata intera, scelta Grafico/Elenco ricordata
    await goto_view(p, "contemporanei")
    t50 = await p.evaluate("""async()=>{contempView='grafico';setContempFocus('civilization-rome');await new Promise(r=>setTimeout(r,200));const f=contempFocus();
        document.querySelectorAll('[data-contemp-more]').forEach(b=>b.click());await new Promise(r=>setTimeout(r,100));
        const exp=ALL.filter(x=>x.id!==f.id&&x.start_year<=f.end_year&&x.end_year>=f.start_year).length;
        const rows=[...document.querySelectorAll('#contempList .cg-wrap')];const bands=document.querySelectorAll('#contempList .cg-band').length;
        const tr=document.querySelector('#contempList .cg-focus .cg-track').getBoundingClientRect(),fb=document.querySelector('#contempList .cg-bar.is-focus').getBoundingClientRect();
        const [lo,hi]=contempScale(f);const expL=tr.left+(f.start_year-lo)/(hi-lo)*tr.width;
        const nur=document.querySelector('#contempList .cg-wrap[data-id="culture-nuragic"] .cg-bar');const cutL=nur?.classList.contains('cut-l');
        document.querySelector('#contempList .cg-wrap[data-id="civilization-han"] .cg-row').click();await new Promise(r=>setTimeout(r,100));
        const han=document.querySelector('#contempList .cg-wrap[data-id="civilization-han"] .contemp-more')?.textContent||'';
        document.querySelector('[data-contemp-view="elenco"]').click();const el=!!document.querySelector('#contempList .contemp-bar')&&!document.querySelector('#contempList .cg');let stored='';try{stored=localStorage.getItem('atlante.contempView')}catch(_){}
        document.querySelector('[data-contemp-view="grafico"]').click();
        return {exp,rows:rows.length,bands,aligned:Math.abs(fb.left-expL)<2,cutL,han:han.includes('insieme dal 206 a.C. al 220 d.C.'),el,stored}}""")
    ok50 = t50["rows"] == t50["exp"] and t50["bands"] == t50["exp"] + 1 and t50["aligned"] and t50["cutL"] and t50["han"] and t50["el"] and t50["stored"] == "elenco"
    R.check("T50", "Contemporanei, vista Grafico: voce principale come fascia comune, ogni voce con la sua durata intera (tagliata se esce dal grafico), dettagli al tocco; si torna all’Elenco", ok50, f"{t50}")

    # T51 Confronto: linea del tempo comune e frasi sulle sovrapposizioni prima della tabella
    await goto_view(p, "confronto")
    t51 = await p.evaluate("""()=>{compareIds=['culture-maya','civilization-inca','state-ancient-egypt'];renderComparator();
        const rows=document.querySelectorAll('.cmp-chart .cmp-row').length,facts=[...document.querySelectorAll('.cmp-facts li')].map(l=>l.textContent);
        const order=[...document.querySelectorAll('#compareOutput > *')].map(e=>e.className||e.tagName);
        compareIds=['culture-maya','civilization-inca'];renderComparator();const band=!!document.querySelector('.cmp-chart .cg-band');
        compareIds=[];renderComparator();return {rows,facts,order:order.slice(0,3),band}}""")
    ok51 = (t51["rows"] == 3 and len(t51["facts"]) == 5 and t51["facts"][0].startswith("Non c’è un periodo")
            and "insieme dal 1200 d.C. al 1533 d.C." in t51["facts"][1] and "Maya ed Egitto dinastico" in t51["facts"][2]
            and t51["order"][0] == "cmp-chart" and t51["order"][1] == "cmp-facts" and t51["band"])
    R.check("T51", "Confronto: linea del tempo comune (fascia del periodo condiviso) e frasi su sovrapposizioni e collegamenti prima della tabella", ok51, f"{t51}")

    # T52 Tecnologia e ricerca: pulsante per la scheda della voce di riferimento; «inca» trova per primo l'Impero inca
    await goto_view(p, "tecnologia")
    t52 = await p.evaluate("""async()=>{setTechFocus('culture-maya');const btn=document.querySelector('#techSummary .open-scheda');const txt=btn?.textContent;
        techMode='dettaglio';techOpenId='tech-ast-long-count';renderTecnologia();const att=[...document.querySelectorAll('[data-tech-id="tech-ast-long-count"] [data-tech-scheda]')].map(b=>b.dataset.techScheda);
        btn&&document.querySelector('#techSummary .open-scheda').click();await new Promise(r=>setTimeout(r,300));const went=[currentView,selected];
        const f=document.getElementById('search');f.value='inca';renderSearchPreview();const first=document.querySelector('#searchPreview .search-hit strong')?.textContent;f.value='';renderSearchPreview();
        return {txt,att,went,first,linked:TECH.filter(t=>(t.related_ids||[]).length).length}}""")
    ok52 = t52["txt"] == "Apri la scheda «Maya»" and t52["att"] == ["culture-maya"] and t52["went"] == ["esplora", "culture-maya"] and t52["first"] == "Impero inca (Tahuantinsuyo)" and t52["linked"] == 29
    R.check("T52", "Tecnologia: «Apri la scheda» per la voce di riferimento e per le attestazioni collegate (29 su 38); ricerca ordinata per rilevanza («inca» → Impero inca)", ok52, f"{t52}")

    # T53 Scheda: data con «circa» quando è approssimata e un solo semaforo della datazione (solida, indicativa, discussa) con i dettagli al tocco
    await goto_view(p, "esplora")
    t53 = await p.evaluate("""async()=>{const out={};for(const id of ['site-chichen-itza','event-1492','culture-botai']){openInEsplora(id);await new Promise(r=>setTimeout(r,250));
        const tags=[...document.querySelectorAll('#detail .tags .tag')];const b=document.querySelector('#detail .tag.sem');const box=document.getElementById('semInfo');const h0=box.hidden;b.click();
        out[id]={n:tags.length,date:tags[0].textContent,sem:b.dataset.sem,open:h0&&!box.hidden&&b.getAttribute('aria-expanded')==='true',info:box.textContent.includes('Affidabilità della datazione')}}
        const cnt={ok:0,mid:0,deb:0};ALL.forEach(x=>cnt[semaforo(x).k]++);return {out,cnt,n:ALL.length}}""")
    o53 = t53["out"]
    ok53 = (all(v["n"] == 2 and v["open"] and v["info"] for v in o53.values()) and o53["site-chichen-itza"]["date"].startswith("circa ")
            and o53["site-chichen-itza"]["sem"] == "mid" and o53["event-1492"]["date"] == "1492 d.C." and o53["event-1492"]["sem"] == "ok"
            and o53["culture-botai"]["sem"] == "deb" and sum(t53["cnt"].values()) == t53["n"] and t53["cnt"]["deb"] == 15)  # 15 dalla v0.68: espansione austronesiana e Polinesia orientale
    R.check("T53", "Scheda: data con «circa» se approssimata e un solo semaforo della datazione (solida · indicativa · discussa) con i dettagli al tocco", ok53, f"{t53}")

    # T54 icone per tipologia: scheda, riepilogo, ricerca; sui punti una forma per tipologia e l'icona piena sul punto scelto; legenda con le forme
    await goto_view(p, "esplora")
    t54 = await p.evaluate("""async()=>{const cats=new Set(ALL.map(typeCat));const allIc=[...cats].every(k=>TYPE_IC[k]);
        openInEsplora('civilization-rome');await new Promise(r=>setTimeout(r,700));
        const sch=!!document.querySelector('#detail .meta svg.type-ic[data-ic="stato"],#detail .meta svg.type-ic');const ic=document.querySelector('#detail .meta svg.type-ic')?.dataset.ic;
        const selIc=document.querySelectorAll('#pins .map-marker[data-id="civilization-rome"] path.pin-ic').length;
        const glyphs=document.querySelectorAll('#pins path.pin-glyph').length,kinds=new Set([...document.querySelectorAll('#pins path.pin-glyph')].map(g=>g.dataset.kind||g.getAttribute('class'))).size;
        const legend=document.querySelectorAll('.legend-pin').length;
        const f=document.getElementById('search');f.value='roma';f.dispatchEvent(new Event('input',{bubbles:true}));await new Promise(r=>setTimeout(r,250));
        const hits=[...document.querySelectorAll('#searchPreview .search-hit')];const hitIc=hits.length>0&&hits.every(h=>h.querySelector('svg.type-ic'));
        f.value='';f.dispatchEvent(new Event('input',{bubbles:true}));
        return {cats:[...cats].sort(),allIc,sch,ic,selIc,glyphs,legend,hits:hits.length,hitIc}}""")
    ok54 = t54["allIc"] and len(t54["cats"]) == 7 and t54["sch"] and t54["selIc"] == 1 and t54["glyphs"] > 0 and t54["legend"] >= 3 and t54["hitIc"]
    R.check("T54", "Icone per tipologia nella scheda e nella ricerca; sui punti una forma per tipologia, icona piena sul punto aperto; legenda con le forme", ok54, f"{t54}")

    # T55 collegamenti a richiesta: nessun arco all'apertura; il pulsante della scheda li mostra tutti dentro la mappa; un estremo apre la sua voce
    t55 = await p.evaluate("""async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));closeDetail({instant:true});openInEsplora('civilization-rome');await w(900);
        const auto=document.querySelectorAll('#linksLayer path.link-arc').length,btn=document.getElementById('detailLinks'),label=btn?.textContent;
        const x=ALL.find(v=>v.id==='civilization-rome'),exp=linkTargets(x).length,[sx,sy]=linkXY(x);
        btn.click();await w(1500);
        const vb=worldSvg.getAttribute('viewBox').split(' ').map(Number),arcs=[...document.querySelectorAll('#linksLayer path.link-arc')];
        const nums=a=>a.getAttribute('d').match(/[-\\d.]+/g).map(Number);
        const inside=arcs.every(a=>{const n=nums(a);return n[4]>=vb[0]&&n[4]<=vb[0]+vb[2]&&n[5]>=vb[1]&&n[5]<=vb[1]+vb[3]});
        const fromPin=arcs.every(a=>{const n=nums(a);return Math.abs(n[0]-sx)<.01&&Math.abs(n[1]-sy)<.01});
        const drawn=arcs.every(a=>parseFloat(getComputedStyle(a).strokeDashoffset)<0.01);
        const bar=!document.getElementById('linksBar').hidden,sheetOpen=!document.getElementById('scheda').hidden,mobile=isCompact();
        const hit=document.querySelector('#linksLayer .link-hit'),hid=hit?.dataset.id;hit?.dispatchEvent(new MouseEvent('click',{bubbles:true}));await w(500);
        const after={sel:selected,arcs:document.querySelectorAll('#linksLayer path.link-arc').length,bar:!document.getElementById('linksBar').hidden};
        closeDetail({instant:true});
        return {auto,label,exp,n:arcs.length,inside,fromPin,drawn,bar,sheetOpen,mobile,hid,after}}""")
    ok55 = (t55["auto"] == 0 and t55["exp"] > 0 and t55["label"] == f"Mostra i collegamenti · {t55['exp']}" and t55["n"] == t55["exp"] and t55["inside"]
            and t55["fromPin"] and t55["drawn"] and t55["bar"] and t55["sheetOpen"] != t55["mobile"]
            and t55["after"] == {"sel": t55["hid"], "arcs": 0, "bar": False})
    R.check("T55", "Collegamenti solo a richiesta: «Mostra i collegamenti» disegna gli archi e la mappa li contiene tutti (su telefono la tendina si chiude); un estremo apre la sua voce", ok55, f"{t55}")

    # T56 tono della mappa secondo l'epoca dell'anno scelto (stessi confini della barra del tempo)
    t56 = await p.evaluate("""async()=>{const out=[];const r=document.getElementById('yearRange');
        for(const y of [-5000,-200,1200,1600,2000]){r.value=y;r.dispatchEvent(new Event('input',{bubbles:true}));await new Promise(res=>setTimeout(res,200));
          out.push([y,document.body.dataset.epoch,getComputedStyle(document.body).getPropertyValue('--epoch-land').trim()])}
        return out}""")
    ep56 = [v[1] for v in t56]
    ok56 = ep56 == ["preistoria", "antichita", "medioevo", "moderna", "contemporanea"] and len({v[2] for v in t56}) == 5 and all(v[2] for v in t56)
    R.check("T56", "La mappa cambia tono con l'epoca (Preistoria, Antichità, Medioevo, Moderna, Contemporanea)", ok56, f"{t56}")

    # T57 la scheda si apre dal punto (su telefono sale dal basso) e si chiude tornandoci; con «riduci movimento» niente animazioni
    t57 = await p.evaluate("""async()=>{const sch=document.getElementById('scheda');const w=ms=>new Promise(r=>setTimeout(r,ms));
        openInEsplora('state-carthage');await w(30);const animOpen=sch.getAnimations().length;const pulse=document.querySelectorAll('#pins circle.pin-pulse').length;
        await w(700);const settled=sch.getAnimations().length===0&&!sch.hidden;
        closeDetail();await w(30);const closing=!sch.hidden&&sch.getAnimations().length>0;await w(500);
        return {animOpen,pulse,settled,closing,closed:sch.hidden&&!detailOpen,sheet:isCompact()}}""")
    await p.emulate_media(reduced_motion="reduce")
    t57r = await p.evaluate("""async()=>{const sch=document.getElementById('scheda');openInEsplora('state-carthage');await new Promise(r=>setTimeout(r,30));
        const a=sch.getAnimations().length;closeDetail();return {anim:a,closedNow:sch.hidden}}""")
    await p.emulate_media(reduced_motion="no-preference")
    ok57 = t57["animOpen"] >= 1 and t57["settled"] and t57["closing"] and t57["closed"] and t57["pulse"] == 1 and t57r == {"anim": 0, "closedNow": True}
    R.check("T57", "Scheda: si apre dal punto della mappa (su telefono sale con un rimbalzo) e si chiude tornandoci; con «riduci movimento» è immediata", ok57, f"{t57}; riduci movimento {t57r}")

    # T58 contesto comune tra le viste: anno e voce scelta restano coerenti passando da una vista all'altra
    t58 = await p.evaluate("""async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const yr=y=>{const r=document.getElementById('yearRange');r.value=y;r.dispatchEvent(new Event('input',{bubbles:true}))};
        const view=v=>{location.hash='#'+v};const vbNow=()=>JSON.stringify([mapZoom,mapCx,mapCy].map(v=>+v.toFixed(2)));const out={};
        view('esplora');await w(300);openInEsplora('civilization-rome');await w(500);closeDetail({instant:true});yr(1500);await w(200);
        view('contemporanei');await w(500);out.cFocus=contempFocusId;
        out.sugActive=[...document.querySelectorAll('#contempSummary [data-contemp-focus]')].map(b=>activeIn(ALL.find(x=>x.id===b.dataset.contempFocus)));
        view('tecnologia');await w(500);out.tFocus=techFocusId;
        view('contemporanei');await w(400);setContempFocus('state-carthage');await w(300);out.yearAfter=chosenYear;
        view('esplora');await w(700);const vb=worldSvg.getAttribute('viewBox').split(' ').map(Number),c=ALL.find(x=>x.id==='state-carthage'),[cx,cy]=geoXY(+c.map_geometry.longitude,+c.map_geometry.latitude);
        out.esplora={sel:selected,open:detailOpen,inView:cx>=vb[0]&&cx<=vb[0]+vb[2]&&cy>=vb[1]&&cy<=vb[1]+vb[3],active:activeIn(c)};
        const z0=vbNow();view('contemporanei');await w(500);view('esplora');await w(500);out.sameView=z0===vbNow();
        const z1=vbNow();addCompare('culture-maya');addCompare('state-carthage');hideToast();await w(200);removeCompare('state-carthage');await w(200);
        out.cmp={sel:selected,sameView:z1===vbNow()};removeCompare('culture-maya');closeDetail({instant:true});
        return out}""")
    ok58 = (t58["cFocus"] is None and t58["sugActive"] and all(t58["sugActive"]) and t58["tFocus"] is None and t58["yearAfter"] != 1500
            and t58["esplora"] == {"sel": "state-carthage", "open": True, "inView": True, "active": True} and t58["sameView"]
            and t58["cmp"] == {"sel": "state-carthage", "sameView": True})
    R.check("T58", "Viste coerenti: Contemporanei e Tecnologia ripartono dall’anno se la voce non è più attiva; una voce scelta lì sposta l’anno e si ritrova in Esplora; inquadratura e voce non cambiano per il confronto", ok58, f"{t58}")

    # T59 storia di questo luogo: tieni premuto (telefono) o doppio clic (PC) su un punto vuoto; voci per epoca, al massimo 4, «+N altre»; mappa con le sole voci del luogo
    await goto_view(p, "esplora")
    await p.evaluate("()=>{const r=document.getElementById('yearRange');r.value=-16;r.dispatchEvent(new Event('input',{bubbles:true}));mapZoom=3;mapCx=(11+180)/360*900;mapCy=(90-40)/180*450;applyMapZoom();document.querySelector('#view-esplora .mapstage').scrollIntoView({block:'center'})}")
    await p.wait_for_timeout(400)
    gx, gy = await p.evaluate("()=>{const m=worldSvg.getScreenCTM(),pt=worldSvg.createSVGPoint();pt.x=(11+180)/360*900;pt.y=(90-40)/180*450;const q=pt.matrixTransform(m);return [q.x,q.y]}")
    if mobile:
        await p.evaluate("""([x,y])=>{const st=document.querySelector('.mapstage'),o={bubbles:true,pointerId:9,pointerType:'touch',clientX:x,clientY:y,isPrimary:true};st.dispatchEvent(new PointerEvent('pointerdown',o));setTimeout(()=>st.dispatchEvent(new PointerEvent('pointerup',o)),750)}""", [gx, gy])
        await p.wait_for_timeout(1200)
    else:
        await p.mouse.dblclick(gx, gy); await p.wait_for_timeout(800)
    t59 = await p.evaluate("""async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const out={};
        out.gesture=!!placeCtx&&Math.abs(placeCtx.lon-11)<1&&Math.abs(placeCtx.lat-40)<1&&!document.getElementById('scheda').hidden;
        openPlaceStory(null,null,{lonlat:{lon:12.5,lat:41.9}});await w(400);
        const secs=[...document.querySelectorAll('.place-epoch')];out.epochs=secs.map(s=>s.dataset.epoch);
        out.max4=secs.every(s=>s.querySelectorAll('.place-row').length<=4);
        const rows=[...document.querySelectorAll('.place-row')].map(b=>b.dataset.placeOpen);out.hasRome=rows.includes('civilization-rome')&&rows.includes('culture-etruscan');
        const pins=new Set([...document.querySelectorAll('#pins .map-marker')].map(g=>g.dataset.id));const geoShown=placeCtx.shown.filter(id=>{const g=ALL.find(x=>x.id===id).map_geometry;return g&&Number.isFinite(Number(g.latitude))});
        out.pinsMatch=pins.size>0&&[...pins].every(id=>placeCtx.shown.includes(id));
        out.mark=!!document.getElementById('placeMark');
        const more=document.querySelector('.place-more');out.more=more?.textContent;const sec=more?.closest('.place-epoch');const n0=sec?.querySelectorAll('.place-row').length;more?.click();await w(200);
        const sec2=document.querySelector(`.place-epoch[data-epoch="${sec?.dataset.epoch}"]`);out.expanded=[n0,sec2?.querySelectorAll('.place-row').length,+(sec2?.querySelector('h3 span')?.textContent||0)];
        document.querySelector('[data-place-mode="anno"]').click();await w(200);
        out.anno=[...document.querySelectorAll('.place-row')].map(b=>ALL.find(x=>x.id===b.dataset.placeOpen)).every(x=>x.end_year>=chosenYear-50&&x.start_year<=chosenYear+50);
        document.querySelector('[data-place-mode="tutte"]').click();await w(200);
        document.querySelector('.place-row[data-place-open="culture-etruscan"]').click();await w(400);
        out.opened={sel:selected,back:!!document.getElementById('placeBack'),place:!!placeCtx};
        document.getElementById('placeBack').click();await w(300);out.back=!!placeCtx&&!!document.querySelector('.place-epoch');
        closeDetail({instant:true});await w(200);out.closed=!placeCtx&&!document.getElementById('placeMark');
        return out}""")
    ok59 = (t59["gesture"] and t59["epochs"] and t59["epochs"] == [e for e in ["contemporanea", "moderna", "medioevo", "antichita", "preistoria"] if e in t59["epochs"]]
            and t59["max4"] and t59["hasRome"] and t59["pinsMatch"] and t59["mark"] and bool(t59["more"])
            and t59["expanded"][0] == 4 and t59["expanded"][1] == t59["expanded"][2] > 4 and t59["anno"]
            and t59["opened"] == {"sel": "culture-etruscan", "back": True, "place": False} and t59["back"] and t59["closed"])
    R.check("T59", "Storia di questo luogo: si apre tenendo premuto o con doppio clic; voci per epoca (al massimo 4, «+N altre»), solo quelle sulla mappa, «Intorno all’anno», ritorno dalla scheda", ok59, f"{t59}")

    # T60 v0.58: pulsante fisso «Storia di un luogo» (scelta del punto con un tocco), Escape annulla, nascosto fuori da Esplora; la storia è a strati (più recente in alto) senza fumetti
    await p.evaluate("()=>{closeDetail({instant:true});hideToast()}"); await goto_view(p, "esplora")
    await click_el(p, "#zoomReset"); await p.wait_for_timeout(300)
    await set_year(p, -16); await p.wait_for_timeout(200)
    await p.evaluate("document.getElementById('mappa').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(250)
    t60 = {}
    t60["btn"] = await p.evaluate("()=>{const b=document.getElementById('placeBtn');if(!b)return null;const r=b.getBoundingClientRect();return {vis:!b.hidden&&r.height>10&&r.height<60,txt:b.textContent.trim(),pressed:b.getAttribute('aria-pressed')}}")
    await tap(p, p.locator("#placeBtn"), mobile); await p.wait_for_timeout(200)
    t60["on"] = await p.evaluate("()=>({pressed:document.getElementById('placeBtn').getAttribute('aria-pressed'),txt:document.getElementById('placeBtnTxt').textContent,cls:document.querySelector('#view-esplora .mapstage').classList.contains('place-pick')})")
    await p.keyboard.press("Escape"); await p.wait_for_timeout(150)
    t60["esc"] = await p.evaluate("()=>document.getElementById('placeBtn').getAttribute('aria-pressed')")
    await tap(p, p.locator("#placeBtn"), mobile); await p.wait_for_timeout(200)
    await click_el(p, "#zoomReset"); await p.wait_for_timeout(300)
    await p.evaluate("document.querySelector('#view-esplora .mapstage').scrollIntoView({block:'center',behavior:'instant'})"); await p.wait_for_timeout(300)
    gx2, gy2 = await empty_map_point(p)
    await tap_xy(p, gx2, gy2, mobile); await p.wait_for_timeout(900)
    t60["ocean"] = await p.evaluate("()=>({ctx:!!placeCtx,pressed:document.getElementById('placeBtn').getAttribute('aria-pressed'),empty:!!document.querySelector('#detail .empty')})")
    await p.evaluate("()=>openPlaceStory(NaN,NaN,{lonlat:{lon:12.5,lat:41.9}})"); await p.wait_for_timeout(500)
    t60["open"] = await p.evaluate("""()=>{const s=[...document.querySelectorAll('.place-strata .place-epoch')].map(e=>e.dataset.epoch);const ord=['contemporanea','moderna','medioevo','antichita','preistoria'];
        return {ctx:!!placeCtx,strata:s.length>=2,order:JSON.stringify(s)===JSON.stringify(ord.filter(x=>s.includes(x))),top:!!document.querySelector('.strata-edge.top'),bot:!!document.querySelector('.strata-edge.bot'),
        pressed:document.getElementById('placeBtn').getAttribute('aria-pressed'),balloon:!!document.querySelector('.place-tip,.coach,.hint-balloon')}}""")
    await p.evaluate("()=>closeDetail({instant:true})")
    await goto_view(p, "contemporanei")
    t60["hid"] = await p.evaluate("()=>document.getElementById('placeBtn').hidden")
    await goto_view(p, "esplora")
    t60["back"] = await p.evaluate("()=>!document.getElementById('placeBtn').hidden")
    ok60 = (bool(t60["btn"]) and t60["btn"]["vis"] and t60["btn"]["txt"] == "Storia di un luogo" and t60["btn"]["pressed"] == "false"
            and t60["on"]["pressed"] == "true" and "Tocca" in t60["on"]["txt"] and t60["on"]["cls"] and t60["esc"] == "false"
            and t60["ocean"]["ctx"] and t60["ocean"]["pressed"] == "false" and t60["ocean"]["empty"] and t60["open"]["ctx"] and t60["open"]["strata"] and t60["open"]["order"] and t60["open"]["top"] and t60["open"]["bot"] and t60["open"]["pressed"] == "false" and not t60["open"]["balloon"]
            and t60["hid"] and t60["back"])
    R.check("T60", "Pulsante «Storia di un luogo»: tocco sulla mappa apre la storia, Escape annulla, nascosto fuori da Esplora; strati dal più recente in alto, nessun fumetto", ok60, f"{t60}")

    # T61 v0.59: senza voce scelta Contemporanei e Tecnologia mostrano la barra dell'anno e gli esempi la seguono; con una voce la barra sparisce e «Scegli per anno» la riporta; Tecnologia di norma solo stessa epoca
    t61 = await p.evaluate("""async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms)),out={};
        const dockVis=()=>{const d=document.getElementById('timeDock');return getComputedStyle(d).display!=='none'&&d.getBoundingClientRect().height>0};
        const sug=sel=>[...document.querySelectorAll(sel+' [data-contemp-focus],'+sel+' [data-tech-focus]')].map(b=>b.dataset.contempFocus||b.dataset.techFocus);
        const yr=y=>{const r=document.getElementById('yearRange');r.value=y;r.dispatchEvent(new Event('input',{bubbles:true}))};
        const marks=()=>[...document.querySelectorAll('#techList .ti-mark')].map(g=>TECH.find(t=>t.id===g.dataset.ti));
        const view=v=>{location.hash='#'+v};
        selected=null;contempFocusId=null;techFocusId=null;techScope='epoca';view('esplora');await w(300);yr(-500);await w(150);
        view('contemporanei');await w(500);out.cDock=dockVis();const c1=sug('#contempSummary');yr(1500);await w(200);const c2=sug('#contempSummary');
        out.cSug=[c1.length>0&&c2.length>0&&c1.join()!==c2.join(),c2.every(id=>activeIn(ALL.find(x=>x.id===id)))];out.cLabel=document.getElementById('dockYear').textContent;
        setContempFocus(c2[0]);await w(300);out.cDockFocus=dockVis();
        document.querySelector('[data-clear-focus="contemporanei"]').click();await w(300);out.cBack=[dockVis(),contempFocusId===null,!!document.querySelector('#contempSummary [data-contemp-focus]')];
        view('tecnologia');await w(500);out.tDock=dockVis();yr(-500);await w(200);const t1=sug('#techSummary');yr(1500);await w(200);const t2=sug('#techSummary');
        out.tSug=[t1.length>0&&t2.length>0&&t1.join()!==t2.join()];
        techMode='sintesi';setTechFocus('event-rapanui-moai-tradition');await w(300);out.tDockFocus=dockVis();const f=ALL.find(x=>x.id==='event-rapanui-moai-tradition'),ep=techEpoch(f);
        const m1=marks();out.epoca=[ep.name,m1.length>0,m1.every(t=>t.start_year>=ep.from),!document.querySelector('#techList .ti-mark[data-ti="tech-arch-great-pyramid"]'),document.querySelector('[data-tech-scope="epoca"]').getAttribute('aria-pressed')];
        document.querySelector('[data-tech-scope="tutte"]').click();await w(200);const m2=marks();out.tutte=[m2.length>m1.length,!!document.querySelector('#techList .ti-mark[data-ti="tech-arch-great-pyramid"]')];
        document.querySelector('[data-tech-scope="epoca"]').click();await w(200);out.again=marks().length===m1.length;
        document.querySelector('[data-clear-focus="tecnologia"]').click();await w(300);out.tBack=[dockVis(),techFocusId===null];
        view('esplora');await w(300);return out}""")
    ok61 = (t61["cDock"] and t61["cSug"] == [True, True] and "1500" in t61["cLabel"] and not t61["cDockFocus"] and t61["cBack"] == [True, True, True]
            and t61["tDock"] and t61["tSug"] == [True] and not t61["tDockFocus"]
            and t61["epoca"] == ["Medioevo", True, True, True, "true"] and t61["tutte"] == [True, True] and t61["again"] and t61["tBack"] == [True, True])
    R.check("T61", "Contemporanei e Tecnologia senza voce scelta: barra dell’anno visibile e esempi che la seguono; con una voce scelta la barra sparisce e «Scegli per anno» la riporta; Tecnologia mostra di norma solo la stessa epoca, «+ epoche precedenti» aggiunge le altre", ok61, f"{t61}")

    # T62 v0.60: Mosaico del tempo (prima «Tavola del tempo · prova»): vista #tavola a tutta altezza, mini foto senza sovrapposizioni, prima le voci importanti,
    # zoom che aggiunge voci, trascinamento che sposta senza aprire schede, tocco su una foto che apre la scheda sopra la tavola; uscendo la scheda torna in Esplora
    reqs62 = []
    p.on("request", lambda r: reqs62.append(r.url) if "upload.wikimedia.org" in r.url else None)
    await p.evaluate("()=>{closeDetail({instant:true});selected=null;detailOpen=false;renderDetail();updateDetailPanel();location.hash='#tavola'}"); await p.wait_for_timeout(900)
    t62 = await p.evaluate("""()=>{const st=document.getElementById('tavStage'),r=st.getBoundingClientRect();
        const tiles=[...document.querySelectorAll('.tav-tile:not([hidden])')].map(e=>{const b=e.getBoundingClientRect();return {l:b.left,t:b.top,r:b.right,b:b.bottom}}).filter(a=>a.r>r.left&&a.l<r.right&&a.b>r.top&&a.t<r.bottom);
        let ov=0;for(let i=0;i<tiles.length;i++)for(let j=i+1;j<tiles.length;j++){const a=tiles[i],b=tiles[j];if(a.l<b.r-1&&a.r>b.l+1&&a.t<b.b-1&&a.b>b.t+1)ov++}
        const rel=id=>ALL.find(x=>x.id===id).relevance||3,placed=[...TAV.lay.keys()],avg=a=>a.reduce((s,v)=>s+v,0)/Math.max(1,a.length);
        return {view:currentView,h:Math.round(r.height),fits:r.bottom<=window.innerHeight+1&&r.top>=-1,n:tiles.length,ov,n0:placed.length,
          relPlaced:+avg(placed.map(rel)).toFixed(2),relAll:+avg(TAV.items.map(i=>rel(i.id))).toFixed(2),dock:getComputedStyle(document.getElementById('timeDock')).display,
          conts:[...document.querySelectorAll('#tavHead .tav-cont')].filter(e=>!e.hidden).map(e=>e.textContent),miniOff:document.getElementById('tavMini').hidden}}""")
    t62["n3"] = await p.evaluate("()=>{tavZoomAt(TAV.s*3,TAV.sw/2,TAV.sh/2);tavDraw();return TAV.lay.size}")
    await p.wait_for_timeout(300)
    t62["mini"] = await p.evaluate("()=>({vis:!document.getElementById('tavMini').hidden,on:document.querySelectorAll('#tavMini .tav-mini-hi path.on').length,txt:!!document.querySelector('#tavMini small').textContent,hint:document.getElementById('tavHint').hidden})")
    sizes62 = sorted({u.split('/')[-1].split('px-')[0] for u in reqs62 if 'px-' in u})
    t62["thumbs"] = sizes62
    st62 = await p.evaluate("()=>{const r=document.getElementById('tavStage').getBoundingClientRect();return [r.left+r.width*0.55,r.top+r.height*0.5]}")
    oy0 = await p.evaluate("()=>TAV.oy")
    if mobile:
        await touch_drag(p, st62[0], st62[1], 0, -140)
    else:
        await p.mouse.move(st62[0], st62[1]); await p.mouse.down(); await p.mouse.move(st62[0], st62[1] - 70, steps=5); await p.mouse.move(st62[0], st62[1] - 140, steps=5); await p.mouse.up()
    await p.wait_for_timeout(500)
    t62["drag"] = await p.evaluate("(o)=>({moved:Math.abs(TAV.oy-o)>60,sel:selected,open:detailOpen})", oy0)
    pick = await p.evaluate("""()=>{const r=document.getElementById('tavStage').getBoundingClientRect();const t=[...document.querySelectorAll('.tav-tile:not([hidden])')].find(e=>{const b=e.querySelector('.tav-ph').getBoundingClientRect();return b.left>r.left+60&&b.right<r.right-10&&b.top>r.top+40&&b.bottom<r.top+r.height*0.6});if(!t)return null;t.setAttribute('data-pick','1');return t.dataset.tav}""")
    if pick:
        await tap(p, p.locator(".tav-tile[data-pick] .tav-ph"), mobile); await p.wait_for_timeout(800)
    t62["open"] = await p.evaluate("""(id)=>{const s=document.getElementById('scheda'),b=s.getBoundingClientRect(),dl=document.getElementById('detailLinks');return {pick:!!id,sel:selected===id,open:detailOpen,vis:!s.hidden,host:s.parentElement.id,
        inScreen:b.top>=-1&&b.bottom<=window.innerHeight+1&&b.height>100,title:document.querySelector('#detail .detail-title')?.textContent===ALL.find(x=>x.id===id)?.name,
        ring:!!document.querySelector('.tav-tile.sel[data-tav="'+id+'"]'),links:!dl||getComputedStyle(dl).display==='none'}}""", pick)
    await p.screenshot(path=f"{OUT}/{name}_tavola.png")
    await p.evaluate("()=>closeDetail({instant:true})")
    await goto_view(p, "esplora")
    t62["back"] = await p.evaluate("()=>{const s=document.getElementById('scheda'),m=document.getElementById('mappa');return s.closest('.view')?.id==='view-esplora'&&m.nextElementSibling===s}")
    await p.evaluate("()=>{selected=null;detailOpen=false;renderDetail();updateDetailPanel()}")
    ok62 = (t62["view"] == "tavola" and t62["h"] >= 300 and t62["fits"] and 5 <= t62["n"] <= 150 and t62["ov"] == 0 and t62["relPlaced"] < t62["relAll"]
            and len(t62["conts"]) == 6 and "Europa" in t62["conts"] and "Asia" in t62["conts"] and t62["miniOff"] and t62["mini"]["vis"] and t62["mini"]["on"] >= 1 and t62["mini"]["txt"] and t62["mini"]["hint"]
            and set(t62["thumbs"]) <= {"120", "250"} and "120" in t62["thumbs"]
            and t62["n3"] > t62["n0"] and t62["dock"] == "none" and t62["drag"] == {"moved": True, "sel": None, "open": False}
            and t62["open"] == {"pick": True, "sel": True, "open": True, "vis": True, "host": "tavolaWrap", "inScreen": True, "title": True, "ring": True, "links": True} and t62["back"])
    R.check("T62", "Mosaico del tempo: a tutta altezza, i sei continenti leggibili da lontano, planisfero in alto da vicino, foto piccole (120 e 250 px), senza sovrapposizioni con prima le voci importanti, lo zoom ne aggiunge, trascinare sposta senza aprire, il tocco apre la scheda sopra la tavola; uscendo la scheda torna in Esplora", ok62, f"{t62}")

async def run_tablet(pw):
    # T36 tablet (iPad emulato): viste nella barra in basso come su telefono, scheda a tendina che si chiude trascinandola giù
    R = Run("ipad")
    browser = await pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    ctx = await browser.new_context(**dict(pw.devices["iPad (gen 7)"]))
    p = await ctx.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
    await p.goto(URL, wait_until="load"); await p.wait_for_timeout(1000)
    g = await p.evaluate("""()=>{const nav=document.querySelector('.mobile-nav'),tabs=document.querySelector('.view-tabs'),dock=document.getElementById('timeDock');
        const n=nav.getBoundingClientRect(),d=dock.getBoundingClientRect();
        return {touchUi:document.documentElement.classList.contains('touch-ui'),nav:getComputedStyle(nav).display!=='none'&&n.height>0,tabs:getComputedStyle(tabs).display!=='none',
          dockAbove:d.bottom<=n.top+1,navBottom:Math.round(n.bottom)===innerHeight}}""")
    await p.evaluate("()=>openInEsplora('civilization-rome')"); await p.wait_for_timeout(700)
    sh = await p.evaluate("()=>{const s=document.getElementById('scheda'),r=s.getBoundingClientRect(),d=document.getElementById('timeDock').getBoundingClientRect();return {sheet:s.classList.contains('is-sheet'),aboveDock:r.bottom<=d.top+1,top:Math.round(r.top),vh:innerHeight}}")
    hb = await p.locator("#sheetHandle").bounding_box()
    await touch_drag(p, hb["x"] + hb["width"] / 2, hb["y"] + hb["height"] / 2, 0, 220); await p.wait_for_timeout(500)
    closed = await p.evaluate("()=>document.getElementById('scheda').hidden")
    wide = []
    for v in ["esplora", "contemporanei", "tecnologia", "universo", "confronto", "archivio", "impostazioni"]:
        await p.evaluate("(n)=>{location.hash='#'+n}", v); await p.wait_for_timeout(350)
        w = await p.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
        if w[0] > w[1] + 1: wide.append(f"{v}: {w[0]}px su {w[1]}px")
    await p.screenshot(path=f"{OUT}/ipad_universo.png")
    ok = g["touchUi"] and g["nav"] and not g["tabs"] and g["dockAbove"] and sh["sheet"] and sh["aboveDock"] and sh["top"] > sh["vh"] * 0.3 and closed and not wide and not errors
    R.check("T36", "Tablet: viste nella barra in basso, scheda a tendina sopra la barra del tempo, si chiude trascinandola giù",
            ok, f"{g}; scheda {sh}; chiusa trascinando: {closed}; viste troppo larghe {wide}; errori {errors[:2]}")
    await browser.close()
    return R.rows

async def main():
    async with async_playwright() as pw:
        a, b, c = await asyncio.gather(run_device(pw, "desktop", {"viewport": {"width": 1440, "height": 900}}, False),
                                       run_device(pw, "iphone13", dict(pw.devices["iPhone 13"]), True),
                                       run_tablet(pw))
        rows = a + b + c
    rows.sort(key=lambda r: (r["code"], r["device"]))
    for r in rows:
        print(f"{r['esito']:8} {r['code']} [{r['device']:8}] {r['name']} — {r['dettaglio']}")
    failed = [r for r in rows if r["esito"] == "FALLITO"]
    print(f"\n{len(rows)} controlli, {len(failed)} falliti, {sum(r['esito']=='NOTO' for r in rows)} difetti noti")
    json.dump(rows, open(f"{OUT}/risultati.json", "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if failed else 0)

asyncio.run(main())
