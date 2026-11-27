"""Albi d'oro con il podio di Giro d'Italia, Tour de France, Formula 1 e Coppa del Mondo di sci (v0.5, 27/11/2026).

Fonti: tabelle di Wikipedia a revisione fissata, estratte nel browser e trascritte in sport/tools/altri/c0..c4.txt,
controllate con l'impronta SHA-256 (primi 16 caratteri) calcolata sia nel browser sia qui.
- c0 Giro e c1 Tour: it.wikipedia, voci «Giro d'Italia» e «Tour de France», tabella Vincitore / Secondo / Terzo.
- c2, c3 Coppa del Mondo di sci alpino, classifica generale uomini e donne: en.wikipedia «FIS Alpine Ski World Cup».
- c4 Formula 1: en.wikipedia, primi tre della classifica piloti nella voce di ogni stagione (revisione per riga);
  i campioni sono stati confrontati, tutti uguali, con «List of Formula One World Drivers' Champions».
"""
import hashlib
import re
from pathlib import Path

from albo_atletica import PAESI as PAESI_EN

DIR = Path(__file__).parent / "altri"
HASH = {"c0": "0d33302b74b697fd", "c1": "ecde37344c5fdfa9", "c2": "cbed3b444fb549f1", "c3": "e5a02c4a90d52a1e",
        "c4": "b2c2991c389c18a0"}
EN = dict(PAESI_EN, **{"United Kingdom": "Gran Bretagna", "Luxembourg": "Lussemburgo", "Liechtenstein": "Liechtenstein",
                       "Slovakia": "Slovacchia", "Monaco": "Monaco", "Belgium": "Belgio"})
# nomi scritti male nella tabella di Wikipedia, o la stessa persona con due nomi
NOMI = {"Ingemark Stenmark": "Ingemar Stenmark", "Maria Höfl-Roesch": "Maria Höfl-Riesch", "Nino Farina": "Giuseppe Farina"}
REV_F1_LISTA, REV_F1_2026 = 1387384745, 1387812162

NOTE = {
    ("giro", 1912): "Quell'anno la classifica fu a squadre.",
    ("giro", 2011): "Vittoria assegnata a Scarponi dopo la squalifica per doping di Alberto Contador.",
    ("tour", 2006): "Vittoria assegnata a Pereiro dopo la squalifica per doping di Floyd Landis.",
    ("tour", 2010): "Vittoria assegnata a Schleck dopo la squalifica per doping di Alberto Contador.",
    ("f1", 1970): "Titolo assegnato dopo la morte di Rindt, nelle prove del Gran Premio d'Italia a Monza.",
}
ARMSTRONG = "Vittoria revocata a Lance Armstrong per doping (2012) e non riassegnata."


def blocchi():
    out = {}
    for k, h in HASH.items():
        t = (DIR / f"{k}.txt").read_text(encoding="utf-8").rstrip("\n")
        assert hashlib.sha256(t.encode()).hexdigest()[:16] == h, f"altri/{k}.txt alterato"
        testa, _, corpo = t.partition("\n")
        out[testa[3:].split("|")[0]] = [r.split("|") for r in corpo.split("\n")]
    return out


def persona(s, inglese):
    s = s.strip()
    if s.lower() in ("non attribuito", ""):
        return ""
    m = re.fullmatch(r"(.+?) \(([^()]+)\)", re.sub(r" \(\d+\)", "", s))
    assert m, s
    nome, paese = m[1].replace("†", "").strip(), m[2]
    nome = NOMI.get(nome, nome)
    if inglese:
        assert paese in EN, f"paese non tradotto: {paese}"
        paese = EN[paese]
    paese = {"Regno Unito": "Gran Bretagna"}.get(paese, paese)
    return f"{nome} ({paese})"


def righe(chiave, B):
    out = []
    inglese = chiave in ("sciM", "sciF", "f1")
    for r in B[chiave]:
        if len(r) < 4:  # «non disputato»
            continue
        etichetta = r[0]
        m = re.fullmatch(r"(\d{4})(?:–(\d{2,4}))?", etichetta)
        assert m, etichetta
        anno = int(m[1]) if not m[2] else int(m[1][:2] + m[2]) if len(m[2]) == 2 else int(m[2])
        oro, arg, bro = (persona(x, inglese) for x in r[1:4])
        riga = {"anno": anno, "sede": "", "oro": oro or "—", "ris": "", "argento": arg or "—", "bronzo": bro or "—"}
        if m[2]:  # «1999–2000» scritto «1999–00» come negli altri albi (v0.7: non entrava nella colonna)
            riga["stag"] = f"{m[1]}–{m[2][-2:]}"
        k = {"sciM": "coppa", "sciF": "coppa"}.get(chiave, chiave)
        nota = NOTE.get((k, anno), "")
        if chiave == "tour" and 1999 <= anno <= 2005:
            nota = ARMSTRONG + (" Terzo posto non attribuito." if not bro else "")
        elif not oro or not bro:
            nota = (nota + " " if nota else "") + ("Primo" if not oro else "Terzo") + " posto non attribuito."
        if nota:
            riga["nota"] = nota
        out.append(riga)
    anni = [x["anno"] for x in out]
    assert anni == sorted(set(anni)), chiave
    return out


