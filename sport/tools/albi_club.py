"""Albi d'oro dei club (v0.7, 27/11/2026): Coppa dei Campioni / Champions League e Coppa Italia di calcio,
Eurolega di basket (uomini e donne), Champions League di pallavolo (uomini e donne).

Fonti: tabelle di en.wikipedia a revisione fissata, estratte nel browser e trascritte in sport/tools/altri/s_*.txt,
controllate con l'impronta SHA-256 (primi 16 caratteri) calcolata sia nel browser sia qui. Le righe dei file sono
la tabella «compattata» nel browser: celle unite sciolte, note a piè di pagina tolte, bandierina del club scritta
come «Paese~», finali di andata e ritorno della Coppa Italia riunite in una riga (punteggi separati da « ; »).
"""
import hashlib
import re
from pathlib import Path

from albi_v06 import EN as EN_BASE

DIR = Path(__file__).parent / "altri"
HASH = {"s_ucl": "0236efbe2a0cfe68", "s_ci": "fb959ef618b5b951", "s_el": "1f3c1c918e8f2921",
        "s_ew": "d0d560151e1afb2f", "s_cm": "27a14e53dd43a65f", "s_cw": "c68023e98d871c30"}

PAESE = dict(EN_BASE, **{
    "Spain": "Spagna", "France": "Francia", "Italy": "Italia", "Germany": "Germania", "West Germany": "Germania Ovest",
    "East Germany": "Germania Est", "England": "Inghilterra", "Scotland": "Scozia", "Wales": "Galles",
    "Netherlands": "Paesi Bassi", "Portugal": "Portogallo", "Belgium": "Belgio", "Greece": "Grecia", "Turkey": "Turchia",
    "Romania": "Romania", "Bulgaria": "Bulgaria", "Poland": "Polonia", "Hungary": "Ungheria", "Sweden": "Svezia",
    "Russia": "Russia", "Soviet Union": "Unione Sovietica", "Czechoslovakia": "Cecoslovacchia",
    "Czech Republic": "Repubblica Ceca", "Slovakia": "Slovacchia", "Croatia": "Croazia", "Lithuania": "Lituania",
    "Israel": "Israele", "Azerbaijan": "Azerbaigian", "Ukraine": "Ucraina", "Switzerland": "Svizzera", "Austria": "Austria",
    "Yugoslavia": "Jugoslavia", "Socialist Federal Republic of Yugoslavia": "Jugoslavia", "SFR Yugoslavia": "Jugoslavia",
    "Commonwealth of Independent States": "Comunità degli Stati Indipendenti", "Hungary ": "Ungheria"})

# Città delle finali (nome italiano)
CITTA = {"Paris": "Parigi", "Madrid": "Madrid", "Brussels": "Bruxelles", "Stuttgart": "Stoccarda", "Glasgow": "Glasgow",
         "Bern": "Berna", "Amsterdam": "Amsterdam", "London": "Londra", "Vienna": "Vienna", "Milan": "Milano",
         "Lisbon": "Lisbona", "Rotterdam": "Rotterdam", "Belgrade": "Belgrado", "Rome": "Roma",
         "Munich": "Monaco di Baviera", "Athens": "Atene", "Seville": "Siviglia", "Barcelona": "Barcellona", "Bari": "Bari",
         "Saint-Denis": "Saint-Denis", "Manchester": "Manchester", "Gelsenkirchen": "Gelsenkirchen", "Istanbul": "Istanbul",
         "Moscow": "Mosca", "Berlin": "Berlino", "Cardiff": "Cardiff", "Kyiv": "Kiev", "Porto": "Porto", "Budapest": "Budapest",
         "Vado Ligure": "Vado Ligure", "Genoa": "Genova", "Florence": "Firenze", "Turin": "Torino",
         "Venice": "Venezia", "Naples": "Napoli", "Bergamo": "Bergamo", "Verona": "Verona", "Parma": "Parma",
         "Ancona": "Ancona", "Vicenza": "Vicenza", "Reggio Emilia": "Reggio Emilia"}
