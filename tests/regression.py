"""Test di regressione dell'Atlante storico.

Uso:  python3 tests/regression.py <file.html> <cartella_screenshot>

Verifica, su desktop e su iPhone 13 emulato, i comportamenti che non devono
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
    p.on("request", lambda r: external.add(r.url) if not r.url.startswith(("file:", "data:", "blob:", "http://127.0.0.1")) else None)
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
    await p.evaluate("()=>{const r=document.getElementById('dockRange');r.value=-500;r.dispatchEvent(new Event('input',{bubbles:true}));r.dispatchEvent(new Event('change',{bubbles:true}))}")
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
    await p.wait_for_timeout(300)
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
    await click_el(p, "#zoomReset")
    await p.wait_for_timeout(300)
    if not await p.is_visible("#mapPointPopup"):
        await tap(p, p.locator("#pins .map-marker").first, mobile)
        await p.wait_for_timeout(300)

    # T06 contrasto pulsanti del popup, per ogni palette
    low = []
    for pal in ["deep", "atlantic", "noir", "sand", "graphite"]:
        await p.evaluate("(n)=>{const b=document.querySelector(`.palette-choice[data-palette='${n}']`);if(b)b.click()}", pal)
        await p.wait_for_timeout(120)
        if not await p.is_visible("#mapPointPopup"):
            await tap(p, p.locator("#pins .map-marker").first, mobile); await p.wait_for_timeout(300)
        for b in await p.query_selector_all("#mapPointPopup .popup-actions button"):
            c = await b.evaluate(JS_CONTRAST)
            if c["ratio"] < 4.5:
                low.append(f"{pal}: '{c['text']}' {c['ratio']:.1f}:1")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='deep']`)?.click()")
    R.check("T06", "Pulsanti del popup leggibili (contrasto >= 4.5:1) in tutte le palette", not low, "; ".join(low) or "tutti >= 4.5:1")
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
    await p.evaluate("()=>closeDetail()")

    # T08 confronto: massimo 5, anno invariato (vista Contemporanei)
    await goto_view(p, "universo")
    await open_details(p, "#moreConfronto")
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
            u0["nodes"] > 20 and u0["w"] > 200 and abs(u1["center"] - u0["center"]) > 1 and u1["year"] == u0["year"],
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
    await p.evaluate("()=>{selectItem('civilization-rome',{preserveYear:true});addCompare('culture-maya');addCompare('event-dinastia-han')}")
    state0 = await p.evaluate("()=>[document.getElementById('yearLabel').textContent,selected,compareIds.length]")
    bad = []
    for v in ["contemporanei", "universo", "archivio", "impostazioni", "esplora"]:
        if mobile:
            await tap(p, p.locator(f".mobile-nav a[data-view-link='{v}']"), mobile)
        else:
            await p.click(f".view-tabs a[data-view-link='{v}']")
        await p.wait_for_timeout(400)
        info = await p.evaluate("""()=>({vis:[...document.querySelectorAll('.view')].filter(v=>!v.hidden).map(v=>v.dataset.view),
            hash:location.hash,active:[...document.querySelectorAll('[data-view-link].active')].map(a=>a.dataset.viewLink)})""")
        if info["vis"] != [v] or info["hash"] != "#" + v or set(info["active"]) != {v}:
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
        document.querySelectorAll('[data-contemp-more]').forEach(b=>b.click());
        const shown=[...document.querySelectorAll('#contempList .contemp-row')].map(r=>r.dataset.id).sort();
        const pins=[...document.querySelectorAll('#pins .map-marker')].map(g=>g.dataset.id);
        const badPins=pins.filter(id=>{const x=ALL.find(a=>a.id===id);return !(x.id===f.id||(x.start_year<=f.end_year&&x.end_year>=f.start_year))});
        const row=id=>document.querySelector(`#contempList .contemp-row[data-id='${id}'] .contemp-overlap`)?.textContent||'';
        return {title:document.getElementById('contempTitle').textContent,exp:exp.length,shown:shown.length,same:JSON.stringify(exp)===JSON.stringify(shown),
          pins:pins.length,badPins,han:row('event-dinastia-han'),nur:row('culture-nuragic')}}""")
    ok15 = (c15["same"] and c15["title"] == "Durante «Roma: Repubblica e Impero»" and c15["pins"] > 0 and not c15["badPins"]
            and c15["han"].startswith("insieme dal 206 a.C. al 220 d.C.") and c15["nur"] == "insieme dal 509 a.C. al 500 a.C. · ≈ 9 anni")
    R.check("T15", "Contemporanei: elenco e punti mostrano solo le voci sovrapposte alla durata scelta, con anni corretti",
            ok15, f"attese {c15['exp']}, mostrate {c15['shown']}, punti {c15['pins']} (fuori periodo {c15['badPins']}); Han: '{c15['han']}'; Nuragici: '{c15['nur']}'")
    await p.screenshot(path=f"{OUT}/{name}_contemporanei.png", full_page=True)

    # T19 dal popup in Contemporanei, "Apri scheda" porta alla scheda nella vista Esplora
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    await tap(p, p.locator("#pins .map-marker[data-id='event-dinastia-han']"), mobile)
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

    # T10 palette conservata dopo ricarica
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='noir']`)?.click()")
    await p.reload(wait_until="load"); await p.wait_for_timeout(800)
    pal = await p.evaluate("()=>document.body.dataset.palette")
    R.check("T10", "La palette scelta resta dopo aver ricaricato la pagina", pal == "noir", f"palette dopo ricarica: {pal}")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='deep']`)?.click()")

    # T21 nessuna vista è più larga dello schermo (niente scorrimento orizzontale della pagina)
    wide = []
    for v in ["esplora", "contemporanei", "universo", "archivio", "impostazioni"]:
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

    # T01 nessun errore, nessuna richiesta esterna (controllato a fine giro)
    R.check("T01", "Nessun errore JavaScript e nessuna risorsa esterna caricata", not errors and not external,
            "; ".join(errors[:3] + sorted(external)[:3]) or "pulito")
    await p.screenshot(path=f"{OUT}/{name}_fine.png")
    await browser.close()
    return R.rows

async def main():
    async with async_playwright() as pw:
        a, b = await asyncio.gather(run_device(pw, "desktop", {"viewport": {"width": 1440, "height": 900}}, False),
                                    run_device(pw, "iphone13", dict(pw.devices["iPhone 13"]), True))
        rows = a + b
    rows.sort(key=lambda r: (r["code"], r["device"]))
    for r in rows:
        print(f"{r['esito']:8} {r['code']} [{r['device']:8}] {r['name']} — {r['dettaglio']}")
    failed = [r for r in rows if r["esito"] == "FALLITO"]
    print(f"\n{len(rows)} controlli, {len(failed)} falliti, {sum(r['esito']=='NOTO' for r in rows)} difetti noti")
    json.dump(rows, open(f"{OUT}/risultati.json", "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if failed else 0)

asyncio.run(main())
