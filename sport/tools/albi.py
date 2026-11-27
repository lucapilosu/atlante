"""Albi d'oro non olimpici: Mondiali, Europei e campionati nazionali.

Legge sport/tools/albi_grezzi.txt (tabelle di Wikipedia trascritte il 26/11/2026, verificate per sezione
con SHA-256 calcolato nel browser) e le normalizza in italiano. Usato da dati.py.
"""
import hashlib
import re
from pathlib import Path

GREZZI = Path(__file__).with_name("albi_grezzi.txt")
# SHA-256 (primi 16 caratteri) di ogni sezione, calcolato nel browser sulle tabelle estratte
HASH = {"calcio_mondiali_m": "2a8ace5e76b31e9e", "calcio_mondiali_f": "47a48801d4168d16", "calcio_europei": "c9686905a2c6a675",
        "basket_mondiali_m": "44cd02e01ccb43d5", "basket_mondiali_f": "f2aa01be22d3f926", "basket_euro_m": "b389141188557e76",
        "basket_euro_f": "a0296e053014fcae", "volley_mondiali_m": "3ef72c15bef7d22d", "volley_mondiali_f": "d15779676e0d191d",
        "volley_euro_m": "efe5b32c0074c5bc", "volley_euro_f": "936c9c8c69e75996", "beach_mondiali_m": "3991c678fdf3b598",
        "beach_mondiali_f": "1fb6a4d6b9678861", "calcio_seriea": "400361f382bb4331", "basket_nba": "a9d9ed6e814108a9",
        "volley_ita_m": "0953a242c2ecba72", "volley_ita_f": "b2cb8c0ac6e49037"}

PAESI = {
    "United States": "Stati Uniti", "Canada": "Canada", "Mexico": "Messico", "Poland": "Polonia", "France": "Francia",
    "Brazil": "Brasile", "Soviet Union": "Unione Sovietica", "USSR": "Unione Sovietica", "Uruguay": "Uruguay",
    "Argentina": "Argentina", "Italy": "Italia", "Puerto Rico": "Porto Rico", "Yugoslavia": "Jugoslavia", "Cuba": "Cuba",
    "Spain": "Spagna", "Australia": "Australia", "Croatia": "Croazia", "Lithuania": "Lituania",
    "FR Yugoslavia": "RF Jugoslavia", "Russia": "Russia", "Serbia": "Serbia", "Slovenia": "Slovenia", "Germany": "Germania",
    "Bulgaria": "Bulgaria", "Czechoslovakia": "Cecoslovacchia", "South Korea": "Corea del Sud", "China": "Cina",
    "Hungary": "Ungheria", "Ukraine": "Ucraina", "Japan": "Giappone", "Belgium": "Belgio", "Romania": "Romania",
    "East Germany": "Germania Est", "West Germany": "Germania Ovest", "Netherlands": "Paesi Bassi",
    "North Korea": "Corea del Nord", "Peru": "Perù", "Turkey": "Turchia", "Portugal": "Portogallo",
    "Switzerland": "Svizzera", "Latvia": "Lettonia", "Norway": "Norvegia", "Qatar": "Qatar", "Sweden": "Svezia",
    "Greece": "Grecia", "England": "Inghilterra", "Wales": "Galles", "Denmark": "Danimarca", "Austria": "Austria",
    "Chile": "Cile", "Philippines": "Filippine", "Colombia": "Colombia", "Belarus": "Bielorussia",
    "Serbia and Montenegro": "Serbia e Montenegro", "Finland": "Finlandia", "Egypt": "Egitto", "Israel": "Israele",
    "Czech Republic": "Repubblica Ceca", "Slovakia": "Slovacchia", "South Africa": "Sudafrica",
    "New Zealand": "Nuova Zelanda", "Malaysia": "Malesia", "Indonesia": "Indonesia", "Georgia": "Georgia",
    "Cyprus": "Cipro", "Estonia": "Estonia", "Luxembourg": "Lussemburgo", "Azerbaijan": "Azerbaigian",
    "Thailand": "Thailandia", "North Macedonia": "Macedonia del Nord",
}
CITTA = {"Los Angeles": "Los Angeles", "Marseille": "Marsiglia", "Rio de Janeiro": "Rio de Janeiro", "Berlin": "Berlino",
         "Gstaad": "Gstaad", "Stavanger": "Stavanger", "Rome": "Roma", "Stare Jabłonki": "Stare Jabłonki",
         "Vienna": "Vienna", "Hamburg": "Amburgo", "Adelaide": "Adelaide",
         "Austria": "Austria (Klagenfurt)", "Netherlands": "Paesi Bassi", "Mexico": "Messico"}