def costruisci():
    B = blocchi()
    assert set(B) == {"giro", "tour", "sciM", "sciF", "f1"}
    COL = ["Vincitore", "Secondo", "Terzo"]
    f1 = righe("f1", B)
    f1.append({"anno": 2026, "sede": "", "oro": "Kimi Antonelli (Italia)", "ris": "", "argento": "—", "bronzo": "—",
               "nota": "Stagione in corso: titolo deciso al Gran Premio del Messico (1° novembre 2026); secondo e terzo "
                       "posto si conosceranno dopo le ultime due gare (Qatar 29 novembre, Abu Dhabi 6 dicembre)."})
    W = "https://{}.wikipedia.org/w/index.php?title={}&oldid={}"
    fonte = lambda ist, t, u: {"i": ist, "t": t, "u": u}
    return {
        "ciclismo": [
            {"id": "giro", "nome": "Giro d'Italia", "nota": "Podio della classifica generale. Le edizioni 1915–1918 e 1941–1945 non si sono corse (guerre).",
             "fonti": [fonte("Wikipedia (it)", "Giro d'Italia, albo d'oro (revisione 153194242)", W.format("it", "Giro_d%27Italia", 153194242)),
                       fonte("Giro d'Italia", "Vingegaard makes cycling history, Milan wins in Rome (31 maggio 2026)", "https://www.giroditalia.it/en/news/vingegaard-makes-cycling-history-milan-wins-in-rome/")],
             "tornei": [{"nome": "Uomini", "tipo": "torneo", "colonne": COL, "righe": righe("giro", B)}]},
            {"id": "tour", "nome": "Tour de France", "nota": "Podio della classifica generale. Le edizioni 1915–1918 e 1940–1946 non si sono corse (guerre).",
             "fonti": [fonte("Wikipedia (it)", "Tour de France, albo d'oro (revisione 153048517)", W.format("it", "Tour_de_France", 153048517)),
                       fonte("Euronews", "Tour de France 2026: fifth title for Tadej Pogačar (26 luglio 2026)", "https://euronews.com/2026/07/26/tour-de-france-2026-fifth-title-for-tadej-pogacar-van-der-poel-wins-on-champs-elysees")],
             "tornei": [{"nome": "Uomini", "tipo": "torneo", "colonne": COL, "righe": righe("tour", B)}]},
        ],
        "motori": [
            {"id": "f1", "nome": "Formula 1", "nota": "Primi tre della classifica piloti del Mondiale, stagione per stagione, dal 1950.",
             "fonti": [fonte("Wikipedia (en)", f"List of Formula One World Drivers' Champions (revisione {REV_F1_LISTA})", W.format("en", "List_of_Formula_One_World_Drivers%27_Champions", REV_F1_LISTA)),
                       fonte("Wikipedia (en)", "Voci delle singole stagioni 1950–2025, classifica piloti (revisioni elencate in sport/tools/altri/c4.txt)", W.format("en", "2025_Formula_One_World_Championship", 1387367768)),
                       fonte("Wikipedia (en)", f"2026 Formula One World Championship (revisione {REV_F1_2026})", W.format("en", "2026_Formula_One_World_Championship", REV_F1_2026)),
                       fonte("Al Jazeera", "Kimi Antonelli becomes Formula One's youngest world champion in Mexico City (2 novembre 2026)", "https://www.aljazeera.com/sports/2026/11/2/kimi-antonelli-becomes-formula-ones-youngest-world-champion-in-mexico-city")],
             "tornei": [{"nome": "Piloti", "tipo": "torneo", "colonne": ["Campione", "Secondo", "Terzo"], "righe": f1}]},
        ],
        "sci": [
            {"id": "coppa", "nome": "Coppa del Mondo", "nota": "Podio della classifica generale della Coppa del Mondo di sci alpino, dalla prima edizione (1967).",
             "fonti": [fonte("Wikipedia (en)", "FIS Alpine Ski World Cup (revisione 1387062415)", W.format("en", "FIS_Alpine_Ski_World_Cup", 1387062415)),
                       fonte("FIS", "Another amazing season cements Odermatt's status as all-time great (2025/26)", "https://www.fis-ski.com/alpine-skiing/news/2025-26/-another-amazing-season-cements-odermatt-s-status-as-all-time-great")],
             "tornei": [{"nome": "Uomini", "tipo": "torneo", "colonne": COL, "righe": righe("sciM", B)},
                        {"nome": "Donne", "tipo": "torneo", "colonne": COL, "righe": righe("sciF", B)}]},
        ],
    }
