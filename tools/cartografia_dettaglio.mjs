// Genera data/mappa-dettaglio.json: cartografia Natural Earth 1:50m (pacchetto npm world-atlas@2, dominio pubblico)
// in tasselli da 30°, proiettata come la mappa della pagina (equirettangolare 900x450).
// Uso: GEO=<cartella con node_modules di topojson-client, mapshaper e il pacchetto world-atlas estratto in GEO/package>
//      node tools/cartografia_dettaglio.mjs 30 data/mappa-dettaglio.json
import fs from 'fs';
const {feature, mesh} = await import((process.env.GEO || '.') + '/node_modules/topojson-client/src/index.js');
const {default: mapshaper} = await import((process.env.GEO || '.') + '/node_modules/mapshaper/mapshaper.js');
const TILE = Number(process.argv[2] || 30), DEC = 2;
const land = JSON.parse(fs.readFileSync((process.env.GEO || '.') + '/package/land-50m.json', 'utf8'));
const countries = JSON.parse(fs.readFileSync((process.env.GEO || '.') + '/package/countries-50m.json', 'utf8'));
const landF = feature(land, land.objects.land);
const landGeom = landF.type === 'FeatureCollection' ? {type: 'MultiPolygon', coordinates: landF.features.flatMap(f => f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates)} : landF.geometry;
const landGeo = {type: 'Feature', properties: {}, geometry: fixPolygons(landGeom)};
const coastGeo = {type: 'Feature', properties: {}, geometry: splitLines(mesh(land, land.objects.land))};          // contorni delle terre (linee)
const borderGeo = {type: 'Feature', properties: {}, geometry: splitLines(mesh(countries, countries.objects.countries, (a, b) => a !== b))}; // confini interni
// --- antimeridiano: in coordinate piane un segmento da +180 a -180 attraversa tutta la mappa ---
// linee (coste, confini): si spezzano dove un segmento salta più di 90° di longitudine (nessuna costa reale lo fa)
function splitLines(geom) {
  const lines = geom.type === 'LineString' ? [geom.coordinates] : geom.type === 'MultiLineString' ? geom.coordinates : [];
  const out = [];
  lines.forEach(l => { let cur = [l[0]]; for (let i = 1; i < l.length; i++) { if (Math.abs(l[i][0] - l[i - 1][0]) > 90) { if (cur.length > 1) out.push(cur); cur = [l[i]]; } else cur.push(l[i]); } if (cur.length > 1) out.push(cur); });
  return {type: 'MultiLineString', coordinates: out};
}
// poligoni (terre) che attraversano l'antimeridiano: si "srotolano" e se ne aggiungono copie spostate di ±360°,
// così il ritaglio sui tasselli tiene le due metà. L'Antartide (che chiude lungo il bordo inferiore) resta com'è.
function fixPolygons(geom) {
  const polys = geom.type === 'Polygon' ? [geom.coordinates] : geom.type === 'MultiPolygon' ? geom.coordinates : [];
  const out = [];
  polys.forEach(poly => {
    const outer = poly[0];
    const crosses = outer.some((c, i) => i && Math.abs(c[0] - outer[i - 1][0]) > 180);
    const antarctic = Math.min(...outer.map(c => c[1])) < -60;
    if (!crosses || antarctic) { out.push(poly); return; }
    const unwrap = ring => { let off = 0; return ring.map((c, i) => { if (i) { const d = c[0] - ring[i - 1][0]; if (d > 180) off -= 360; else if (d < -180) off += 360; } return [c[0] + off, c[1]]; }); };
    const u = poly.map(unwrap);
    [-360, 0, 360].forEach(sh => out.push(u.map(r => r.map(([x, y]) => [x + sh, y]))));
  });
  return {type: 'MultiPolygon', coordinates: out};
}
const fx = v => { const r = Number(v.toFixed(DEC)); return (Object.is(r, -0) ? 0 : r).toString(); };
const proj = ([lon, lat]) => [(lon + 180) * 2.5, (90 - lat) * 2.5];
function encode(geom, close) {
  let d = '', pts = 0;
  const ring = cs => { let s = '', px = 0, py = 0, n = 0;
    cs.forEach((c, i) => { const [x0, y0] = proj(c); const X = Number(x0.toFixed(DEC)), Y = Number(y0.toFixed(DEC));
      if (i === 0) s += `M${fx(X)} ${fx(Y)}`; else { const dx = X - px, dy = Y - py; if (Math.abs(dx) < 1e-9 && Math.abs(dy) < 1e-9) return; s += `l${fx(dx)} ${fx(dy)}`; }
      px = X; py = Y; n++; });
    if (n > 1) { d += close ? s + 'z' : s; pts += n; } };
  const walk = g => { if (!g) return;
    if (g.type === 'Polygon') g.coordinates.forEach(ring);
    else if (g.type === 'MultiPolygon') g.coordinates.forEach(p => p.forEach(ring));
    else if (g.type === 'LineString') ring(g.coordinates);
    else if (g.type === 'MultiLineString') g.coordinates.forEach(ring);
    else if (g.type === 'GeometryCollection') g.geometries.forEach(walk); };
  walk(geom); return [d, pts];
}
async function clip(fc, bbox) {
  const out = await mapshaper.applyCommands(`-i in.json -clip bbox=${bbox.join(',')} -o out.json format=geojson`, {'in.json': fc});
  const g = JSON.parse(out['out.json']);
  return g.type === 'FeatureCollection' ? g.features.map(f => f.geometry) : [g.geometry || g];
}
const tiles = [];
let tot = {fill: 0, coast: 0, border: 0};
for (let lon = -180; lon < 180; lon += TILE) for (let lat = -90; lat < 90; lat += TILE) {
  const bbox = [lon, lat, lon + TILE, Math.min(90, lat + TILE)];
  const t = {bbox};
  for (const [key, fc, close] of [['fill', landGeo, true], ['coast', {type: 'FeatureCollection', features: [coastGeo]}, false], ['border', {type: 'FeatureCollection', features: [borderGeo]}, false]]) {
    const geoms = await clip(fc, bbox);
    let d = '', n = 0; geoms.forEach(g => { const [s, k] = encode(g, close); d += s; n += k; });
    if (n) { t[key] = d; tot[key] += n; }
  }
  if (t.fill || t.coast || t.border) tiles.push(t);
}
fs.writeFileSync(process.argv[3], JSON.stringify(tiles));
const size = tiles.reduce((a, t) => a + (t.fill || '').length + (t.coast || '').length + (t.border || '').length, 0);
console.log(`tasselli ${tiles.length}, punti`, tot, `dimensione ${Math.round(size / 1024)} KB`);
