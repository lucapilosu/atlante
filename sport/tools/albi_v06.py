"""Albi d'oro v0.6 (27/11/2026): tennis (finali di singolare dei quattro Slam, era Open), nuoto e ginnastica
artistica olimpici (gare principali scelte da Luca).

Fonti: tabelle di Wikipedia a revisione fissata, estratte nel browser e trascritte in sport/tools/altri/,
controllate con l'impronta SHA-256 (primi 16 caratteri) calcolata sia nel browser sia qui.
- t_*.txt: «List of ... singles champions» (en), una per torneo e genere; la revisione è nella prima riga.
- n1, n2: «List of Olympic medalists in swimming (men/women)».
- g1: «List of Olympic medalists in gymnastics (men/women)».
Le finali Slam 2026 sono state riscontrate anche su fonti giornalistiche e ufficiali (elencate tra le fonti).
"""
import hashlib
import re
from pathlib import Path

from albo_atletica import PAESI as PAESI_EN, SEDI

DIR = Path(__file__).parent / "altri"
HASH = {"t_aoM": "31b7a37353ea7103", "t_aoF": "f9e2a2a2912f032c", "t_rgM": "3dfa8ceb39d52f43",
        "t_rgF": "1bdcee6e663a942c", "t_wM": "749e899fd912b73d", "t_wF": "2706933b400178b0",
        "t_usM": "b3aa338c59243f95", "t_usF": "e5166742acc94e6d",
        "n1": "03f8d56b870bca23", "n2": "84a25ae30e44578d", "g1": "3e545f61860023d2"}

# Codici CIO usati nelle tabelle del tennis
CIO = {"ARG": "Argentina", "AUS": "Australia", "AUT": "Austria", "BEL": "Belgio", "BLR": "Bielorussia",
       "BRA": "Brasile", "CAN": "Canada", "CHI": "Cile", "CHN": "Cina", "CRO": "Croazia", "CYP": "Cipro",
       "CZE": "Repubblica Ceca", "DEN": "Danimarca", "ECU": "Ecuador", "ESP": "Spagna", "FRA": "Francia",
       "FRG": "Germania Ovest", "GBR": "Gran Bretagna", "GER": "Germania", "GRE": "Grecia", "ITA": "Italia",
       "JPN": "Giappone", "KAZ": "Kazakistan", "LAT": "Lettonia", "NED": "Paesi Bassi", "NOR": "Norvegia",
       "NZL": "Nuova Zelanda", "PAR": "Paraguay", "POL": "Polonia", "ROU": "Romania", "RSA": "Sudafrica",
       "RUS": "Russia", "SRB": "Serbia", "SUI": "Svizzera", "SVK": "Slovacchia", "SWE": "Svezia",
       "TCH": "Cecoslovacchia", "TUN": "Tunisia", "UKR": "Ucraina", "URS": "Unione Sovietica", "USA": "Stati Uniti",
       "YUG": "Jugoslavia"}
EN = dict(PAESI_EN, **{"Austria": "Austria", "Australasia": "Australasia", "Singapore": "Singapore",
                       "Zimbabwe": "Zimbabwe", "Slovakia": "Slovacchia", "Kazakhstan": "Kazakistan",
                       "Lithuania": "Lituania", "Suriname": "Suriname", "Costa Rica": "Costa Rica",
                       "Hong Kong": "Hong Kong", "Egypt": "Egitto", "Israel": "Israele", "Kyrgyzstan": "Kirghizistan",
                       "Uzbekistan": "Uzbekistan", "Philippines": "Filippine", "Ireland": "Irlanda"})

SLAM = [("ao", "Australian Open", "Australian Open"), ("rg", "Roland Garros", "French Open"),
        ("wimbledon", "Wimbledon", "Wimbledon"), ("usopen", "US Open", "US Open")]
GARE_NUOTO = [("100 metre freestyle", "100 m stile libero"), ("200 metre freestyle", "200 m stile libero"),
              ("100 metre backstroke", "100 m dorso"), ("100 metre breaststroke", "100 m rana"),
              ("100 metre butterfly", "100 m farfalla"), ("400 metre individual medley", "400 m misti"),
              ("4 × 100 metre freestyle relay", "Staffetta 4×100 stile libero"),
              ("4 × 100 metre medley relay", "Staffetta 4×100 misti")]
GARE_GINN = [("All-around, individual", "Concorso generale"), ("All-around, team", "Concorso a squadre")]
GENERI = [("M", "Uomini"), ("F", "Donne")]
NON_ASSEGNATO = {"", "none awarded"}

# Celle da sistemare: (blocco, sezione, anno, testo nella tabella) -> (testo corretto, nota)
NOTA_1904 = ("Il CIO attribuisce le medaglie del 1904 secondo il club rappresentato: Julius Lenhart, austriaco, "
             "gareggiava per un club statunitense; Adolf Spinnler, svizzero, per un club tedesco.")
