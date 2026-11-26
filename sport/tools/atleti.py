"""Atleti e palmarès del Pilu Sports Almanac (v0.3).

Fonte: infobox di en.wikipedia (medagliere: Olimpiadi, Mondiali, Europei, Copa América; titoli NBA; Slam di tennis;
Grandi Giri; titoli mondiali di F1/moto; Coppe del Mondo di sci) e sezione «Palmarès» di it.wikipedia (campionati
nazionali e Champions League vinti). Estratti nel browser il 26/11/2026, revisioni fissate in ogni record, trascritti
in atleti/b0..b5.txt e controllati blocco per blocco con l'impronta SHA-256 calcolata nel browser.
"""
import hashlib
import re
from pathlib import Path

DIR = Path(__file__).with_name("atleti")
HASH = {"b0": "c1fa7e206be848c1", "b1": "4a36fb63c2029d60", "b2": "0040af2a4421cfdc",
        "b3": "578f70bc1b2846f1", "b4": "4900dc3e8210a83d", "b5": "2d394637922aaaa1"}

# id, nome mostrato, paese, sport principale, altri nomi per la ricerca
META = """
usain-bolt|Usain Bolt|Giamaica|atletica|
carl-lewis|Carl Lewis|Stati Uniti|atletica|
jesse-owens|Jesse Owens|Stati Uniti|atletica|
emil-zatopek|Emil Zátopek|Cecoslovacchia|atletica|Zatopek
abebe-bikila|Abebe Bikila|Etiopia|atletica|
sergey-bubka|Sergej Bubka|Unione Sovietica, poi Ucraina|atletica|Sergey Bubka
armand-duplantis|Armand Duplantis|Svezia|atletica|Mondo Duplantis
eliud-kipchoge|Eliud Kipchoge|Kenya|atletica|
shelly-ann-fraser-pryce|Shelly-Ann Fraser-Pryce|Giamaica|atletica|
allyson-felix|Allyson Felix|Stati Uniti|atletica|
sara-simeoni|Sara Simeoni|Italia|atletica|
pietro-mennea|Pietro Mennea|Italia|atletica|
gianmarco-tamberi|Gianmarco Tamberi|Italia|atletica|Gimbo
michael-phelps|Michael Phelps|Stati Uniti|nuoto|
mark-spitz|Mark Spitz|Stati Uniti|nuoto|
katie-ledecky|Katie Ledecky|Stati Uniti|nuoto|
ian-thorpe|Ian Thorpe|Australia|nuoto|
federica-pellegrini|Federica Pellegrini|Italia|nuoto|
leon-marchand|Léon Marchand|Francia|nuoto|
jury-chechi|Jury Chechi|Italia|ginnastica|Yuri Chechi
nadia-comaneci|Nadia Comăneci|Romania|ginnastica|Comaneci
simone-biles|Simone Biles|Stati Uniti|ginnastica|
larisa-latynina|Larisa Latynina|Unione Sovietica|ginnastica|
kohei-uchimura|Kōhei Uchimura|Giappone|ginnastica|Kohei Uchimura
lebron-james|LeBron James|Stati Uniti|basket|
michael-jordan|Michael Jordan|Stati Uniti|basket|
kareem-abdul-jabbar|Kareem Abdul-Jabbar|Stati Uniti|basket|
bill-russell|Bill Russell|Stati Uniti|basket|
magic-johnson|Magic Johnson|Stati Uniti|basket|
kobe-bryant|Kobe Bryant|Stati Uniti|basket|
stephen-curry|Stephen Curry|Stati Uniti|basket|
nikola-jokic|Nikola Jokić|Serbia|basket|Jokic
diana-taurasi|Diana Taurasi|Stati Uniti|basket|
dino-meneghin|Dino Meneghin|Italia|basket|
arvydas-sabonis|Arvydas Sabonis|Unione Sovietica, poi Lituania|basket|
manu-ginobili|Manu Ginóbili|Argentina|basket|Ginobili
karch-kiraly|Karch Kiraly|Stati Uniti|pallavolo|
giba|Giba|Brasile|pallavolo|Gilberto Godoy Filho
lorenzo-bernardi|Lorenzo Bernardi|Italia|pallavolo|
andrea-giani|Andrea Giani|Italia|pallavolo|
ivan-zaytsev|Ivan Zaytsev|Italia|pallavolo|Zaytsev Zaitsev
simone-giannelli|Simone Giannelli|Italia|pallavolo|
earvin-ngapeth|Earvin N'Gapeth|Francia|pallavolo|Ngapeth
wilfredo-leon|Wilfredo León|Cuba, poi Polonia|pallavolo|Leon
bartosz-kurek|Bartosz Kurek|Polonia|pallavolo|
paola-egonu|Paola Egonu|Italia|pallavolo|
francesca-piccinini|Francesca Piccinini|Italia|pallavolo|
monica-de-gennaro|Monica De Gennaro|Italia|pallavolo|Moki
tijana-boskovic|Tijana Bošković|Serbia|pallavolo|Boskovic
zhu-ting|Zhu Ting|Cina|pallavolo|
kim-yeon-koung|Kim Yeon-koung|Corea del Sud|pallavolo|
regla-torres|Regla Torres|Cuba|pallavolo|
lang-ping|Lang Ping|Cina|pallavolo|
kerri-walsh-jennings|Kerri Walsh Jennings|Stati Uniti|beach|
misty-may-treanor|Misty May-Treanor|Stati Uniti|beach|
phil-dalhausser|Phil Dalhausser|Stati Uniti|beach|
emanuel-rego|Emanuel Rego|Brasile|beach|
ricardo-santos|Ricardo Santos|Brasile|beach|
anders-mol|Anders Mol|Norvegia|beach|
david-ahman|David Åhman|Svezia|beach|Ahman
laura-ludwig|Laura Ludwig|Germania|beach|
paolo-nicolai|Paolo Nicolai|Italia|beach|
daniele-lupo|Daniele Lupo|Italia|beach|
marta-menegatti|Marta Menegatti|Italia|beach|
ana-patricia|Ana Patrícia Ramos|Brasile|beach|Ana Patricia
duda-lisboa|Duda Lisboa|Brasile|beach|Eduarda Santos Lisboa
pele|Pelé|Brasile|calcio|Pele Edson Arantes do Nascimento
diego-maradona|Diego Armando Maradona|Argentina|calcio|
lionel-messi|Lionel Messi|Argentina|calcio|Leo Messi
cristiano-ronaldo|Cristiano Ronaldo|Portogallo|calcio|CR7
zinedine-zidane|Zinédine Zidane|Francia|calcio|Zidane
johan-cruyff|Johan Cruijff|Paesi Bassi|calcio|Cruyff
franz-beckenbauer|Franz Beckenbauer|Germania Ovest|calcio|
paolo-maldini|Paolo Maldini|Italia|calcio|
marta|Marta|Brasile|calcio|Marta Vieira da Silva
gianluigi-buffon|Gianluigi Buffon|Italia|calcio|Gigi Buffon
roger-federer|Roger Federer|Svizzera|tennis|
rafael-nadal|Rafael Nadal|Spagna|tennis|Rafa
novak-djokovic|Novak Đoković|Serbia|tennis|Djokovic Nole
serena-williams|Serena Williams|Stati Uniti|tennis|
steffi-graf|Steffi Graf|Germania|tennis|
rod-laver|Rod Laver|Australia|tennis|
jannik-sinner|Jannik Sinner|Italia|tennis|
eddy-merckx|Eddy Merckx|Belgio|ciclismo|
fausto-coppi|Fausto Coppi|Italia|ciclismo|
marco-pantani|Marco Pantani|Italia|ciclismo|
tadej-pogacar|Tadej Pogačar|Slovenia|ciclismo|Pogacar
bernard-hinault|Bernard Hinault|Francia|ciclismo|
ayrton-senna|Ayrton Senna|Brasile|motori|
michael-schumacher|Michael Schumacher|Germania|motori|
lewis-hamilton|Lewis Hamilton|Regno Unito|motori|
juan-manuel-fangio|Juan Manuel Fangio|Argentina|motori|
valentino-rossi|Valentino Rossi|Italia|motori|
giacomo-agostini|Giacomo Agostini|Italia|motori|
ingemar-stenmark|Ingemar Stenmark|Svezia|sci|
mikaela-shiffrin|Mikaela Shiffrin|Stati Uniti|sci|
lindsey-vonn|Lindsey Vonn|Stati Uniti|sci|
alberto-tomba|Alberto Tomba|Italia|sci|
marcel-hirscher|Marcel Hirscher|Austria|sci|
federica-brignone|Federica Brignone|Italia|sci|
"""
# ordine dei record nei blocchi = ordine di META
NOTE = {
    "karch-kiraly": ("Da ottobre 2024 è il commissario tecnico della nazionale maschile degli Stati Uniti; dal 2012 al 2024 "
                     "aveva allenato quella femminile.",
                     {"i": "USA Volleyball", "t": "Karch Kiraly to Coach U.S. Men's National Team (24 ottobre 2024)",
                      "u": "https://usavolleyball.org/story/karch-kiraly-to-coach-u-s-mens-national-team/"}),
}
COMP = {"O": "Olimpiadi", "W": "Mondiali", "E": "Europei", "A": "Copa América"}
MED = {"G": "oro", "S": "argento", "B": "bronzo"}
SLAM = {"Australian Open": "Australian Open", "French Open": "Roland Garros", "Wimbledon": "Wimbledon", "US Open": "US Open"}
LEGHE = {"UEFA Champions League": "Coppa dei Campioni / Champions League", "Coppa dei Campioni": "Coppa dei Campioni / Champions League",
         "CEV Champions League": "Champions League (pallavolo)", "Campeonato Brasileiro Série A": "Campionato brasiliano"}
