// Raccolta candidate foto v0.73 — da eseguire nel browser integrato (pagina wikidata.org)
(async () => {
  const BASE = 'https://raw.githubusercontent.com/lucapilosu/atlante/foto-v073/tools/foto/v073/';
  const M = await (await fetch(BASE + 'mappa.json?' + Date.now())).json();
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  async function getJSON(url, tries = 6) {
    let wait = 800;
    for (let i = 0; i < tries; i++) {
      try {
        const r = await fetch(url, { cache: 'no-store', priority: 'high' });
        if (r.status === 429 || r.status >= 500) { await sleep(wait); wait *= 2; continue; }
        if (r.status === 404) return null;
        return await r.json();
      } catch (e) { await sleep(wait); wait *= 2; }
    }
    return null;
  }
  async function pool(items, n, fn) {
    const out = new Array(items.length); let i = 0;
    await Promise.all(Array.from({ length: n }, async () => {
      while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); }
    }));
    return out;
  }
  const S = window.FOTO = { log: [], cand: {} };
  // 1. immagini delle pagine
  const pageFiles = {}; // id -> [{f, src, pi}]
  for (const [id, m] of Object.entries(M)) pageFiles[id] = [];
  const jobs = [];
  for (const [id, m] of Object.entries(M)) {
    for (const t of m.en) jobs.push([id, 'en', t]);
    for (const t of m.it) jobs.push([id, 'it', t]);
  }
  await pool(jobs, 4, async ([id, lang, t]) => {
    const u = `https://${lang}.wikipedia.org/w/api.php?action=query&format=json&origin=*&redirects=1&prop=images|pageimages|pageprops&ppprop=wikibase_item&piprop=name&imlimit=max&titles=` + encodeURIComponent(t);
    const j = await getJSON(u);
    const pages = j && j.query && j.query.pages ? Object.values(j.query.pages) : [];
    for (const p of pages) {
      if (p.missing !== undefined) { S.log.push('manca ' + lang + ':' + t); continue; }
      const pi = p.pageimage ? p.pageimage.replace(/_/g, ' ') : null;
      if (pi) pageFiles[id].push({ f: pi, src: lang + ':' + p.title, pi: 1 });
      if (p.pageprops && p.pageprops.wikibase_item) {
        const w = await getJSON('https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&origin=*&property=P18&entity=' + p.pageprops.wikibase_item);
        const c = w && w.claims && w.claims.P18 ? w.claims.P18 : [];
        for (const x of c) pageFiles[id].push({ f: x.mainsnak.datavalue.value, src: 'wd:' + p.pageprops.wikibase_item, pi: 1 });
      }
      for (const im of (p.images || [])) pageFiles[id].push({ f: im.title.replace(/^(File|Immagine|Image):/, ''), src: lang + ':' + p.title, pi: 0 });
    }
  });
  // 2. informazioni dei file su Commons
  const all = [...new Set(Object.values(pageFiles).flat().map(x => x.f))].filter(f => /\.(jpe?g|png)$/i.test(f));
  S.log.push('file jpg/png: ' + all.length);
  const info = {};
  const chunks = []; for (let i = 0; i < all.length; i += 40) chunks.push(all.slice(i, i + 40));
  await pool(chunks, 3, async ch => {
    const u = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*&prop=imageinfo&iiprop=size|mime|url|extmetadata&iiextmetadatafilter=Artist|LicenseShortName&titles=' + encodeURIComponent(ch.map(f => 'File:' + f).join('|'));
    const j = await getJSON(u);
    const norm = {}; for (const n of ((j && j.query && j.query.normalized) || [])) norm[n.to] = n.from;
    for (const p of Object.values((j && j.query && j.query.pages) || {})) {
      if (!p.imageinfo) continue;
      const ii = p.imageinfo[0]; const em = ii.extmetadata || {};
      const name = p.title.replace(/^File:/, '');
      const artist = em.Artist ? em.Artist.value.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim() : '';
      const lic = em.LicenseShortName ? em.LicenseShortName.value : '';
      info[name] = { w: ii.width, h: ii.height, url: ii.url.split('?')[0], a: artist, l: lic };
    }
  });
  // 3. filtro e visualizzazioni
  const keep = {};
  for (const [id, arr] of Object.entries(pageFiles)) {
    const seen = new Set(); const kw = M[id].kw.map(k => k.toLowerCase());
    keep[id] = [];
    for (const x of arr) {
      if (seen.has(x.f)) { if (x.pi) keep[id].forEach(y => { if (y.f === x.f) y.pi = 1; }); continue; }
      seen.add(x.f);
      const i = info[x.f]; if (!i) continue;
      if (Math.max(i.w, i.h) < 500 || Math.min(i.w, i.h) < 300) continue;
      if (!i.l) continue;
      const low = x.f.toLowerCase().replace(/_/g, ' ');
      const rel = x.pi || kw.some(k => low.includes(k)) ? 1 : 0;
      keep[id].push({ f: x.f, src: x.src, pi: x.pi, rel, ...i });
    }
  }
  // visualizzazioni solo per le prime 12 di ogni voce (prima le pertinenti, nell'ordine della pagina)
  for (const id of Object.keys(keep)) { keep[id].sort((a, b) => b.rel - a.rel); keep[id] = keep[id].slice(0, 12); }
  const files = [...new Set(Object.values(keep).flat().map(x => x.f))];
  S.log.push('candidate valide: ' + files.length);
  const views = {};
  await pool(files, 3, async f => {
    const path = decodeURIComponent(info[f].url.replace('https://upload.wikimedia.org', ''));
    const u = 'https://wikimedia.org/api/rest_v1/metrics/mediarequests/per-file/all-referers/user/' + encodeURIComponent(path) + '/monthly/20251101/20261031';
    const j = await getJSON(u);
    views[f] = j && j.items ? j.items.reduce((s, x) => s + (x.requests || 0), 0) : 0;
  });
  for (const id of Object.keys(keep)) {
    keep[id].forEach(x => x.v = views[x.f] || 0);
    keep[id].sort((a, b) => (b.rel - a.rel) || (b.v - a.v));
    S.cand[id] = keep[id].slice(0, 8);
  }
  S.done = true;
})();