CELLE = {
    ("M|All-around, individual", "1904", "Julius Lenhart AUT (United States)"): "Julius Lenhart (United States)",
    ("M|All-around, individual", "1904", "Adolf Spinnler SUI (Germany)"): "Adolf Spinnler (Germany)",
    ("M|All-around, team", "1904", "United States ; Julius Lenhart"): "United States",
}
NOTE_OLI = {("M|All-around, individual", 1904): NOTA_1904,
            ("M|All-around, team", 1904): "Nella squadra statunitense c'era anche l'austriaco Julius Lenhart."}
# Le due edizioni dell'Australian Open del 1977 (gennaio e dicembre: il torneo cambiò data)
STAG_1977 = ["1977 (gennaio)", "1977 (dicembre)"]


def leggi(k):
    t = (DIR / f"{k}.txt").read_text(encoding="utf-8").rstrip("\n")
    assert hashlib.sha256(t.encode()).hexdigest()[:16] == HASH[k], f"altri/{k}.txt alterato"
    return t


def sezioni(k):
    out = {}
    for sez in leggi(k).split("## ")[1:]:
        testa, _, corpo = sez.partition("\n")
        out[testa] = [r.split("|") for r in corpo.rstrip("\n").split("\n")]
    return out


# ---------- tennis ----------
def tennista(cod, nome, anno, neutri):
    nome = re.sub(r" \(\d+/\d*$", "", nome.strip())  # residuo di un contatore di titoli nella cella
    assert "(" not in nome, nome
    if not cod:
        assert anno >= 2022, (anno, nome)  # dal 2022 russi e bielorussi giocano senza bandiera
        neutri.append(nome)
        return nome
    return f"{nome} ({CIO[cod]})"


def slam(k):
    testa, *righe = leggi(k).split("\n")
    _, fonte, rev = testa[3:].split("|")
    out, n1977 = [], 0
    for l in righe:
        r = l.split("|")
        if len(r) == 2:
            assert r[1].startswith("No competition"), r
            continue
        assert len(r) == 6, r
        et = r[0]
        m = re.fullmatch(r"(\d{4})(?: \(([12])\))?", et)
        assert m, et
        anno, neutri = int(m[1]), []
        riga = {"anno": anno, "sede": "", "oro": tennista(r[1], r[2], anno, neutri),
                "ris": r[5].replace(" retired", " (ritiro)"), "argento": tennista(r[3], r[4], anno, neutri)}
        if anno == 1977 and k.startswith("t_ao"):
            riga["stag"] = STAG_1977[n1977]
            n1977 += 1
            riga["nota"] = "Nel 1977 il torneo si giocò due volte: a gennaio e a dicembre, data poi mantenuta fino al 1985."
        if neutri:
            riga["nota"] = "Senza bandiera nazionale: " + ", ".join(neutri) + "."
        out.append(riga)
    anni = [x["anno"] for x in out]
    assert anni == sorted(anni) and len(set(anni)) == len(anni) - (1 if k.startswith("t_ao") else 0), k
    assert not k.startswith("t_ao") or n1977 == 2, k
    return out, fonte.removeprefix("en:"), int(rev)


# ---------- nuoto e ginnastica ----------
def persona(s, squadra):
    s = s.strip()
    if squadra:
        return EN[s]
    m = re.fullmatch(r"(.+) \(([^()]+)\)", s)
    assert m, f"atleta senza paese: {s!r}"
    if m[2] not in EN:
        raise KeyError(f"paese non tradotto: {m[2]!r}")
    return f"{m[1]} ({EN[m[2]]})"


def olimpici(blocchi, gare, sezione_chiave):
    tornei = []
    for g, gen in GENERI:
        for e, it in gare:
            sez = f"{g}|{e}"
            squadra = "relay" in e or "team" in e
            per_anno = {}
            for r in blocchi[sez]:
                assert len(r) == 4, r
                anno = int(r[0])
                pos = per_anno.setdefault(anno, [[], [], []])
                for i, x in enumerate(r[1:]):
                    x = CELLE.get((sez, r[0], x), x)
                    if x.strip().lower() in NON_ASSEGNATO:
                        continue
                    for p in x.split(" ; "):
                        p = persona(p, squadra)
                        if p not in pos[i]:
                            pos[i].append(p)
            righe = []
            for anno in sorted(per_anno):
                oro, arg, bro = per_anno[anno]
                note = ["oro ex aequo"] if len(oro) > 1 else []
                if not arg and not bro:
                    note.append("argento e bronzo non assegnati")
                else:
                    note += ["argento non assegnato"] if not arg else ["argento ex aequo"] if len(arg) > 1 else []
                    note += ["bronzo non assegnato"] if not bro else ["bronzo ex aequo"] if len(bro) > 1 else []
                testo = "; ".join(note)
                testo = testo[:1].upper() + testo[1:] + "." if testo else ""
                if (sez, anno) in NOTE_OLI:
                    testo = (NOTE_OLI[(sez, anno)] + " " + testo).strip()
                assert oro, (sez, anno)
                riga = {"anno": anno, "sede": SEDI[anno], "oro": ", ".join(oro), "ris": "",
                        "argento": ", ".join(arg) or "—", "bronzo": ", ".join(bro) or "—"}
                if testo:
                    riga["nota"] = testo
                righe.append(riga)
            tornei.append({"nome": it, "genere": gen, "tipo": "torneo", "righe": righe})
    return tornei