EVENTI = [(r"4 ?[×x] ?100 m relay|4 × 100 m$", "staffetta 4×100"), (r"4 ?[×x] ?400 m relay|4 × 400 m$", "staffetta 4×400"),
          (r"4 × 400 m mixed", "staffetta 4×400 mista"),
          (r"Long jump", "salto in lungo"), (r"High [Jj]ump", "salto in alto"), (r"Pole vault", "salto con l'asta"),
          (r"Marathon", "maratona"), (r"10,000 m", "10.000 m"),
          (r"4 ?[×x] ?(\d+) m (free|freestyle)$", r"staffetta 4×\1 stile libero"), (r"4 ?[×x] ?(\d+) m medley$", r"staffetta 4×\1 misti"),
          (r"4 × 100 m mixed freestyle", "staffetta 4×100 mista stile libero"), (r"4 × 100 m mixed medley", "staffetta 4×100 misti mista"),
          (r"4 × 200 m mixed freestyle", "staffetta 4×200 mista stile libero"),
          (r"(\d+) m freestyle", r"\1 m stile libero"), (r"(\d+) m butterfly", r"\1 m farfalla"),
          (r"(\d+) m breaststroke", r"\1 m rana"), (r"(\d+) m medley", r"\1 m misti"),
          (r"^All-[Aa]round$", "concorso generale"), (r"^Rings$", "anelli"), (r"^Floor( [Ee]xercise)?$", "corpo libero"),
          (r"^Vault$", "volteggio"), (r"^Uneven [Bb]ars$", "parallele asimmetriche"), (r"^Balance [Bb]eam$", "trave"),
          (r"^Parallel [Bb]ars$", "parallele"), (r"^Horizontal [Bb]ar$", "sbarra"), (r"^Team, apparatus$", "squadre, attrezzi"),
          (r"^Giant slalom$", "slalom gigante"), (r"^Downhill$", "discesa libera"), (r"^Combined$", "combinata"),
          (r"^Team combined$", "combinata a squadre"), (r"^Team event$", "gara a squadre"),
          (r"^Amateurs' road race$", "corsa in linea dilettanti"), (r"^Professional road race$", "corsa in linea professionisti"),
          (r"^Road race$", "corsa in linea"), (r"^Individual pursuit$", "inseguimento individuale"),
          (r"^Singles$", "singolare"), (r"^Doubles$", "doppio"),
          (r"^(Team|Team competition|Indoor|Beach|Men's basketball|Women's|Under-18)$", "")]
