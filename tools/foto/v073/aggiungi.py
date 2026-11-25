#!/usr/bin/env python3
"""v0.73: aggiunge foto alle voci che non ne hanno (non tocca le altre).

Formato del file: una riga per foto, nell'ordine della scheda
  voce|h|file|autore|licenza
Uso: python3 tools/foto/v073/aggiungi.py tools/foto/v073/selezione_v073.tsv
"""
import json
import sys

sys.path.insert(0, "tools/foto")
from applica_selezione import h2, pulisci_autore  # noqa: E402

DATA = "data/atlante.json"


def main(path: str) -> None:
    d = json.load(open(DATA, encoding="utf-8"))
    recs = {x["id"]: x for k in ("entities", "events") for x in d[k]}
    nuove: dict[str, list] = {}
    for riga in open(path, encoding="utf-8"):
        riga = riga.rstrip("\n")
        if not riga or riga.startswith("#"):
            continue
        vid, h, f, a, l = riga.split("|")
        if vid not in recs:
            sys.exit(f"voce sconosciuta: {vid}")
        if recs[vid].get("images"):
            sys.exit(f"la voce ha già foto: {vid}")
        if h2(f) != h:
            sys.exit(f"hash non corrispondente: {vid} {f}")
        nuove.setdefault(vid, []).append({"f": f, "h": h, "a": pulisci_autore(a), "l": l})
    for vid, ims in nuove.items():
        if len(ims) > 3:
            sys.exit(f"più di 3 foto: {vid}")
        recs[vid]["images"] = ims
    with open(DATA, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)

    print(f"voci con foto nuove: {len(nuove)}  foto: {sum(len(v) for v in nuove.values())}")


if __name__ == "__main__":
    main(sys.argv[1])