CLUB = {"Internazionale": "Inter"}


def sezioni():
    t = GREZZI.read_text(encoding="utf-8")
    out = {}
    for blocco in t.split("## ")[1:]:
        k, _, v = blocco.partition("\n")
        v = v.rstrip("\n")
        h = hashlib.sha256(v.encode()).hexdigest()[:16]
        assert h == HASH[k], f"sezione {k} alterata rispetto alla trascrizione verificata"
        out[k] = [r for r in v.split("\n")]
    assert set(out) == set(HASH)
    return out


def paese(s):
    s = s.strip()
    if s in PAESI:
        return PAESI[s]
    raise KeyError(f"paese non tradotto: {s!r}")


def sedi(s):
    """'Canada Mexico United States' o 'Italy / Bulgaria' -> 'Canada, Messico, Stati Uniti'."""
    s = s.replace(" / ", " ").strip()
    if s == "Pan-Europe":
        return "11 città europee"
    nomi, resto = [], s
    chiavi = sorted(PAESI, key=len, reverse=True)
    while resto:
        for c in chiavi:
            if resto == c or resto.startswith(c + " "):
                nomi.append(PAESI[c])
                resto = resto[len(c):].strip()
                break
        else:
            raise KeyError(f"sede non riconosciuta: {s!r} (resto {resto!r})")
    return ", ".join(nomi)


def punteggio(s):
    s = s.strip()
    if s.startswith("Round-robin") or "No playoffs" in s:
        return "girone"
    if s == "1–1 (a.e.t.)2–0 (replay)":
        return "1–1 d.t.s.; 2–0 ripetizione"
    m = re.match(r"^(\d+–\d+)( \(a\.e\.t\.\)| \(g\.g\.\)| \(OT\)| overtime)?(\((\d+–\d+) p\))?", s)
    assert m, s
    out = m.group(1)
    extra = m.group(2) or ""
    if "a.e.t." in extra or "OT" in extra or "overtime" in extra:
        out += " d.t.s."
    elif "g.g." in extra:
        out += " golden gol"
    if m.group(4):
        out += f" ({m.group(4)} rig.)"
    return out


def torneo(righe, citta=False):
    out = []
    for r in righe:
        if r.startswith("#"):
            continue
        a, sede, oro, ris, arg, bro = r.split("|")
        if oro.startswith("Not held"):
            continue
        bronzi = [paese(bro)] if bro in PAESI else [paese(x) for x in bro.split(" and ")]
        out.append({"anno": int(a), "sede": CITTA[sede] if citta else sedi(sede), "oro": paese(oro),
                    "ris": punteggio(ris), "argento": paese(arg), "bronzo": ", ".join(bronzi)})
    return out


def coppia(s):
    parti = []
    for p in s.split(" ; "):
        naz, nomi = p.split(": ")
        parti.append(f"{nomi} ({paese(naz)})")
    return "; ".join(parti)


def beach(righe):
    out = []
    for r in righe:
        a, sede, oro, ris, arg, bro = r.split("|")
        out.append({"anno": int(a), "sede": CITTA[sede], "oro": coppia(oro), "ris": ris, "argento": coppia(arg),
                    "bronzo": coppia(bro)})
    return out


