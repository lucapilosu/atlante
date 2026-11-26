#!/usr/bin/env python3
"""Pilu Sports Almanac: unisce sport/src/almanacco.html e sport/data/almanacco.json in sport/index.html."""
import json
from pathlib import Path

base = Path(__file__).parent
dati = json.loads((base / "data/almanacco.json").read_text(encoding="utf-8"))
for v in dati["voci"]:
    assert v["fonti"], v["id"]
    for f in v["fonti"]:
        assert f["u"].startswith("http"), (v["id"], f)
tpl = (base / "src/almanacco.html").read_text(encoding="utf-8")
js = json.dumps(dati, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
assert tpl.count("/*DATI*/null") == 1
(base / "index.html").write_text(tpl.replace("/*DATI*/null", js), encoding="utf-8")
print(f"sport/index.html: {len(dati['voci'])} tessere, {len(dati['albi'])} albi d'oro")