# Nomi dei club di calcio come si dicono in italiano
CLUB = {"Inter Milan": "Inter", "AC Milan": "Milan", "Bayern Munich": "Bayern Monaco", "Red Star Belgrade": "Stella Rossa",
        "Eintracht Frankfurt": "Eintracht Francoforte", "Barcelona": "Barcellona", "Hamburger SV": "Amburgo",
        "Marseille": "Olympique Marsiglia", "Malmö FF": "Malmö", "Steaua București": "Steaua Bucarest",
        "Partizan": "Partizan Belgrado", "Monaco": "AS Monaco", "Club Brugge": "Club Brugge"}

SEGNI = {"†": " d.t.s.", "*": " (rigori)"}


def leggi(k):
    t = (DIR / f"{k}.txt").read_text(encoding="utf-8").rstrip("\n")
    assert hashlib.sha256(t.encode()).hexdigest()[:16] == HASH[k], f"altri/{k}.txt alterato"
    testa, *righe = t.split("\n")
    _, fonte, rev = testa[3:].split("|")
    return [r.split("|") for r in righe], fonte.removeprefix("en:"), int(rev)


def stagione(s):
    """«1999–2000» -> «1999–00»; anno = anno di fine stagione (come negli altri albi)."""
    m = re.fullmatch(r"(\d{4})–(\d{2}|\d{4})", s)
    if m:
        fine = m[2][-2:]
        return f"{m[1]}–{fine}", int(m[1]) + 1
    assert re.fullmatch(r"\d{4}", s), s
    return s, int(s)


def club_paese(cella, calcio=False):
    paese, _, nome = cella.partition("~")
    assert nome, cella
    nome = CLUB.get(nome, nome) if calcio else re.sub(r"\bMoscow\b(?! Region)", "Mosca", nome)
    return f"{nome} ({PAESE[paese]})"


def punteggio(s):
    s = s.strip()
    for k, v in SEGNI.items():
        if s.endswith(k):
            return s[:-1] + v
    return s


def citta(sede):
    parti = [p.strip() for p in sede.split(",")]
    c = parti[-2] if len(parti) >= 3 else parti[-1]
    return CITTA[c]


ANNULLATA = "Edizione annullata per la pandemia di COVID-19."


def riga_annullata(lab):
    st, anno = stagione(lab)
    return {"anno": anno, "stag": st, "oro": "Non assegnata", "ris": "", "argento": "", "nota": ANNULLATA}


# ---------- Coppa dei Campioni / Champions League ----------
def champions_calcio():
    righe, fonte, rev = leggi("s_ucl")
    out = []
    for lab, pv, v, ris, f, pf, sede in righe:
        st, anno = stagione(lab)
        if ris.endswith("&"):  # finale ripetuta: la riga prima è la prima partita
            prima = out.pop()
            assert prima["stag"] == st
            r = {**prima, "ris": f"{prima['ris']}; {ris[:-1]}",
                 "nota": f"Finale ripetuta: la prima partita era finita {prima['ris']}, la ripetizione {ris[:-1]}."}
            out.append(r)
            continue
        out.append({"anno": anno, "stag": st, "sede": citta(sede), "oro": club_paese(f"{pv}~{v}", True),
                    "ris": punteggio(ris), "argento": club_paese(f"{pf}~{f}", True)})
    return out, fonte, rev


# ---------- Coppa Italia ----------
NON_DISPUTATA = {"1923–1925", "1928–1935", "1944–1957"}


