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
URL = "file://" + HTML
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

async def tap(p, locator, mobile):
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
    p.on("request", lambda r: external.add(r.url) if not r.url.startswith(("file:", "data:", "blob:")) else None)
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
    await set_year(p, -500)
    y = await year(p)
    dock = (await p.text_content("#dockYear")).strip()
    R.check("T03", "Lo slider imposta l'anno e la barra in basso lo segue", y == "500 a.C." and dock == y, f"{y} / dock {dock}")

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
            n_hits > 0 and field == "" and prev_hidden and detail_h == first_name,
            f"{n_hits} risultati, scheda '{detail_h}'")

    # Mappa
    await open_details(p, "#mapView")
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    await set_year(p, -16)
    await p.click("#zoomReset") if await p.is_visible("#zoomReset") else None
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
    R.check("T05", "Tap su un punto: popup con titolo, anno invariato", popup_vis and popup_title != "" and await year(p) == y0,
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
        mb = await m.locator("circle").bounding_box()
        await tap(p, m, mobile)
        await p.wait_for_timeout(250)
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
        const c=document.querySelector(`#pins .map-marker[data-id='${id}'] circle`);if(!c)return {closed:false,gone:true};
        const m=c.getBoundingClientRect(),r=pp.getBoundingClientRect(),a=getComputedStyle(pp,'::after'),below=pp.classList.contains('is-below');
        const tx=r.left+parseFloat(a.left)+7,ty=below?r.top-7:r.bottom+7;
        return {closed:false,dist:Math.hypot(m.left+m.width/2-tx,m.top+m.height/2-ty)}}"""
    pid = await p.evaluate("()=>document.getElementById('mapPointPopup').dataset.itemId")
    await p.evaluate("()=>window.scrollBy(0,60)")
    await p.wait_for_timeout(250)
    after_scroll = await p.evaluate(measure, pid)
    await p.click("#zoomIn", force=True)
    await p.wait_for_timeout(500)
    after_zoom = await p.evaluate(measure, pid)
    ok_scroll = not after_scroll.get("closed") and after_scroll.get("dist", 99) <= 16
    ok_zoom = after_zoom.get("closed") or after_zoom.get("dist", 99) <= 16
    R.check("T13", "Il popup segue il punto dopo scroll della pagina e zoom della mappa (o si chiude se il punto esce)",
            ok_scroll and ok_zoom, f"dopo scroll {after_scroll}, dopo zoom {after_zoom}")
    await p.click("#zoomReset", force=True)
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
    R.check("T07", "'Apri scheda' apre la scheda giusta senza cambiare anno", dh == ptitle and await year(p) == y0, f"'{dh}', anno {y0} -> {await year(p)}")

    # T08 confronto: massimo 5, anno invariato
    await open_details(p, ".secondary-sections")
    y0 = await year(p)
    added = []
    for q in ["roma", "maya", "han", "egitto", "inca", "nazca", "kush"]:
        if len(added) >= 6: break
        await p.fill("#compareSearch", q); await p.wait_for_timeout(250)
        cands = await p.query_selector_all("#compareResults [data-add-compare]")
        for c in cands:
            cid = await c.get_attribute("data-add-compare")
            if cid not in added:
                await c.click(force=True); added.append(cid); await p.wait_for_timeout(200); break
    count_txt = (await p.text_content("#compareCount")).strip()
    n_cmp = await p.evaluate("()=>compareIds.length")
    R.check("T08", "Confronto: al massimo 5 elementi, l'anno non cambia",
            len(added) >= 6 and n_cmp == 5 and count_txt.startswith("5 / 5") and await year(p) == y0,
            f"tentati {len(added)}, presenti {n_cmp}, '{count_txt}', anno {y0} -> {await year(p)}")
    await p.evaluate("()=>{compareIds.slice().forEach(id=>removeCompare(id))}")

    # T09 timeline: lo scorrimento orizzontale non cambia anno né ordine righe
    await open_details(p, ".advanced-exploration")
    await p.evaluate("document.getElementById('timeline').scrollIntoView({behavior:'instant'})")
    await p.wait_for_timeout(300)
    snap = "()=>[...document.querySelectorAll('#timeHtml .time-row .time-label')].map(e=>e.title)"
    win = "()=>[timelineViewMin,timelineViewMax]"
    before, w0, y0 = await p.evaluate(snap), await p.evaluate(win), await year(p)
    await p.evaluate("document.getElementById('timelinebox').scrollIntoView({block:'center',behavior:'instant'})")
    await p.wait_for_timeout(300)
    box = await p.locator("#timelinebox").bounding_box()
    cx, cy = box["x"] + box["width"] * 0.6, box["y"] + min(box["height"] * 0.5, 160)
    hit = await p.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);return e&&e.closest('#timelinebox')?'ok':(e?e.className||e.tagName:'nulla')}", [cx, cy])
    if mobile:   # trascinamento con un dito, eventi touch reali via CDP
        cdp = await p.context.new_cdp_session(p)
        await cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": cx, "y": cy}]})
        for i in range(1, 11):
            await cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": cx - 18 * i, "y": cy}]})
            await p.wait_for_timeout(16)
        await cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    else:        # rotella orizzontale sopra una barra (caso più difficile)
        bar = await p.locator("#timeHtml .time-bar").first.bounding_box()
        if bar:
            cx, cy = bar["x"] + bar["width"] / 2, bar["y"] + bar["height"] / 2
        await p.mouse.move(cx, cy)
        await p.mouse.wheel(400, 0)
    await p.wait_for_timeout(500)
    after, w1, y1 = await p.evaluate(snap), await p.evaluate(win), await year(p)
    common = [t for t in before if t in after]
    order_ok = common == [t for t in after if t in before]
    moved = abs(w1[0] - w0[0]) > 1
    R.check("T09", "Timeline: lo scorrimento sposta la finestra ma non cambia anno né ordine delle righe",
            moved and y1 == y0 and order_ok,
            f"punto toccato: {hit}; finestra {w0[0]}→{round(w1[0])}, anno {y0} -> {y1}, righe in comune {len(common)} ordine {'ok' if order_ok else 'cambiato'}")

    # Indagine (difetto noto): i filtri Civiltà / Siti / Reti agiscono sui punti?
    await p.evaluate("document.getElementById('mappa').scrollIntoView({behavior:'instant'})")
    count = "()=>document.querySelectorAll('#pins .map-marker').length"
    n0 = await p.evaluate(count)
    await p.evaluate("()=>['layerCivil','layerSites','layerNetworks'].forEach(id=>{const c=document.getElementById(id);c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}))})")
    await p.wait_for_timeout(300)
    n1 = await p.evaluate(count)
    await p.evaluate("()=>['layerCivil','layerSites','layerNetworks'].forEach(id=>{const c=document.getElementById(id);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))})")
    R.check("N01", "Filtri mappa Civiltà/Siti/Reti nascondono i punti", n1 < n0, f"punti con tutti i filtri attivi {n0}, tutti spenti {n1}", known=True)

    # T10 palette conservata dopo ricarica
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='noir']`)?.click()")
    await p.reload(wait_until="load"); await p.wait_for_timeout(800)
    pal = await p.evaluate("()=>document.body.dataset.palette")
    R.check("T10", "La palette scelta resta dopo aver ricaricato la pagina", pal == "noir", f"palette dopo ricarica: {pal}")
    await p.evaluate("()=>document.querySelector(`.palette-choice[data-palette='deep']`)?.click()")

    # T01 nessun errore, nessuna richiesta esterna (controllato a fine giro)
    R.check("T01", "Nessun errore JavaScript e nessuna risorsa esterna caricata", not errors and not external,
            "; ".join(errors[:3] + sorted(external)[:3]) or "pulito")
    await p.screenshot(path=f"{OUT}/{name}_fine.png")
    await browser.close()
    return R.rows

async def main():
    async with async_playwright() as pw:
        rows = []
        rows += await run_device(pw, "desktop", {"viewport": {"width": 1440, "height": 900}}, False)
        rows += await run_device(pw, "iphone13", dict(pw.devices["iPhone 13"]), True)
    rows.sort(key=lambda r: (r["code"], r["device"]))
    for r in rows:
        print(f"{r['esito']:8} {r['code']} [{r['device']:8}] {r['name']} — {r['dettaglio']}")
    failed = [r for r in rows if r["esito"] == "FALLITO"]
    print(f"\n{len(rows)} controlli, {len(failed)} falliti, {sum(r['esito']=='NOTO' for r in rows)} difetti noti")
    json.dump(rows, open(f"{OUT}/risultati.json", "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if failed else 0)

asyncio.run(main())
