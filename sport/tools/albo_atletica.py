"""Albo d'oro olimpico dell'atletica: solo le gare del programma attuale (scelta di Luca, 26/11/2026).

Fonte: tabelle di Wikipedia «List of Olympic medalists in athletics (men/women)», revisioni fissate,
trascritte in sport/tools/atletica/a0..a5.txt e verificate con impronta SHA-256 (primi 16 caratteri)
calcolata sia nel browser sul testo estratto sia qui sul file.
"""
import hashlib
import re
from pathlib import Path

DIR = Path(__file__).parent / "atletica"
HASH = {"a0": "6d1f27023c0d67a5", "a1": "0a9e54f22ca4de56", "a2": "45183e2268554427",
        "a3": "00ccdf8a88aebdfd", "a4": "baa245c48e46a6d9", "a5": "b72931b3754768cb"}
REV_M, REV_F = 1379935508, 1379934565

GARE = [("100 metres", "100 m"), ("200 metres", "200 m"), ("400 metres", "400 m"), ("5000 metres", "5000 m"),
        ("10,000 metres", "10.000 m"), ("Marathon", "Maratona"), ("4 × 100 metres relay", "Staffetta 4×100"),
        ("4 × 400 metres relay", "Staffetta 4×400"), ("High jump", "Salto in alto"),
        ("Pole vault", "Salto con l'asta"), ("Long jump", "Salto in lungo")]
GENERI = [("M", "Uomini"), ("F", "Donne"), ("X", "Misti")]

SEDI = {1896: "Atene", 1900: "Parigi", 1904: "Saint Louis", 1908: "Londra", 1912: "Stoccolma", 1920: "Anversa",
        1924: "Parigi", 1928: "Amsterdam", 1932: "Los Angeles", 1936: "Berlino", 1948: "Londra", 1952: "Helsinki",
        1956: "Melbourne", 1960: "Roma", 1964: "Tokyo", 1968: "Città del Messico", 1972: "Monaco di Baviera",
        1976: "Montréal", 1980: "Mosca", 1984: "Los Angeles", 1988: "Seul", 1992: "Barcellona", 1996: "Atlanta",
        2000: "Sydney", 2004: "Atene", 2008: "Pechino", 2012: "Londra", 2016: "Rio de Janeiro", 2020: "Tokyo",
        2024: "Parigi"}

PAESI = {
    "United States": "Stati Uniti", "Great Britain": "Gran Bretagna", "Greece": "Grecia", "Hungary": "Ungheria",
    "France": "Francia", "Sweden": "Svezia", "South Africa": "Sudafrica", "Finland": "Finlandia", "Estonia": "Estonia",
    "Italy": "Italia", "Chile": "Cile", "Argentina": "Argentina", "Japan": "Giappone", "Belgium": "Belgio",
    "Czechoslovakia": "Cecoslovacchia", "Yugoslavia": "Jugoslavia", "Ethiopia": "Etiopia", "Morocco": "Marocco",
    "New Zealand": "Nuova Zelanda", "East Germany": "Germania Est", "West Germany": "Germania Ovest",
    "Netherlands": "Paesi Bassi", "Soviet Union": "Unione Sovietica", "Portugal": "Portogallo", "Ireland": "Irlanda",
    "Kenya": "Kenya", "Djibouti": "Gibuti", "South Korea": "Corea del Sud", "Germany": "Germania",
    "Brazil": "Brasile", "Uganda": "Uganda", "Canada": "Canada", "Poland": "Polonia", "Cuba": "Cuba",
    "Jamaica": "Giamaica", "Nigeria": "Nigeria", "Trinidad and Tobago": "Trinidad e Tobago", "China": "Cina",
    "Australia": "Australia", "Bahamas": "Bahamas", "Botswana": "Botswana", "Norway": "Norvegia",
    "Philippines": "Filippine", "Russia": "Russia", "Algeria": "Algeria", "Czech Republic": "Repubblica Ceca",
    "Qatar": "Qatar", "Ukraine": "Ucraina", "Belarus": "Bielorussia", "Denmark": "Danimarca",
    "Unified Team": "Squadra Unificata", "Spain": "Spagna", "Haiti": "Haiti", "Panama": "Panama",
    "United Team of Germany": "Squadra unificata tedesca", "British West Indies": "Indie Occidentali Britanniche",
    "Saint Lucia": "Santa Lucia", "Namibia": "Namibia", "Bahrain": "Bahrein", "Dominican Republic": "Repubblica Dominicana",
    "Sri Lanka": "Sri Lanka", "Mexico": "Messico", "Colombia": "Colombia", "Romania": "Romania", "Bulgaria": "Bulgaria",
    "Austria": "Austria", "Croatia": "Croazia", "Iceland": "Islanda", "ROC": "ROC (Russia)", "Serbia": "Serbia",
    "Grenada": "Grenada", "Tanzania": "Tanzania", "Mozambique": "Mozambico", "Burundi": "Burundi", "Eritrea": "Eritrea",
    "Switzerland": "Svizzera", "Barbados": "Barbados", "Zambia": "Zambia", "Venezuela": "Venezuela",
    "Ivory Coast": "Costa d'Avorio", "Senegal": "Senegal", "Tunisia": "Tunisia", "Ecuador": "Ecuador",
    "Guatemala": "Guatemala", "India": "India", "Turkey": "Turchia", "Lithuania": "Lituania", "Latvia": "Lettonia",
    "Slovenia": "Slovenia", "Bohemia": "Boemia", "Puerto Rico": "Porto Rico",
}
NON_ASSEGNATO = {"none awarded", "None awarded", "Vacant"}


