#!/usr/bin/env python3
"""Applica a data/atlante.json una selezione di foto nel formato "diff".

Formato (una riga per foto, nell'ordine in cui compare nella scheda):
  voce|=N                      -> tiene la N-esima foto (da 0) che la voce ha già
  voce|h|file|autore|licenza   -> foto nuova da Wikimedia Commons
Le voci che non compaiono nel file restano senza foto.

Uso: python3 tools/foto/applica_selezione.py tools/foto/diff_v054.txt tools/foto/selezione_v054.tsv
"""
import hashlib
import json
import re
import sys

DATA = "data/atlante.json"
# Foto da togliere dopo il controllo finale (voce, file)
SCARTA = {("event-su-nuraxi-main-tower", "Central tower of the Nuraghe at Saint Antine of Torralba.jpg")}

SCONOSCIUTO = re.compile(r"^(unknown|anonymous)[^|]*$", re.I)


def pulisci_autore(a: str) -> str:
    a = a.strip()
    m = re.match(r"^No machine-readable author provided\. (.+?) assumed", a)
    if m:
        a = m.group(1)
    a = re.sub(r"^\[\S+ (.+)\]$", r"\1", a)            # [url Nome] -> Nome
    a = re.sub(r"^(Author|Photographer|Painting): ", "", a)
    a = re.sub(r"^\(cc\) ", "", a)
    a = re.sub(r"^- ", "", a)
    if SCONOSCIUTO.match(a) or re.fullmatch(r"(Unknown\w* ?\w*)+\.?", a):
        return "Autore sconosciuto"
    if len(a) > 45 or "http" in a or "uploader" in a.lower() or "Photo Credit" in a:
        return "Vedi Wikimedia Commons"
    return a


def h2(nome: str) -> str:
    return hashlib.md5(nome.replace(" ", "_").encode()).hexdigest()[:2]


def main(diff_path: str, tsv_out: str) -> None:
    d = json.load(open(DATA, encoding="utf-8"))
    recs = {x["id"]: x for k in ("entities", "events") for x in d[k]}
    nuove: dict[str, list] = {}
    for riga in open(diff_path, encoding="utf-8"):
        riga = riga.rstrip("\n")
        if not riga:
            continue
        parti = riga.split("|")
        vid = parti[0]
        if vid not in recs:
            sys.exit(f"voce sconosciuta: {vid}")
        if parti[1].startswith("="):
            im = dict(recs[vid]["images"][int(parti[1][1:])])
        else:
            _, h, f, a, l = parti
            im = {"f": f, "h": h, "a": pulisci_autore(a), "l": l}
        if (vid, im["f"]) in SCARTA:
            continue
        if h2(im["f"]) != im["h"]:
            sys.exit(f"hash non corrispondente: {vid} {im['f']}")
        nuove.setdefault(vid, []).append(im)
    for vid, x in recs.items():
        if vid in nuove:
            x["images"] = nuove[vid][:3]
        else:
            x.pop("images", None)
    with open(DATA, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    with open(tsv_out, "w", encoding="utf-8") as fh:
        for vid, ims in nuove.items():
            for im in ims:
                fh.write("|".join([vid, im["h"], im["f"], im["a"], im["l"]]) + "\n")
    tot = sum(len(v) for v in nuove.values())
    print(f"voci con foto: {len(nuove)}  foto: {tot}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