def anno_stagione(lab):
    m = re.match(r"^(\d{4})(?:–(\d{2,4}))?", lab)
    a = int(m.group(1))
    if m.group(2):
        b = m.group(2)
        return int(b) if len(b) == 4 else (a // 100) * 100 + int(b) + (100 if int(b) < a % 100 else 0)
    return a


def club(s):
    s = re.sub(r"\s*\(\d+\)$", "", s.strip())
    return CLUB.get(s, s)


def serie_a(righe):
    out = []
    for r in righe:
        _, lab, oro, arg = r.split("|")
        if lab in ("Season", "Year") or lab == "1915–19" or lab == "1945":
            continue
        lab = lab.replace("(FIGC)", " (FIGC)").replace("(CCI)", " (CCI)")
        lab = re.sub(r"^(\d{4})–\d\d(\d\d)$", r"\1–\2", lab)  # «1999–2000» → «1999–00» (v0.7)
        riga = {"anno": anno_stagione(lab), "stag": lab, "oro": club(oro),
                "argento": "" if arg == "-" else ", ".join(club(x) for x in arg.split("/"))}
        if "/" in arg:
            riga["nota"] = "secondo posto a pari merito"
        if lab == "1944":
            riga.update(oro="Non assegnato", argento="",
                        nota="Campionato Alta Italia in tempo di guerra, vinto dallo Spezia: la FIGC gli riconosce un "
                             "titolo onorifico, non conteggiato tra gli scudetti")
        elif lab == "1926–27":
            riga.update(oro="Revocato", nota="titolo vinto sul campo dal Torino e revocato dalla FIGC")
        elif lab == "2004–05":
            riga.update(oro="Non assegnato", nota="titolo revocato alla Juventus dopo Calciopoli")
        elif lab == "2005–06":
            riga["nota"] = "titolo assegnato all'Inter d'ufficio dopo Calciopoli"
        elif lab == "1914–15":
            riga["nota"] = "torneo interrotto dalla guerra, titolo assegnato al Genoa a fine conflitto"
        out.append(riga)
    return out


def nba(righe):
    return [{"anno": int(a), "stag": f"{int(a) - 1}–{a[2:]}", "oro": vin, "ris": ris, "argento": per}
            for a, vin, per, ris, _ in (r.split("|") for r in righe)]


def volley_ita(righe):
    out = []
    for r in righe:
        lab, oro, arg = r.split("|")
        riga = {"anno": anno_stagione(lab), "stag": lab, "oro": oro, "argento": arg}
        if oro.startswith("Cancelled"):
            riga.update(oro="Non assegnato", argento="", nota="stagione interrotta per la pandemia di COVID-19")
        elif oro == "Not assigned":
            riga["oro"] = "Non assegnato"
        out.append(riga)
    return out


def wp(titolo, rev, tabella):
    return {"i": "Wikipedia", "t": f"{titolo} (revisione {rev}, tabella «{tabella}»)",
            "u": f"https://en.wikipedia.org/w/index.php?title={titolo.replace(' ', '_')}&oldid={rev}"}


def ff(ist, titolo, url):
    return {"i": ist, "t": titolo, "u": url}


def costruisci():
    S = sezioni()
    U, D = "Uomini", "Donne"
    return {
        "calcio": [
            {"id": "mondiali", "nome": "Mondiali", "tornei": [
                {"nome": U, "righe": torneo(S["calcio_mondiali_m"]),
                 "nota": "1942 e 1946 non disputati per la Seconda guerra mondiale. Nel 1930 non si giocò la finale per il terzo posto."},
                {"nome": D, "righe": torneo(S["calcio_mondiali_f"])}],
             "fonti": [wp("FIFA World Cup", 1386052828, "Results"), wp("FIFA Women's World Cup", 1385546953, "Results"),
                       ff("FIFA", "Spain complete unprecedented global double (finale 2026)",
                          "https://inside.fifa.com/organisation/media-releases/spain-unprecedented-global-double-new-milestones-historic-world-cup-2026")]},
            {"id": "europei", "nome": "Europei", "tornei": [
                {"nome": U, "righe": torneo(S["calcio_europei"]),
                 "nota": "Dal 1984 non si gioca la finale per il terzo posto: nella colonna bronzo ci sono le due semifinaliste sconfitte. "
                         "L'edizione «2020» si giocò nel 2021 in 11 città europee."}],
             "fonti": [wp("UEFA European Championship", 1384979470, "Results")]},
            {"id": "scudetto", "nome": "Scudetto", "tornei": [
                {"nome": U, "tipo": "lega", "righe": serie_a(S["calcio_seriea"]),
                 "nota": "Girone unico (Serie A) dal 1929–30. Prima il titolo si decideva con gironi regionali e finali: "
                         "nella colonna del secondo posto c'è la finalista sconfitta. Nel 1921–22 ci furono due campionati, "
                         "FIGC e CCI, entrambi riconosciuti. 1915–19 e 1945 non disputati per la guerra."}],
             "fonti": [wp("List of Italian football champions", 1371936691, "Champions"),
                       ff("Inter", "L'Inter è Campione d'Italia! Parma battuto, è lo Scudetto numero 21 (2025–26)",
                          "https://www.inter.it/it/notizie/inter-parma-serie-a-2025-2026")]},
        ],
        "basket": [
            {"id": "mondiali", "nome": "Mondiali", "tornei": [
                {"nome": U, "righe": torneo(S["basket_mondiali_m"]),
                 "nota": "Fino al 1974 il titolo si assegnava con un girone finale («girone»), senza finale secca."},
                {"nome": D, "righe": torneo(S["basket_mondiali_f"])}],
             "fonti": [wp("FIBA Basketball World Cup", 1383881599, "Summaries"),
                       wp("FIBA Women's Basketball World Cup", 1378996075, "Summaries"),
                       ff("Al Jazeera", "USA defeat France to win 12th FIBA Women's Basketball World Cup (2026)",
                          "https://www.aljazeera.com/sports/2026/9/13/usa-defeat-france-to-win-12th-fiba-womens-basketball-world-cup")]},
            {"id": "europei", "nome": "Europei", "tornei": [
                {"nome": U, "righe": torneo(S["basket_euro_m"]), "nota": "EuroBasket. 1941 annullato per la guerra."},
                {"nome": D, "righe": torneo(S["basket_euro_f"]), "nota": "EuroBasket Women. 1940 annullato per la guerra."}],
             "fonti": [wp("EuroBasket", 1375424928, "Results"), wp("EuroBasket Women", 1383589252, "Results")]},
            {"id": "nba", "nome": "NBA", "tornei": [
                {"nome": "Finali", "tipo": "lega", "righe": nba(S["basket_nba"]),
                 "nota": "Le finali 1947–1949 sono della BAA, la lega che nel 1949 diventò NBA; la NBA le conta come proprie. "
                         "Nella colonna «serie» le partite vinte dalle due finaliste."}],
             "fonti": [wp("List of NBA champions", 1387614241, "Champions"),
                       ff("NBA", "2026 NBA Finals schedule (Knicks 4-1)", "https://www.nba.com/news/2026-nba-finals-schedule")]},
        ],
        "pallavolo": [
            {"id": "mondiali", "nome": "Mondiali", "tornei": [
                {"nome": U, "righe": torneo(S["volley_mondiali_m"])}, {"nome": D, "righe": torneo(S["volley_mondiali_f"])}],
             "fonti": [wp("FIVB Men's Volleyball World Championship", 1380470993, "Results"),
                       wp("FIVB Women's Volleyball World Championship", 1380862738, "Results")]},
            {"id": "europei", "nome": "Europei", "tornei": [
                {"nome": U, "righe": torneo(S["volley_euro_m"])}, {"nome": D, "righe": torneo(S["volley_euro_f"])}],
             "fonti": [wp("Men's European Volleyball Championship", 1381071838, "Results"),
                       wp("Women's European Volleyball Championship", 1377059491, "Results"),
                       ff("CEV", "Sultans of the Net retain EuroVolley crown (2026, donne)",
                          "https://www.cev.eu/articles/volleyball/sultans-of-the-net-delight-record-crowd-to-retain-eurovolley-crown-and-qualify-for-la28/"),
                       ff("FIVB", "Poland punch ticket to LA28 with EuroVolley triumph (2026, uomini)",
                          "https://www.fivb.com/poland-punch-ticket-to-la28-with-eurovolley-triumph/")]},
            {"id": "scudetto", "nome": "Scudetto", "tornei": [
                {"nome": U, "tipo": "lega", "righe": volley_ita(S["volley_ita_m"]), "nota": "Oggi SuperLega; le squadre hanno il nome dello sponsor di quella stagione."},
                {"nome": D, "tipo": "lega", "righe": volley_ita(S["volley_ita_f"]), "nota": "Oggi Serie A1; le squadre hanno il nome dello sponsor di quella stagione."}],
             "fonti": [wp("Italian Volleyball League", 1387610588, "Champions"),
                       wp("Italian Women's Volleyball League", 1377007798, "Champions"),
                       ff("Lega Pallavolo Serie A", "Sir Susa Scai Perugia is the 2025/26 Italian Champion",
                          "https://www.legavolley.it/2026/max-colaci-game-3-mvp/?lang=en"),
                       ff("Il Post", "Conegliano ha vinto lo Scudetto femminile nella pallavolo (2026)",
                          "https://www.ilpost.it/2026/04/22/conegliano-scudetto-pallavolo-2026/")]},
        ],
        "beach": [
            {"id": "mondiali", "nome": "Mondiali", "tornei": [
                {"nome": U, "righe": beach(S["beach_mondiali_m"]),
                 "nota": "Nel 1997 la finale per il bronzo non si giocò: bronzo a entrambe le coppie sconfitte in semifinale."},
                {"nome": D, "righe": beach(S["beach_mondiali_f"]),
                 "nota": "Nel 1997 la finale per il bronzo non si giocò: bronzo a entrambe le coppie sconfitte in semifinale."}],
             "fonti": [wp("Beach Volleyball World Championships", 1360069742, "Results"),
                       ff("CEV", "Åhman/Hellvig, Graudina/Samoilova secure double global crown (2025)",
                          "https://www.cev.eu/articles/beach-volleyball/aahmanhellvig-graudinasamoilova-secure-unprecedented-double-global-crown-for-europe")]},
        ],
    }


if __name__ == "__main__":
    A = costruisci()
    for s, gg in A.items():
        for g in gg:
            for t in g["tornei"]:
                print(s, g["nome"], t["nome"], len(t["righe"]), t["righe"][0], t["righe"][-1], sep=" | ")