W = "https://en.wikipedia.org/w/index.php?title={}&oldid={}"


def fonte(ist, t, u):
    return {"i": ist, "t": t, "u": u}


def wp(titolo, rev):
    return fonte("Wikipedia", f"{titolo} (revisione {rev})", W.format(titolo.replace(" ", "_"), rev))


GIORNALI = {
    "ao": [fonte("Australian Open", "Rybakina's recipe: how the AO 2026 women's final was won", "https://ausopen.com/node/261766"),
           fonte("ATP Tour / TSN", "Alcaraz batte Djokovic 2-6 6-2 6-3 7-5 (1° febbraio 2026)", "https://www.tsn.ca/tennis/article/alcaraz-beats-djokovic-in-australian-open-final-becomes-youngest-man-to-complete-career-grand-slam/")],
    "rg": [fonte("ATP Tour", "Zverev wins first major title at Roland Garros (7 giugno 2026)", "https://www.atptour.com/en/news/zverev-cobolli-roland-garros-2026-final-report"),
           fonte("Roland-Garros", "Andreeva lives teenage dream with maiden Grand Slam title (6 giugno 2026)", "https://www.rolandgarros.com/en-us/article/2026-edition-final-andreeva-chwalinska")],
    "wimbledon": [fonte("ATP Tour", "Sinner successfully defends Wimbledon crown, defeats Zverev (12 luglio 2026)", "https://www.atptour.com/en/news/sinner-zverev-wimbledon-2026-final-sunday"),
                  fonte("WTA", "At 21, Noskova becomes youngest Wimbledon champion in 15 years (11 luglio 2026)", "https://www.wtatennis.com/news/4533700/at-21-linda-noskova-caps-brilliant-fortnight-to-become-youngest-wimbledon-champion-in-15-years-defeats-karolina-muchova")],
    "usopen": [fonte("ATP Tour", "Zverev doubles up in 2026, stymies Shelton for US Open title (13 settembre 2026)", "https://www.atptour.com/en/news/zverev-shelton-us-open-2026-final-report"),
               fonte("WTA", "Rybakina ends Sabalenka's reign at the US Open (12 settembre 2026)", "https://www.wtatennis.com/news/4575707/rybakina-halts-sabalenkas-three-peat-bid-to-capture-first-us-open-title")],
}
NOTE_SLAM = {
    "ao": "Finali di singolare dell'era Open, dal 1969 (il torneo si aprì ai professionisti un anno dopo gli altri). "
          "Nel 1986 non si giocò, per lo spostamento da dicembre a gennaio.",
    "rg": "Finali di singolare dell'era Open, dal 1968.",
    "wimbledon": "Finali di singolare dell'era Open, dal 1968. Nel 2020 il torneo fu annullato per la pandemia.",
    "usopen": "Finali di singolare dell'era Open, dal 1968.",
}


def costruisci():
    tennis = []
    for gid, nome, _ in SLAM:
        k = {"ao": "ao", "rg": "rg", "wimbledon": "w", "usopen": "us"}[gid]
        (rm, fm, rvm), (rf, ff, rvf) = slam(f"t_{k}M"), slam(f"t_{k}F")
        col = ["Campione", "Finalista"]
        tennis.append({"id": gid, "nome": nome, "nota_gruppo": NOTE_SLAM[gid],
                       "fonti": [wp(fm, rvm), wp(ff, rvf)] + GIORNALI[gid],
                       "tornei": [{"nome": "Uomini", "tipo": "torneo", "colonne": col, "righe": rm},
                                  {"nome": "Donne", "tipo": "torneo", "colonne": col, "righe": rf}]})
    N = {**sezioni("n1"), **sezioni("n2")}
    G = sezioni("g1")
    assert set(N) == {f"{g}|{e}" for g, _ in GENERI for e, _ in GARE_NUOTO}, set(N)
    assert set(G) == {f"{g}|{e}" for g, _ in GENERI for e, _ in GARE_GINN}, set(G)
    rev = lambda k: leggi(k).split("\n")[0].split("|")
    _, tn_m, rn_m, tn_f, rn_f = rev("n1")
    _, tg_m, rg_m, tg_f, rg_f = rev("g1")
    nuoto = {"tornei": olimpici(N, GARE_NUOTO, "n"),
             "fonti": [wp(tn_m.removeprefix("en:"), rn_m), wp(tn_f, rn_f)]}
    ginn = {"tornei": olimpici(G, GARE_GINN, "g"),
            "fonti": [wp(tg_m.removeprefix("en:"), rg_m), wp(tg_f, rg_f)]}
    return tennis, nuoto, ginn


if __name__ == "__main__":
    t, n, g = costruisci()
    print(sum(len(x["righe"]) for gr in t for x in gr["tornei"]), "righe tennis;",
          sum(len(x["righe"]) for x in n["tornei"]), "nuoto;", sum(len(x["righe"]) for x in g["tornei"]), "ginnastica")
