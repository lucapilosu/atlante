"""Costruisce index.html a partire dal modello e dai dati.

    python3 build.py

- src/atlante.html  modello della pagina (HTML, CSS, JavaScript) con i segnaposto
                    __ATLANTE_DATI__, {{VERSIONE}} e {{DATA}}
- data/atlante.json dati dell'atlante (voci, eventi, fonti)
- versione.json     numero di versione e data mostrati nella pagina

Il risultato è un unico file autonomo, che si apre anche senza connessione.
Prima di scriverlo controlla i dati: gli errori bloccano la costruzione,
gli avvisi vengono solo segnalati.
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def controlla(db):
    errori, avvisi = [], []
    voci = db["entities"] + db["events"]
    conta = Counter(v["id"] for v in voci)
    errori += [f"id duplicato: {i}" for i, n in conta.items() if n > 1]
    ids = set(conta)
    fonti = {f["id"] for f in db["sources"]}
    for v in voci:
        a, b = v.get("start_year"), v.get("end_year")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            errori.append(f"{v['id']}: anni non numerici ({a}, {b})")
        elif a > b:
            errori.append(f"{v['id']}: inizio {a} dopo la fine {b}")
        for s in v.get("source_ids") or []:
            if s not in fonti:
                errori.append(f"{v['id']}: fonte inesistente {s}")
        rif = (v.get("related_entities") or []) + (v.get("related_entity_ids") or [])
        for r in rif:
            if r not in ids:
                avvisi.append(f"{v['id']}: collegamento a voce inesistente {r}")
        if not v.get("source_ids"):
            avvisi.append(f"{v['id']}: nessuna fonte")
        # v0.52 · immagini da Wikimedia Commons: nome del file, cartella, autore e licenza obbligatori
        for im in v.get("images") or []:
            if not (im.get("f") and len(im.get("h", "")) == 2 and im.get("a") and im.get("l")):
                errori.append(f"{v['id']}: immagine incompleta {im}")
        if len(v.get("images") or []) > 3:
            errori.append(f"{v['id']}: più di 3 immagini")

    # v0.47 · vista Tecnologia: ogni attestazione deve avere ambito, area, anni e fonti valide
    ambiti = {d["id"] for d in db.get("technology_domains", [])}
    aree = {"Europa", "Asia", "Africa", "Americhe", "Oceania"}
    visti = set()
    for t in db.get("technologies", []):
        i = t.get("id", "?")
        if i in visti or i in ids:
            errori.append(f"{i}: id duplicato (attestazioni tecniche)")
        visti.add(i)
        if t.get("domain") not in ambiti:
            errori.append(f"{i}: ambito sconosciuto {t.get('domain')}")
        if t.get("region") not in aree:
            errori.append(f"{i}: area non valida {t.get('region')}")
        a, b = t.get("start_year"), t.get("end_year")
        if not isinstance(a, int) or not isinstance(b, int):
            errori.append(f"{i}: anni non interi ({a}, {b})")
        elif a > b:
            errori.append(f"{i}: inizio {a} dopo la fine {b}")
        elif 0 in (a, b):
            errori.append(f"{i}: l’anno 0 non esiste")
        if not t.get("source_ids"):
            errori.append(f"{i}: attestazione senza fonti")
        for s in t.get("source_ids") or []:
            if s not in fonti:
                errori.append(f"{i}: fonte inesistente {s}")
        for r in t.get("related_ids") or []:
            if r not in ids:
                avvisi.append(f"{i}: collegamento a voce inesistente {r}")
    return errori, avvisi


def main():
    modello = (ROOT / "src/atlante.html").read_text(encoding="utf-8")
    db = json.loads((ROOT / "data/atlante.json").read_text(encoding="utf-8"))
    ver = json.loads((ROOT / "versione.json").read_text(encoding="utf-8"))

    errori, avvisi = controlla(db)
    senza_fonti = sum(a.endswith("nessuna fonte") for a in avvisi)
    altri = [a for a in avvisi if not a.endswith("nessuna fonte")]
    for a in altri:
        print("avviso:", a)
    if senza_fonti:
        print(f"avviso: {senza_fonti} voci senza fonti")
    if errori:
        for e in errori:
            print("ERRORE:", e)
        sys.exit("Costruzione interrotta: correggere i dati.")

    dati = json.dumps(db, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    for segno in ("__ATLANTE_DATI__", "{{VERSIONE}}", "{{DATA}}"):
        if segno not in modello:
            sys.exit(f"Segnaposto mancante nel modello: {segno}")
    pagina = (modello.replace("__ATLANTE_DATI__", dati)
                     .replace("{{VERSIONE}}", ver["versione"])
                     .replace("{{DATA}}", ver["data"]))
    (ROOT / "index.html").write_text(pagina, encoding="utf-8")
    print(f"index.html v{ver['versione']}: {len(db['entities'])} entità, "
          f"{len(db['events'])} eventi, {len(db.get('technologies', []))} attestazioni tecniche, "
          f"{len(db['sources'])} fonti")


if __name__ == "__main__":
    main()
