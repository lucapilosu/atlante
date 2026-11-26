#!/usr/bin/env python3
"""Pilu Sports Almanac: unisce sport/src/almanacco.html e sport/data/almanacco.json in sport/index.html.

Scrive anche sport/atleti.json (palmarès, scaricato dalla pagina solo quando serve) e sport/versione.json
(impronta del contenuto: la pagina la confronta con la propria per proporre l'aggiornamento)."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).parent
dati = json.loads((base / "data/almanacco.json").read_text(encoding="utf-8"))
for v in dati["voci"]:
    assert v["fonti"], v["id"]
    for f in v["fonti"]:
        assert f["u"].startswith("http"), (v["id"], f)
for sp, a in dati["albi"].items():
    for g in a["gruppi"]:
        assert g["fonti"] and all(f["u"].startswith("http") for f in g["fonti"]), (sp, g["id"])
        for t in g["tornei"]:
            assert t["tipo"] in ("torneo", "lega") and t["righe"], (sp, g["id"], t["nome"])
            chiavi = [r.get("stag") or str(r["anno"]) for r in t["righe"]]
            assert len(chiavi) == len(set(chiavi)), (sp, g["id"], t["nome"], "righe doppie")
atl = json.loads((base / "data/atleti.json").read_text(encoding="utf-8"))
ids = [a["id"] for a in atl]
assert len(ids) == len(set(ids)), "atleti doppi"
for a in atl:
    assert a["fonti"] and all(f["u"].startswith("http") for f in a["fonti"]), a["id"]
    assert set(a["sport"]) <= {s["id"] for s in dati["sport"]} and a["genere"] in ("Uomini", "Donne"), a["id"]
    for p in a["palmares"]:
        if "albo" in p:  # il collegamento deve portare a una riga che esiste davvero
            sp, gid, ti, k = p["albo"].split("|")
            t = next(g for g in dati["albi"][sp]["gruppi"] if g["id"] == gid)["tornei"][int(ti)]
            assert any((r.get("stag") or str(r["anno"])) == k for r in t["righe"]), (a["id"], p)
atl_js = json.dumps(atl, ensure_ascii=False, separators=(",", ":"))
tpl = (base / "src/almanacco.html").read_text(encoding="utf-8")
js = json.dumps(dati, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
assert tpl.count("/*DATI*/null") == 1 and tpl.count("/*VERSIONE*/''") == 1
v = hashlib.sha256((tpl + js + atl_js).encode()).hexdigest()[:10]
(base / "index.html").write_text(tpl.replace("/*DATI*/null", js).replace("/*VERSIONE*/''", json.dumps(v)), encoding="utf-8")
(base / "atleti.json").write_text(atl_js, encoding="utf-8")
(base / "versione.json").write_text(json.dumps({"v": v}), encoding="utf-8")
print(f"sport/index.html: {len(dati['voci'])} tessere, {sum(len(t['righe']) for a in dati['albi'].values() for g in a['gruppi'] for t in g['tornei'])} righe di albo d'oro in {len(dati['albi'])} sport; "
      f"sport/atleti.json: {len(atl)} atleti; versione {v}")