def coppa_italia():
    righe, fonte, rev = leggi("s_ci")
    out = []
    for lab, v, ris, f, sede, agg in righe:
        if lab in NON_DISPUTATA:
            assert v == "Not held"
            continue
        st, anno = stagione(lab)
        if v == "Not concluded":
            out.append({"anno": anno, "stag": st, "oro": "Non assegnata", "ris": "", "argento": "",
                        "nota": "Edizione non conclusa."})
            continue
        v, f = re.sub(r" [‡#]$", "", v), f
        riga = {"anno": anno, "stag": st, "oro": CLUB.get(v, v), "argento": CLUB.get(f, f),
                "ris": ", ".join(punteggio(x) for x in ris.split(" ; ")) if ris else ""}
        if sede:
            riga["sede"] = citta(sede)
        if " ; " in ris:
            m = re.search(r"(\d+–\d+) on aggregate", agg)
            assert m, agg
            if "away goals" in agg:
                riga["nota"] = f"Andata e ritorno, {m[1]} nel totale: decisero i gol in trasferta."
            elif "penalties" in agg:
                rig = re.search(r"won (\d+–\d+) on penalties", agg)[1]
                riga["nota"] = f"Andata e ritorno, {m[1]} nel totale: decisero i rigori ({rig})."
            else:
                riga["nota"] = f"Andata e ritorno, {m[1]} nel totale."
        elif ris.endswith("&"):
            riga["ris"] = ris[:-1]
            riga["nota"] = "Vinta nella ripetizione della finale."
        elif not ris:
            assert 1968 <= anno <= 1971, lab
            riga["nota"] = "Assegnata con un girone finale, senza finale."
        out.append(riga)
    return out, fonte, rev


# ---------- Eurolega ----------
def serie(s):
    """«*86–81 / 84–*71» -> «86–81, 84–71» (l'asterisco segna la squadra di casa); OT = supplementari."""
    gare = [g.replace("*", "").strip() for g in s.split(" / ")]
    gare = [re.sub(r" \((\d?)OT\)", lambda m: f" ({m[1] or '1'} suppl.)", g) for g in gare]
    return ", ".join(gare), len(gare)


def eurolega():
    righe, fonte, rev = leggi("s_el")
    out, n2001 = [], 0
    for lab, _sede, v, f, ris in righe:
        if v.startswith("Cancelled"):
            out.append(riga_annullata(lab))
            continue
        if lab.startswith("2000–01 *"):
            # due competizioni nello stesso anno: Suproleague FIBA (prima riga, Parigi) ed Euroleague ULEB
            lab, n2001 = "2000–01", n2001 + 1
        st, anno = stagione(lab)
        if lab == "1958":
            st = "1957–58"
        p, n = serie(ris)
        r = {"anno": anno, "stag": st, "oro": club_paese(v), "ris": p, "argento": club_paese(f)}
        if n > 1:
            r["nota"] = f"Finale in {n} partite."
        if lab == "2000–01":
            if n2001 == 1:
                r.update(stag="2000–01 (Suproleague)", parallela=True,
                         nota="Stagione divisa: la Suproleague della FIBA si giocò accanto all'Euroleague dei club (ULEB), "
                              "da cui discende l'Eurolega di oggi.")
            else:
                r.update(stag="2000–01 (Euroleague)", nota="Euroleague dei club (ULEB). " + r.get("nota", ""))
                r["nota"] = r["nota"].strip()
        out.append(r)
    assert n2001 == 2
    return out, fonte, rev


def eurolega_donne():
    righe, fonte, rev = leggi("s_ew")
    out = []
    for lab, v, ris, f in righe:
        if v.startswith("Curtailed"):
            out.append(riga_annullata(lab))
            continue
        st, anno = stagione(lab)
        m = re.fullmatch(r"(\d+–\d+) (\d+–\d+) / (\d+–\d+)", ris)
        r = {"anno": anno, "stag": st, "oro": club_paese(v), "argento": club_paese(f),
             "ris": f"{m[2]}, {m[3]}" if m else ris}
        if m:
            r["nota"] = f"Andata e ritorno, {m[1]} nel totale."
        else:
            assert re.fullmatch(r"\d+–\d+", ris), ris
        out.append(r)
    return out, fonte, rev


# ---------- Champions League di pallavolo ----------
def cev(k):
    righe, fonte, rev = leggi(k)
    out = []
    for lab, v, ris, f in righe:
        if v.startswith("Cancelled"):
            out.append(riga_annullata(lab))
            continue
        st, anno = stagione(lab)
        r = {"anno": anno, "stag": st, "oro": club_paese(v), "argento": club_paese(f), "ris": ""}
        m = re.fullmatch(r"(\d–\d) (\d–\d)won (\d–\d) on aggregate", ris)
        if ris == "Group Stage":
            r["nota"] = "Titolo assegnato in un girone finale."
        elif m:
            r["ris"] = f"{m[1]}, {m[2]}"
            r["nota"] = f"Andata e ritorno, {m[3]} nei set vinti."
        elif ris:
            assert re.fullmatch(r"\d–\d(, \d–\d)*", ris), ris
            r["ris"] = ris
            if "," in ris:
                r["nota"] = f"Finale in {ris.count(',') + 1} partite."
        out.append(r)
    return out, fonte, rev