def blocchi():
    out = {}
    for k, h in HASH.items():
        t = (DIR / f"{k}.txt").read_text(encoding="utf-8").rstrip("\n")
        assert hashlib.sha256(t.encode()).hexdigest()[:16] == h, f"atletica/{k}.txt alterato"
        for sez in t.split("## ")[1:]:
            testa, _, corpo = sez.partition("\n")
            g, gara = testa.split("|")
            assert (g, gara) not in out, (g, gara)
            out[(g, gara)] = [r.split("|") for r in corpo.rstrip("\n").split("\n")]
    return out


def paese(s):
    if s not in PAESI:
        raise KeyError(f"paese non tradotto: {s!r}")
    return PAESI[s]


def nome(s, staffetta):
    s = s.strip()
    if staffetta:
        return paese(s)
    m = re.fullmatch(r"(.+) \(([^()]+)\)", s)
    assert m, f"atleta senza paese: {s!r}"
    return f"{m[1]} ({paese(m[2])})"


def cella(s, staffetta):
    """-> (testo, numero di medagliati). '' se non assegnata."""
    s = s.strip()
    if s in NON_ASSEGNATO:
        return "", 0
    parti = [p for p in s.split(" ; ")]
    return ", ".join(nome(p, staffetta) for p in parti), len(parti)


CORREZIONI = {
    # La cella della tabella contiene due collegamenti separati (atleta e bandiera): ricomposta a mano.
    ("F", "High jump", "1952", 3): ("Aleksandra Chudina (?) ; Soviet Union (?)", "Aleksandra Chudina (Soviet Union)"),
}
NOTE = {
    ("F", "100 metres", "2000"): "Oro revocato a Marion Jones (Stati Uniti) per doping e non riassegnato.",
}


def costruisci():
    B = blocchi()
    attese = {(g, e) for g, _ in GENERI[:2] for e, _ in GARE} | {("X", "4 × 400 metres relay")}
    assert set(B) == attese, set(B) ^ attese
    tornei = []
    for g, gen in GENERI:
        for e, it in GARE:
            if (g, e) not in B:
                continue
            staff = "relay" in e
            righe = []
            for r in B[(g, e)]:
                assert len(r) == 4, r
                for (cg, ce, ca, ci), (vecchio, nuovo) in CORREZIONI.items():
                    if (cg, ce, ca) == (g, e, r[0]):
                        assert r[ci] == vecchio, r
                        r[ci] = nuovo
                anno = int(r[0])
                (oro, no), (arg, na), (bro, nb) = (cella(x, staff) for x in r[1:])
                note = ["oro ex aequo"] if no > 1 else []
                if not arg and not bro:
                    note.append("argento e bronzo non assegnati")
                else:
                    note += ["argento non assegnato"] if not arg else ["argento ex aequo"] if na > 1 else []
                    note += ["bronzo non assegnato"] if not bro else ["bronzo ex aequo"] if nb > 1 else []
                testo = "; ".join(note)
                testo = testo[:1].upper() + testo[1:] + "." if testo else ""
                if (g, e, r[0]) in NOTE:
                    testo = (NOTE[(g, e, r[0])] + " " + testo).strip()
                riga = {"anno": anno, "sede": SEDI[anno], "oro": oro or "—", "ris": "",
                        "argento": arg or "—", "bronzo": bro or "—"}
                if testo:
                    riga["nota"] = testo
                righe.append(riga)
            assert [r["anno"] for r in righe] == sorted({r["anno"] for r in righe}), (g, e)
            tornei.append({"nome": it if g != "X" else it + " mista", "genere": gen, "tipo": "torneo", "righe": righe})
    return tornei