SPORT_X = [("beach volleyball", "beach"), ("volleyball", "pallavolo"), ("basketball", "basket"), ("athletics", "atletica"),
           ("swimming", "nuoto"), ("gymnastics", "ginnastica"), ("football", "calcio"), ("tennis", "tennis"),
           ("cycling", "ciclismo"), ("bicycle", "ciclismo"), ("skiing", "sci")]
# correzioni puntuali, scritte qui perché si vedano (vedi note_fonti.md)
ALLENATORE_MEDAGLIE = {("franz-beckenbauer", "W", 1986), ("franz-beckenbauer", "W", 1990), ("franz-beckenbauer", "E", 1988)}
ALLENATORE_LEGHE = {("johan-cruyff", 1), ("franz-beckenbauer", 1), ("zinedine-zidane", 1), ("lorenzo-bernardi", 1),
                    ("lorenzo-bernardi", "Campionato turco")}


def evento(s):
    s = s.strip()
    for a, b in EVENTI:
        s2 = re.sub(a, b, s)
        if s2 != s:
            return s2.strip()
    return s


def anni(testo):
    """'1991–1993, 1996' -> [(1991,'1991'),...]; '2012-13' -> (2013,'2012-13'); 'Metropolitano 1981' -> 1981."""
    out = []
    for m in re.finditer(r"(\d{4})(?:[-–](\d{2,4}))?", testo):
        a, b = m.group(1), m.group(2)
        if b and len(b) == 4 and int(b) - int(a) > 1 and not re.search(r"-\d{4}", m.group(0)) is None and False:
            pass
        if b is None:
            out.append((int(a), a))
        elif len(b) == 2 or (len(b) == 4 and int(b) == int(a) + 1):
            fine = int(b) if len(b) == 4 else (int(a) // 100) * 100 + int(b) + (100 if int(b) < int(a) % 100 else 0)
            out.append((fine, f"{a}-{str(fine)[2:]}"))
        else:  # intervallo di anni interi: 1959–1966
            out.extend((y, str(y)) for y in range(int(a), int(b) + 1))
    return out


def leggi():
    recs = []
    for k, h in HASH.items():
        t = (DIR / f"{k}.txt").read_text(encoding="utf-8").rstrip("\n")
        assert hashlib.sha256(t.encode()).hexdigest()[:16] == h, f"{k} alterato"
        cur = None
        for r in t.split("\n"):
            if r.startswith("@"):
                cur = {"head": r[1:].split("|"), "righe": []}
                recs.append(cur)
            else:
                cur["righe"].append(r.split("|"))
    return recs


def costruisci():
    meta = [r.split("|") for r in META.strip().split("\n")]
    recs = leggi()
    assert len(meta) == len(recs), (len(meta), len(recs))
    out = []
    for (aid, nome, paese, sport0, alias), rec in zip(meta, recs):
        wen, ten, rev, tit, itrev = rec["head"]
        sport_cur, pal, visti, leghe_viste = sport0, [], set(), {}
        for r in rec["righe"]:
            tipo = r[0]
            if tipo == "X":
                h = r[1].lower()
                sport_cur = next((v for k, v in SPORT_X if k in h), sport0)
            elif tipo == "M":
                _, c, m, y, ev = r
                ruolo = "allenatore" if "#coach" in ev or (aid, c, int(y)) in ALLENATORE_MEDAGLIE else "atleta"
                ev = ev.replace("#coach", "").strip()
                sp = "beach" if ev == "Beach" else ("pallavolo" if ev == "Indoor" else sport_cur)
                if aid == "marta-menegatti":
                    sp = "beach"
                pal.append({"anno": int(y), "sport": sp, "comp": COMP[c], "esito": MED[m], "gara": evento(ev), "ruolo": ruolo})
            elif tipo == "T":
                nomecomp = SLAM.get(r[1], r[1])
                for y, lab in anni(r[2]):
                    pal.append({"anno": y, "sport": sport0, "comp": nomecomp, "esito": "vittoria", "gara": "singolare" if r[1] in SLAM else "classifica generale", "ruolo": "atleta"})
            elif tipo == "C":
                h, v = r[1], r[2]
                if "Formula One" in h:
                    comp = "Mondiale di Formula 1"
                elif h == "World Cup":
                    comp = "Coppa del Mondo generale"
                elif "Grand Prix motorcycle" in h:
                    for classe, testo in re.findall(r"(\d+cc) – ([\d, ]+)", v.replace("1974500cc", "1974 500cc")):
                        for y, lab in anni(testo):
                            pal.append({"anno": y, "sport": sport0, "comp": f"Mondiale {classe}", "esito": "titolo", "gara": "", "ruolo": "atleta"})
                    continue
                else:
                    comp = "Mondiale " + h.replace(" World Championship", "").replace("MotoGP", "MotoGP / 500cc")
                yy = anni(v[v.find("("):]) if "(" in v else []
                if not yy:  # solo il numero (Stenmark): voce riassuntiva senza anno
                    pal.append({"anno": None, "sport": sport0, "comp": comp, "esito": "titolo", "gara": f"{v.split()[0]} volte", "ruolo": "atleta"})
                for y, lab in yy:
                    pal.append({"anno": y, "sport": sport0, "comp": comp, "esito": "titolo", "gara": "", "ruolo": "atleta"})
            elif tipo == "L":
                t = r[1]
                m = re.match(r"(?:(\d+)× )?(.+?) \((.+)\)$", t)
                nomecomp = m.group(2)
                comp = {"NBA champion": "Campionato NBA", "NBA Finals MVP": "MVP delle finali NBA",
                        "NBA Most Valuable Player": "MVP della stagione NBA", "WNBA champion": "Campionato WNBA",
                        "WNBA Finals MVP": "MVP delle finali WNBA", "EuroLeague champion": "Eurolega"}[nomecomp]
                ruolo = "allenatore" if comp in leghe_viste and aid == "kareem-abdul-jabbar" else "atleta"
                for y, lab in anni(m.group(3)):
                    k = (comp, y)
                    if k in visti:
                        continue
                    visti.add(k)
                    pal.append({"anno": y, "sport": sport0, "comp": comp, "esito": "titolo", "gara": "vice allenatore" if ruolo == "allenatore" else "", "ruolo": ruolo})
                leghe_viste[comp] = True
            elif tipo == "I":
                nomecomp, testo = r[1], r[2]
                if nomecomp in ("Campionato NBA", "Campionato WNBA") or (sport0 == "basket" and nomecomp in ("Eurolega", "Coppa dei Campioni")):
                    continue  # già dai titoli dell'infobox inglese
                n_occ = leghe_viste.get(("I", nomecomp), 0)
                leghe_viste[("I", nomecomp)] = n_occ + 1
                if aid == "gianluigi-buffon" and n_occ == 1:
                    continue  # 2004-05: titolo revocato alla Juventus
                if aid == "bill-russell" and n_occ == 1:
                    continue
                ruolo = "allenatore" if (aid, n_occ) in ALLENATORE_LEGHE or (aid, nomecomp) in ALLENATORE_LEGHE else "atleta"
                comp = LEGHE.get(nomecomp, nomecomp)
                if sport0 == "pallavolo" and nomecomp.startswith("Campionato"):
                    pass
                for y, lab in anni(testo):
                    k = (comp, y, ruolo)
                    if k in visti:
                        continue
                    visti.add(k)
                    pal.append({"anno": y, "stag": lab if "-" in lab else "", "sport": sport0, "comp": comp, "esito": "titolo", "gara": "", "ruolo": ruolo})
        sports = []
        for p in pal:
            if p["sport"] not in sports:
                sports.append(p["sport"])
        if sport0 not in sports:
            sports.insert(0, sport0)
        fonti = [{"i": "Wikipedia (en)", "t": f"{ten} (revisione {rev}, infobox)",
                  "u": f"https://en.wikipedia.org/w/index.php?title={ten.replace(' ', '_')}&oldid={rev}"}]
        if tit:
            fonti.append({"i": "Wikipedia (it)", "t": f"{tit} (revisione {itrev}, Palmarès)",
                          "u": f"https://it.wikipedia.org/w/index.php?title={tit.replace(' ', '_')}&oldid={itrev}"})
        a = {"id": aid, "nome": nome, "paese": paese, "sport": sports, "alias": alias.strip(), "palmares": pal, "fonti": fonti,
             "ruoli": sorted({p["ruolo"] for p in pal})}
        if aid in NOTE:
            a["nota"], f2 = NOTE[aid]
            a["fonti"].append(f2)
        out.append(a)
    return out


if __name__ == "__main__":
    A = costruisci()
    print(len(A), "atleti,", sum(len(a["palmares"]) for a in A), "risultati")
    for a in A:
        if a["id"] in ("karch-kiraly", "lebron-james", "franz-beckenbauer", "kareem-abdul-jabbar", "giacomo-agostini", "lorenzo-bernardi", "bill-russell"):
            print(a["id"], a["sport"], a["ruoli"])
            for p in a["palmares"]:
                print("   ", p)