W = "https://en.wikipedia.org/w/index.php?title={}&oldid={}"


def wp(titolo, rev):
    return {"i": "Wikipedia", "t": f"{titolo} (revisione {rev})", "u": W.format(titolo.replace(" ", "_"), rev)}


def torneo(nome, righe, colonne=("Vincitore", "Finalista"), nota=None, bandiere=True):
    t = {"nome": nome, "tipo": "lega", "colonne": list(colonne), "ris_nome": "Finale", "righe": righe}
    if bandiere:
        t["bandiere"] = True
    if nota:
        t["nota"] = nota
    return t


def costruisci(fonti_extra):
    """Restituisce {sport: [gruppi]}; fonti_extra: {gid: [fonti]} con i riscontri della stagione 2025-26."""
    ucl, f1, r1 = champions_calcio()
    ci, f2, r2 = coppa_italia()
    el, f3, r3 = eurolega()
    ew, f4, r4 = eurolega_donne()
    cm, f5, r5 = cev("s_cm")
    cw, f6, r6 = cev("s_cw")
    return {
        "calcio": [
            {"id": "champions", "nome": "Champions League", "fonti": [wp(f1, r1)] + fonti_extra["champions"],
             "nota_gruppo": "Finali della Coppa dei Campioni (1955–1992) e della Champions League (dal 1992-93), "
                            "con la città della finale. «d.t.s.» = dopo i tempi supplementari.",
             "tornei": [torneo("Finali", ucl)]},
            {"id": "coppaitalia", "nome": "Coppa Italia", "fonti": [wp(f2, r2)] + fonti_extra["coppaitalia"],
             "nota_gruppo": "Finali dal 1922. Non disputata nel 1923–1925, nel 1928–1935 e nel 1944–1957; l'edizione 1926-27 "
                            "non fu conclusa. Dal 1967-68 al 1970-71 un girone finale al posto della finale; andata e ritorno "
                            "nel 1937-38, 1940-41, 1941-42 e dal 1980-81 al 2006-07. «d.t.s.» = dopo i tempi supplementari.",
             "tornei": [torneo("Finali", ci, bandiere=False)]}],
        "basket": [
            {"id": "eurolega", "nome": "Eurolega", "fonti": [wp(f3, r3), wp(f4, r4)] + fonti_extra["eurolega"],
             "nota_gruppo": "Finali della Coppa dei Campioni e dell'Eurolega, uomini dal 1958 e donne dal 1959. "
                            "Le squadre hanno il nome dello sponsor di quella stagione.",
             "tornei": [torneo("Uomini", el), torneo("Donne", ew)]}],
        "pallavolo": [
            {"id": "champions", "nome": "Champions League", "fonti": [wp(f5, r5), wp(f6, r6)] + fonti_extra["champions_volley"],
             "nota_gruppo": "Finali della Coppa dei Campioni e della CEV Champions League, uomini dal 1959-60 e donne dal "
                            "1960-61. Le squadre hanno il nome dello sponsor di quella stagione.",
             "tornei": [torneo("Uomini", cm),
                        torneo("Donne", cw, nota="Per le edizioni dal 1971-72 al 1989-90 la fonte non riporta il "
                                                 "punteggio della finale.")]}],
    }


if __name__ == "__main__":
    vuoto = {"champions": [], "coppaitalia": [], "eurolega": [], "champions_volley": []}
    for sp, gg in costruisci(vuoto).items():
        for g in gg:
            for t in g["tornei"]:
                print(sp, g["id"], t["nome"], len(t["righe"]), t["righe"][0]["stag"], "→", t["righe"][-1]["stag"])
