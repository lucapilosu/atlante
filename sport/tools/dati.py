#!/usr/bin/env python3
"""Genera sport/data/almanacco.json (Pilu Sports Almanac, prima versione, 26 novembre 2026).

Tessere: fatti verificati sulle fonti indicate (note in sport/tools/note_fonti.md).
Albi d'oro olimpici: trascritti dalle tabelle «Results summary» di Wikipedia
(revisioni indicate in ALBI_FONTE) lette dal browser il 26/11/2026, con controllo
a campione su olympics.com e fivb.com (Berlino 1936, Tokyo 1964, Atene 2004,
Rio 2016, Parigi 2024; Atlanta 1996 per il beach volley).
"""
import json
from pathlib import Path

SPORT = [
    ("olimpiadi", "Olimpiadi e mondo", "#c8a85a", "globo"),
    ("basket", "Basket", "#e2772f", "basket"),
    ("pallavolo", "Pallavolo", "#3f8fdc", "volley"),
    ("beach", "Beach volley", "#e8c24a", "beach"),
    ("atletica", "Atletica", "#d4574f", "pista"),
    ("calcio", "Calcio", "#3fae62", "calcio"),
    ("ciclismo", "Ciclismo", "#e3699f", "bici"),
    ("tennis", "Tennis", "#b7d33f", "tennis"),
    ("motori", "Motori", "#9aa3ad", "scacchi"),
    ("sci", "Sci", "#8fd6f6", "sci"),
    ("nuoto", "Nuoto", "#2fb7b3", "onde"),
]

OC = "olympics.com"


def f(ist, titolo, url):
    return {"i": ist, "t": titolo, "u": url}


V = []


def v(id, sport, anno, titolo, testo, luogo, fonti, italia=False, nota="", data="", circa=False):
    V.append({"id": id, "sport": sport, "anno": anno, "data": data, "circa": circa, "titolo": titolo,
              "testo": testo, "luogo": luogo, "fonti": fonti, "italia": italia, "nota": nota})


# ---------- Olimpiadi e sport nel mondo ----------
v("olimpia", "olimpiadi", -776, "I Giochi di Olimpia",
  "Nel santuario di Zeus a Olimpia, nel Peloponneso, si tengono i Giochi più famosi della Grecia antica. La data del 776 a.C. è quella che citano di solito le fonti scritte; i Giochi si svolgono ogni quattro anni fino al 393 d.C.",
  "Olimpia (Grecia)",
  [f(OC, "What is the origin of the Olympic Games?", "https://www.olympics.com/ioc/faq/history-and-origin-of-the-games/what-is-the-origin-of-the-olympic-games"),
   f(OC, "Athens 1896 - 125 years of shared Olympic values", "https://www.olympics.com/ioc/news/athens-1896-125-years-of-shared-olympic-values")],
  nota="Il CIO scrive che la data esatta d'inizio non si conosce: il 776 a.C. è la data tradizionale.", circa=True)
v("cio-1894", "olimpiadi", 1894, "Nasce il Comitato olimpico internazionale",
  "Il 23 giugno 1894, alla Sorbona di Parigi, un congresso organizzato da Pierre de Coubertin approva all'unanimità il ritorno dei Giochi olimpici. È la nascita del CIO.",
  "Parigi, Sorbona",
  [f(OC, "International Olympic Committee", "https://www.olympics.com/ioc/overview"),
   f(OC, "factsheet - Olympic Day (23 June)", "https://stillmed.olympics.com/media/Documents/Beyond-the-Games/Factsheets/Olympic-Day.pdf")],
  data="23 giugno 1894")
v("atene-1896", "olimpiadi", 1896, "Atene 1896, la prima Olimpiade moderna",
  "Dal 6 al 15 aprile 1896 Atene ospita i primi Giochi dell'era moderna, nello Stadio Panatenaico: oltre 300 atleti, tutti uomini, in 43 gare di 9 sport.",
  "Atene, Stadio Panatenaico",
  [f(OC, "Athens 1896", "https://www.olympics.com/en/sport-events/athens-1896"),
   f(OC, "The Opening Ceremony", "https://www.olympics.com/en/news/the-opening-ceremony")],
  data="6–15 aprile 1896")
v("parigi-1900-donne", "olimpiadi", 1900, "Parigi 1900: le prime donne ai Giochi",
  "Ai Giochi di Parigi, legati all'Esposizione universale, gareggiano per la prima volta le donne: 22 su 997 atleti. La tennista britannica Charlotte Cooper è la prima campionessa olimpica in una gara individuale.",
  "Parigi",
  [f(OC, "The first women Olympians", "https://www.olympics.com/en/news/the-first-women-olympians"),
   f(OC, "Paris 1900 Summer Olympics", "https://www.olympics.com/en/olympic-games/paris-1900")])
v("chamonix-1924", "olimpiadi", 1924, "Chamonix 1924, i primi Giochi invernali",
  "Dal 25 gennaio al 5 febbraio 1924 Chamonix ospita una «Settimana internazionale degli sport invernali» con 258 atleti di 16 paesi. Nel 1926 il CIO la riconosce come prima edizione dei Giochi olimpici invernali.",
  "Chamonix (Francia)",
  [f(OC, "When were the first Olympic Winter Games held?", "https://www.olympics.com/ioc/faq/history-and-origin-of-the-games/when-were-the-first-olympic-winter-games-held"),
   f(OC, "Chamonix 1924 Winter Olympics", "https://www.olympics.com/en/olympic-games/chamonix-1924")],
  data="25 gennaio – 5 febbraio 1924")
v("roma-1960-paralimpiadi", "olimpiadi", 1960, "Roma 1960, le prime Paralimpiadi",
  "Dal 18 al 25 settembre 1960, sei giorni dopo la chiusura delle Olimpiadi, Roma ospita i primi Giochi paralimpici, organizzati da Ludwig Guttmann e dal neurochirurgo italiano Antonio Maglio.",
  "Roma",
  [f("paralympic.org", "Rome 1960", "https://www.paralympic.org/rome-1960"),
   f("paralympic.org", "Paralympic Games", "https://www.paralympic.org/paralympic-games")],
  italia=True, data="18–25 settembre 1960",
  nota="Partecipanti: l'IPC indica 400 atleti da 23 paesi nella pagina generale e 319 atleti da 21 paesi nella pagina dedicata a Roma 1960; nel testo non c'è il numero.")
v("milano-cortina-2026", "olimpiadi", 2026, "Milano Cortina 2026, record dell'Italia",
  "Ai Giochi invernali di casa, dal 6 al 22 febbraio 2026, l'Italia vince 30 medaglie (10 ori, 6 argenti, 14 bronzi), il suo miglior risultato di sempre. Arianna Fontana arriva a 14 medaglie olimpiche: nessun atleta italiano ne ha vinte di più.",
  "Milano e Cortina d'Ampezzo",
  [f(OC, "Olympic Winter Games Milano Cortina 2026", "https://www.olympics.com/en/olympic-games/milano-cortina-2026"),
   f(OC, "Hosts Italy breaks all-time medal record at Winter Olympics", "https://www.olympics.com/en/news/hosts-italy-breaks-all-time-medal-record-at-winter-olympics-all-medals-complete-list"),
   f(OC, "Achievements, emotions and records: the best of the Milano Cortina 2026 Winter Olympics", "https://www.olympics.com/en/milano-cortina-2026/news/imprese-emozioni-e-record-il-meglio-dei-giochi-olimpici-invernali-di-milano-cortina-2026")],
  italia=True, data="6–22 febbraio 2026")

# ---------- Basket ----------
v("basket-naismith", "basket", 1891, "Naismith inventa il basket",
  "James Naismith, insegnante di educazione fisica alla scuola della YMCA di Springfield, nel Massachusetts, inventa un gioco da palestra per l'inverno. La prima partita si gioca il 21 dicembre 1891, con due cesti da pesche come canestri.",
  "Springfield (Massachusetts, USA)",
  [f("Britannica", "Basketball", "https://www.britannica.com/sports/basketball"),
   f("Naismith Basketball Hall of Fame", "First Team", "https://www.hoophall.com/hall-of-famers/first-team")],
  data="21 dicembre 1891")
v("basket-fiba", "basket", 1932, "Nasce la FIBA",
  "Il 18 giugno 1932, a Ginevra, otto federazioni nazionali (Argentina, Cecoslovacchia, Grecia, Italia, Lettonia, Portogallo, Romania e Svizzera) fondano la Federazione internazionale di basket e approvano regole comuni.",
  "Ginevra (Svizzera)",
  [f("FIBA", "FIBA celebrates 85th anniversary", "https://www.fiba.basketball/en/news/fiba-celebrates-85th-anniversary"),
   f("FIBA", "8 Founding Federations", "https://about.fiba.basketball/en/fiba-hall-of-fame/hall-of-famers/8-founding-federations")],
  italia=True, data="18 giugno 1932")
v("basket-berlino-1936", "basket", 1936, "Il basket arriva alle Olimpiadi",
  "A Berlino il basket entra nel programma olimpico. Si gioca all'aperto su campi in terra: la finale si disputa sotto la pioggia e gli Stati Uniti battono il Canada 19-8.",
  "Berlino",
  [f(OC, "Olympic basketball's muddy beginnings", "https://www.olympics.com/en/news/olympic-basketball-s-muddy-beginnings"),
   f("FIBA", "Olympic Games: Berlin 1936", "https://www.fiba.basketball/en/news/olympic-games-berlin-1936")])
v("basket-nba", "basket", 1946, "Nasce la lega che diventerà la NBA",
  "Nel 1946 a New York nasce la Basketball Association of America, che gioca la prima partita il 1° novembre. Nel 1949 si fonde con la National Basketball League: nasce la NBA.",
  "New York",
  [f("Britannica", "National Basketball Association (NBA)", "https://www.britannica.com/topic/National-Basketball-Association"),
   f("NBA", "About the NBA", "https://www.nba.com/news/about")])
v("basket-donne-1976", "basket", 1976, "Il basket femminile alle Olimpiadi",
  "A Montréal 1976 debutta il torneo olimpico femminile: vince l'Unione Sovietica, che in finale batte gli Stati Uniti.",
  "Montréal (Canada)",
  [f("FIBA", "Tokyo 2020 by numbers", "https://www.fiba.basketball/en/news/olympics-men-2020-news-tokyo-2020-by-numbers-stats-and-facts-from-the-olympic-basketball-tournaments"),
   f("Wikipedia", "Basketball at the Summer Olympics (rev. 1383154364)", "https://en.wikipedia.org/w/index.php?title=Basketball_at_the_Summer_Olympics&oldid=1383154364")])
v("basket-euro-1983", "basket", 1983, "Italia campione d'Europa",
  "Agli Europei in Francia l'Italia di Sandro Gamba vince tutte le sette partite e conquista il suo primo titolo europeo; in finale c'è la Spagna.",
  "Francia (Limoges, Caen, Nantes)",
  [f("FIBA", "All-Time Medalists - FIBA EuroBasket", "https://www.fiba.basketball/en/events/fiba-eurobasket-2025/all-time-medalists"),
   f("FIBA", "Top Five Italy Teams of All Time", "https://www.fiba.basketball/en/news/top-five-italy-teams-all-time")],
  italia=True)
v("basket-euro-1999", "basket", 1999, "Di nuovo campioni d'Europa",
  "Agli Europei del 1999, ancora in Francia, l'Italia vince il suo secondo titolo battendo la Spagna; Gregor Fučka è il miglior giocatore del torneo.",
  "Francia (finale a Parigi)",
  [f("FIBA", "All-Time Medalists - FIBA EuroBasket", "https://www.fiba.basketball/en/events/fiba-eurobasket-2025/all-time-medalists")],
  italia=True, nota="Che la Spagna sia la finalista viene dalla tabella FIBA (Italia prima, Spagna seconda).")
v("basket-atene-2004", "basket", 2004, "Argento olimpico ad Atene",
  "Ai Giochi di Atene l'Italia arriva in finale e vince l'argento, la sua medaglia olimpica più recente nel basket; l'oro va all'Argentina.",
  "Atene",
  [f(OC, "Athens 2004 Basketball Results", "https://www.olympics.com/en/olympic-games/athens-2004/results/basketball"),
   f("FIBA", "Back to the future: Pozzecco recalls...", "https://www.fiba.basketball/en/events/fiba-eurobasket-2025-qualifiers/news/eurobasket-2025-qualifiers-news-back-to-the-future-pozzecco-recalls-playing-in-eurobasket-qualifiers-1999-2003")],
  italia=True, nota="«La più recente» è una deduzione di Claude dall'albo d'oro olimpico 2008–2024, dove l'Italia non compare sul podio.")

# ---------- Pallavolo ----------
v("volley-morgan", "pallavolo", 1895, "Morgan inventa la pallavolo",
  "William G. Morgan, direttore sportivo della YMCA di Holyoke, nel Massachusetts, inventa un gioco meno faticoso del basket e lo chiama «mintonette». Presto diventerà volleyball.",
  "Holyoke (Massachusetts, USA)",
  [f("FIVB", "History", "https://www.fivb.com/volleyball/the-game/history/"),
   f("Britannica", "Who invented volleyball?", "https://www.britannica.com/question/Who-invented-volleyball")])
v("volley-fivb", "pallavolo", 1947, "Nasce la FIVB",
  "Nell'aprile 1947 a Parigi quattordici federazioni, tra cui l'Italia, fondano la Federazione internazionale di pallavolo. Dal 1984 ha sede a Losanna.",
  "Parigi",
  [f("FIVB", "Volleyball's Century: The FIVB Legacy", "https://www.fivb.com/inside-fivb/fivb/history/"),
   f("FIVB", "Volleyball History - Men's World Cup 2015", "http://worldcup.2015.men.fivb.com/en/competition/volleyballhistory")],
  italia=True)
v("volley-mondiale-1949", "pallavolo", 1949, "Il primo Mondiale",
  "A settembre Praga ospita il primo Campionato del mondo maschile: vince l'Unione Sovietica davanti a Cecoslovacchia e Bulgaria. Il Mondiale femminile arriverà nel 1952.",
  "Praga",
  [f("Volleyball World", "Men's World Championship by the numbers", "https://en.volleyballworld.com/volleyball/competitions/men-world-championship/2022/news/men-s-world-championship-by-the-numbers"),
   f("FIVB", "Volleyball's Century: The FIVB Legacy", "https://www.fivb.com/inside-fivb/fivb/history/")])
v("volley-tokyo-1964", "pallavolo", 1964, "La pallavolo diventa olimpica",
  "A Tokyo 1964 la pallavolo debutta ai Giochi, maschile e femminile insieme. Vincono l'Unione Sovietica tra gli uomini e il Giappone tra le donne, che in finale batte proprio l'URSS.",
  "Tokyo",
  [f(OC, "Volleyball: a brief history", "https://www.olympics.com/en/news/volleyball-a-brief-history"),
   f(OC, "Bewitched: Japan's 1964 gold in women's volleyball", "https://www.olympics.com/en/news/tokyo-1964-women-volleyball-japan-gold")])
v("volley-fenomeni", "pallavolo", 1990, "La «generazione dei fenomeni»",
  "Con Julio Velasco in panchina l'Italia vince il Mondiale 1990 a Rio de Janeiro. È il primo di tre titoli mondiali di fila: poi Atene 1994 e Tokyo 1998.",
  "Rio de Janeiro",
  [f("Volleyball World", "Worlds' roll of honour: 1949-2018", "https://en.volleyballworld.com/volleyball/competitions/men-world-championship/2022/news/men-s-world-championship-roll-of-honour"),
   f(OC, "De Giorgi, Velasco e Giani: dalla Generazione dei Fenomeni a Parigi 2024", "https://www.olympics.com/it/notizie/pallavolo-degiorgi-giani-velasco-olimpiadi-parigi-2024-generazione-fenomeni")],
  italia=True)
v("volley-parigi-2024", "pallavolo", 2024, "Oro olimpico per l'Italia femminile",
  "L'11 agosto 2024 a Parigi l'Italia di Velasco batte gli Stati Uniti 3-0 nella finale olimpica: è la prima medaglia olimpica della pallavolo femminile italiana, e subito d'oro.",
  "Parigi",
  [f(OC, "Paris 2024 volleyball: Italy's women win first Olympic volleyball gold", "https://www.olympics.com/en/news/paris-2024-results-italy-win-first-olympic-volleyball-gold")],
  italia=True, data="11 agosto 2024")
v("volley-2025", "pallavolo", 2025, "Doppio titolo mondiale",
  "Nel 2025 l'Italia vince entrambi i Mondiali: le donne il 7 settembre a Bangkok (3-2 alla Türkiye), gli uomini il 28 settembre a Manila (3-1 alla Bulgaria), quinto titolo maschile.",
  "Bangkok e Manila",
  [f(OC, "FIVB Women's World Championship 2025: Italy clinch world title", "https://www.olympics.com/en/news/fivb-womens-volleyball-world-championship-2025-italy-clinch-title"),
   f("Volleyball World", "Italy beat Bulgaria to triumph with second consecutive and fifth overall world title", "https://en.volleyballworld.com/volleyball/competitions/men-world-championship/news/italy-beat-bulgaria-to-triumph-with-second-consecutive-and-fifth-overall-world-title")],
  italia=True)

# ---------- Beach volley ----------
v("beach-santa-monica", "beach", 1920, "Due contro due a Santa Monica",
  "Sulle spiagge della California, e soprattutto a Santa Monica, negli anni Venti nasce il gioco a due per squadra. Il primo torneo si gioca alla fine degli anni Quaranta.",
  "Santa Monica (California, USA)",
  [f(OC, "Beach Volleyball", "https://www.olympics.com/en/sports/beach-volleyball/"),
   f("Britannica", "Beach volleyball", "https://www.britannica.com/sports/beach-volleyball")],
  circa=True,
  nota="Le fonti non concordano: olympics.com indica il 1920 per il gioco a due e il 1947 per il primo torneo; Britannica indica il 1930 e il 1948 (Will Rogers State Beach).")
v("beach-fivb-1987", "beach", 1987, "Il primo torneo FIVB",
  "Nel 1987 si gioca il primo torneo di beach volley riconosciuto dalla federazione internazionale. Nove anni dopo il beach volley sarà olimpico.",
  "",
  [f("FIVB", "FIVB celebrates 75th Anniversary", "https://www.fivb.com/fivb-celebrates-75th-anniversary/")])
v("beach-atlanta-1996", "beach", 1996, "Il beach volley diventa olimpico",
  "Dopo la prova dimostrativa di Barcellona 1992, il beach volley entra nei Giochi ad Atlanta: oltre 107.000 spettatori in sei giorni. Vincono Karch Kiraly e Kent Steffes (USA) e Jackie Silva e Sandra Pires (Brasile).",
  "Atlanta (USA)",
  [f("FIVB", "Beach volleyball marks 30 years as an Olympic sport", "https://www.fivb.com/beach-volleyball-marks-30-years-as-an-olympic-sport/"),
   f(OC, "Beach volleyball rules: All you need to know", "https://www.olympics.com/en/news/beach-volleyball-indoor-difference-rules-history-olympics")])
v("beach-mondiali-1997", "beach", 1997, "I primi Mondiali di beach volley",
  "L'anno dopo il debutto olimpico la FIVB organizza i primi Campionati del mondo di beach volley.",
  "",
  [f(OC, "History of volleyball: From origins to the Olympics", "https://www.olympics.com/en/news/what-history-volleyball-game-origin-mintonette-ymca-fivb-olympics")],
  nota="La sede non è stata verificata in questa sessione e non è indicata.")
v("beach-rio-2016", "beach", 2016, "Nicolai e Lupo d'argento a Rio",
  "Paolo Nicolai e Daniele Lupo arrivano in finale sulla spiaggia di Copacabana e vincono l'argento, la prima medaglia olimpica italiana nel beach volley.",
  "Rio de Janeiro, Copacabana",
  [f("Volleyball World", "A fresh start for Nicolai in 2022", "https://en.volleyballworld.com/beachvolleyball/competitions/beach-pro-tour-2022/news/it-s-all-new-for-nicolai-in-2022"),
   f(OC, "Rio 2016 Beach Volleyball Results", "https://www.olympics.com/en/olympic-games/rio-2016/results/beach-volleyball")],
  italia=True)

# ---------- Atletica ----------
v("atletica-iaaf", "atletica", 1912, "Nasce la federazione mondiale",
  "Il 17 luglio 1912, a Stoccolma, 17 federazioni fondano la IAAF (oggi World Athletics) per avere regole comuni e un elenco ufficiale dei record del mondo.",
  "Stoccolma",
  [f("World Athletics", "Early origins to 1930s", "https://worldathletics.org/heritage/history/early-origins-to-1930s")],
  data="17 luglio 1912")
v("atletica-mondiali-1983", "atletica", 1983, "I primi Mondiali di atletica",
  "Dal 7 al 14 agosto 1983 Helsinki ospita i primi Campionati del mondo: 1.355 atleti da 153 paesi. Fino ad allora il titolo mondiale era, di fatto, quello olimpico.",
  "Helsinki",
  [f("World Athletics", "1980s to end of 20th Century", "https://worldathletics.org/heritage/history/1980s-to-end-of-20th-century"),
   f("World Athletics", "History of the World Athletics Championships", "https://worldathletics.org/en/competitions/world-athletics-championships/world-athletics-championships-tokyo-2025-7190593/event-info/world-athletics-history")],
  data="7–14 agosto 1983")
v("atletica-958", "atletica", 2009, "9\"58 sui 100 metri",
  "Ai Mondiali di Berlino, il 16 agosto 2009, Usain Bolt corre i 100 metri in 9\"58: è ancora il record del mondo.",
  "Berlino, Olympiastadion",
  [f("World Athletics", "World records set at Berlin World Championships have been ratified", "https://worldathletics.org/news/news/world-records-set-at-berlin-world-championshi"),
   f("World Athletics", "100 Metres men - All Time Top Lists", "https://worldathletics.org/records/all-time-toplists/sprints/100-metres/outdoor/men/senior")],
  data="16 agosto 2009")

# ---------- Calcio ----------
v("calcio-fa", "calcio", 1863, "Le prime regole del calcio",
  "Il 26 ottobre 1863, alla Freemasons' Tavern di Londra, i rappresentanti di una dozzina di club fondano la Football Association e scrivono le prime regole comuni del gioco.",
  "Londra",
  [f("The FA", "The History of The FA", "https://www.thefa.com/about-football-association/who-we-are/history"),
   f("Britannica", "Football Association (FA)", "https://www.britannica.com/topic/Football-Association")],
  data="26 ottobre 1863")
v("calcio-fifa", "calcio", 1904, "Nasce la FIFA",
  "Il 21 maggio 1904 a Parigi i rappresentanti di sette federazioni europee fondano la Federazione internazionale del calcio.",
  "Parigi",
  [f("FIFA", "FIFA celebrates 119th birthday", "https://inside.fifa.com/organisation/news/fifa-celebrates-119th-birthday"),
   f("FIFA", "Happy birthday FIFA!", "https://www.fifa.com/who-we-are/news/happy-birthday-fifa-772772")],
  data="21 maggio 1904")
v("calcio-mondiale-1930", "calcio", 1930, "Il primo Mondiale",
  "In Uruguay si gioca il primo Campionato del mondo, con 13 squadre. Il 30 luglio, a Montevideo, l'Uruguay batte l'Argentina 4-2 in finale.",
  "Montevideo",
  [f("FIFA", "FIFA World Cup champions: 1930-1978", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1930-1978-uruguay-italy-germany-brazil-england-argentina")])
v("calcio-italia-1934", "calcio", 1934, "Italia campione del mondo",
  "L'Italia di Vittorio Pozzo vince il Mondiale di casa battendo la Cecoslovacchia 2-1 ai supplementari a Roma. Nel 1938, in Francia, rivince: è la prima squadra a confermarsi campione.",
  "Roma",
  [f("FIFA", "FIFA World Cup champions: 1930-1978", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1930-1978-uruguay-italy-germany-brazil-england-argentina"),
   f("FIFA", "The back-to-back champions", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/italy-brazil-consecutive-titles")],
  italia=True)
v("calcio-italia-1982", "calcio", 1982, "Campioni del mondo in Spagna",
  "L'11 luglio 1982, al Bernabéu di Madrid, l'Italia batte la Germania Ovest 3-1 e vince il suo terzo Mondiale, il primo dal 1938.",
  "Madrid",
  [f("FIFA", "FIFA World Cup champions: 1982-2026", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1982-2026-italy-argentina-germany-brazil-france-spain")],
  italia=True, data="11 luglio 1982")
v("calcio-donne-1991", "calcio", 1991, "Il primo Mondiale femminile",
  "La FIFA organizza in Cina il primo Campionato del mondo femminile.",
  "Cina",
  [f("FIFA", "We are FIFA", "https://jobs.fifa.com/we-are-fifa")])
v("calcio-italia-2006", "calcio", 2006, "Il quarto titolo mondiale",
  "In Germania l'Italia vince il suo quarto Mondiale: la finale con la Francia finisce 1-1 e gli azzurri vincono 5-3 ai rigori.",
  "Germania",
  [f("FIFA", "FIFA World Cup champions: 1982-2026", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/world-cup-champions-1982-2026-italy-argentina-germany-brazil-france-spain"),
   f("FIFA", "Teams with the most FIFA World Cup titles", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/teams-most-wins-titles-trophies")],
  italia=True)
v("calcio-mondiale-2026", "calcio", 2026, "Mondiale 2026: vince la Spagna",
  "Le pagine FIFA aggiornate indicano la Spagna campione del mondo 2026: è il suo secondo titolo.",
  "Canada, Messico e Stati Uniti",
  [f("FIFA", "Teams with the most FIFA World Cup titles", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/teams-most-wins-titles-trophies"),
   f("FIFA", "World Cup-winning teams by total time trailed", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/winners-champions-time-behind-losing")],
  nota="Verificato solo su due pagine statistiche FIFA (titoli per squadra e minuti in svantaggio). Paesi organizzatori da conoscenza di Claude, non da una fonte letta in questa sessione.")

# ---------- Ciclismo ----------
v("ciclismo-giro-1909", "ciclismo", 1909, "Il primo Giro d'Italia",
  "Il 13 maggio 1909 parte da Milano il primo Giro d'Italia, organizzato dalla Gazzetta dello Sport: 8 tappe e 2.448 km. Vince Luigi Ganna.",
  "Milano",
  [f("Giro d'Italia", "Giro d'Italia: tutte le edizioni storiche 1909-1922", "https://archivio.giroditalia.it/it/edizioni/1909-1922/"),
   f("Giro d'Italia", "Ricordi da… Torino, 1909: il primo Giro", "https://www.giroditalia.it/news/ricordi-da-torino-1909-il-primo-giro-e-il-cortese-inganno/")],
  italia=True, data="13 maggio 1909")
v("ciclismo-maglia-rosa", "ciclismo", 1931, "Nasce la maglia rosa",
  "Nel 1931 Armando Cougnet, giornalista della Gazzetta dello Sport, introduce una maglia rosa per riconoscere subito il primo della classifica.",
  "",
  [f("Giro d'Italia", "90 Years of the Maglia Rosa", "https://www.giroditalia.it/en/magliarosa/")],
  italia=True)

# ---------- Tennis ----------
v("tennis-wimbledon", "tennis", 1877, "Il primo Wimbledon",
  "Nel luglio 1877 l'All England Croquet and Lawn Tennis Club organizza il primo torneo di tennis su prato: 22 iscritti, solo il singolare maschile. Vince Spencer Gore.",
  "Londra, Wimbledon",
  [f("Britannica", "Tennis", "https://www.britannica.com/sports/tennis"),
   f("Wimbledon", "The Championships 1877 Gentlemen's Singles", "https://assets.wimbledon.com/archive/draws/pdfs/draws/1877_MS_A4.pdf")])
v("tennis-davis", "tennis", 1900, "Nasce la Coppa Davis",
  "Nel 1900 Stati Uniti e Gran Bretagna si sfidano per un trofeo comprato da Dwight Davis: nasce la Coppa Davis, oggi la più grande competizione annuale a squadre nazionali.",
  "Boston (USA)",
  [f("Davis Cup", "History", "https://www.daviscup.com/en/about/history"),
   f("Britannica", "Davis Cup", "https://www.britannica.com/sports/Davis-Cup")])
v("tennis-open", "tennis", 1968, "Comincia l'era Open",
  "Nel marzo 1968 la federazione internazionale approva i primi tornei aperti sia ai dilettanti sia ai professionisti: comincia l'era Open.",
  "",
  [f("Britannica", "Tennis - Professional and open tennis", "https://www.britannica.com/sports/tennis/Professional-and-open-tennis"),
   f("Britannica", "What Is the Open Era in Tennis?", "https://www.britannica.com/sports/What-Is-the-Open-Era-in-Tennis")])
v("tennis-davis-1976", "tennis", 1976, "Italia, prima Coppa Davis",
  "A dicembre, a Santiago del Cile, l'Italia di Adriano Panatta e Corrado Barazzutti batte il Cile 4-1 e vince la sua prima Coppa Davis.",
  "Santiago del Cile",
  [f("Davis Cup", "Previous Champions", "https://www.daviscup.com/en/previous-champions"),
   f("Davis Cup", "Italy Davis Cup team profile", "https://www.daviscup.com/en/news/italy-team-profile-article")],
  italia=True)
v("tennis-davis-tris", "tennis", 2023, "Tre Coppe Davis di fila",
  "Dopo 47 anni l'Italia torna a vincere la Coppa Davis nel 2023 a Malaga (2-0 all'Australia). Si ripete nel 2024 (Paesi Bassi) e nel 2025 a Bologna (Spagna).",
  "Malaga e Bologna",
  [f("Davis Cup", "Previous Champions", "https://www.daviscup.com/en/previous-champions"),
   f("Davis Cup", "Italy: meet the Davis Cup by Generali Final 8 team", "https://www.daviscup.com/en/news/italy-meet-the-davis-cup-by-generali-final-8-team")],
  italia=True)

# ---------- Motori ----------
v("motori-le-mans", "motori", 1923, "La prima 24 Ore di Le Mans",
  "Il 26 e 27 maggio 1923 33 auto partono per la prima corsa di 24 ore sul circuito di Le Mans. Vincono André Lagache e René Léonard su Chenard & Walcker.",
  "Le Mans (Francia)",
  [f("24h Le Mans", "A century of racing: the 24 Hours of Le Mans is 100 years old!", "https://www.24h-lemans.com/en/news/a-century-of-racing-the-24-hours-of-le-mans-is-100-years-old-57463"),
   f("24h Le Mans", "First winner of the 24 Hours of Le Mans", "https://www.24h-lemans.com/en/news/first-winner-of-the-24-hours-of-le-mans-who-was-rene-leonard-andre-lagaches-teammate-50683")],
  data="26–27 maggio 1923")
v("motori-f1-1950", "motori", 1950, "Il primo Gran Premio di Formula 1",
  "Il 13 maggio 1950 a Silverstone si corre la prima gara del Mondiale di Formula 1. Vince l'italiano Giuseppe «Nino» Farina su Alfa Romeo, che a fine anno sarà il primo campione del mondo.",
  "Silverstone (Inghilterra)",
  [f("Formula 1", "Ten fascinating facts about the very first F1 race", "https://www.formula1.com/en/latest/article/f1-first-race-1950-silverstone.2f2zI6BmGT9bnK4vX10paZ"),
   f("Formula 1", "Great Britain - Silverstone", "https://www.formula1.com/en/information/great-britain-silverstone-circuit.2DtFVI1FjkYgLVdGhbAIv0")],
  italia=True, data="13 maggio 1950")

# ---------- Sci ----------
v("sci-fis", "sci", 1924, "Nasce la FIS",
  "Il 2 febbraio 1924, durante i Giochi di Chamonix, 14 nazioni fondano la Federazione internazionale dello sci, erede della commissione nata a Christiania (Oslo) nel 1910.",
  "Chamonix (Francia)",
  [f("FIS", "History of FIS", "https://www.fis-ski.com/en/inside-fis/about-fis/history/history-of-fis")],
  data="2 febbraio 1924")
v("sci-murren-1931", "sci", 1931, "I primi Mondiali di sci alpino",
  "Dal 20 al 23 febbraio 1931 Mürren, in Svizzera, ospita i primi Mondiali di sci alpino: discesa e slalom, maschili e femminili. Tra i paesi in gara c'è anche l'Italia.",
  "Mürren (Svizzera)",
  [f("FIS", "Where it all began: Mürren 1931", "https://100.fis-ski.com/moments/where-it-all-began-muerren-1931")],
  data="20–23 febbraio 1931")
v("sci-coppa-1967", "sci", 1967, "Nasce la Coppa del Mondo",
  "Il 5 gennaio 1967 a Berchtesgaden si corre la prima gara della Coppa del Mondo di sci alpino, nata da un'idea del giornalista francese Serge Lang. La prima stagione conta 17 gare.",
  "Berchtesgaden (Germania)",
  [f("FIS", "Alpine World Cup turns 60", "https://www.fis-ski.com/alpine-skiing/news/2026-27/crystal-globes-prominent-calendars-wild-cards-confirmed-alpine-world-cup-turns-60"),
   f("FIS", "The Ski World Cup, a success story", "https://100.fis-ski.com/moments/the-ski-world-cup-a-success-story")],
  data="5 gennaio 1967")

# ---------- Nuoto ----------
v("nuoto-fina", "nuoto", 1908, "Nasce la FINA",
  "Il 19 luglio 1908, durante le Olimpiadi di Londra, otto federazioni fondano la Federazione internazionale del nuoto (oggi World Aquatics).",
  "Londra",
  [f("World Aquatics", "Overview and history", "https://www.worldaquatics.com/content/overview-and-history")],
  data="19 luglio 1908")
v("nuoto-mondiali-1973", "nuoto", 1973, "I primi Mondiali di nuoto",
  "Nel 1973 Belgrado ospita i primi Campionati del mondo di nuoto, pallanuoto, tuffi e nuoto sincronizzato.",
  "Belgrado",
  [f("World Aquatics", "Overview and history", "https://www.worldaquatics.com/content/overview-and-history")])

# ---------- Albi d'oro olimpici ----------
P = {"United States": "Stati Uniti", "Canada": "Canada", "Mexico": "Messico", "Poland": "Polonia", "France": "Francia",
     "Brazil": "Brasile", "Soviet Union": "Unione Sovietica", "Uruguay": "Uruguay", "Argentina": "Argentina", "Italy": "Italia",
     "Puerto Rico": "Porto Rico", "Yugoslavia": "Jugoslavia", "Cuba": "Cuba", "Spain": "Spagna", "Australia": "Australia",
     "Croatia": "Croazia", "Lithuania": "Lituania", "Unified Team": "Squadra Unificata", "FR Yugoslavia": "RF Jugoslavia",
     "Russia": "Russia", "Serbia": "Serbia", "Slovenia": "Slovenia", "Germany": "Germania", "Bulgaria": "Bulgaria",
     "Czechoslovakia": "Cecoslovacchia", "South Korea": "Corea del Sud", "China": "Cina", "Hungary": "Ungheria",
     "Ukraine": "Ucraina", "Japan": "Giappone", "Belgium": "Belgio", "Romania": "Romania", "East Germany": "Germania Est",
     "Netherlands": "Paesi Bassi", "ROC": "ROC (Russia)", "North Korea": "Corea del Nord", "Peru": "Perù", "Turkey": "Turchia",
     "Portugal": "Portogallo", "Switzerland": "Svizzera", "Latvia": "Lettonia", "Norway": "Norvegia", "Qatar": "Qatar",
     "Sweden": "Svezia", "Greece": "Grecia", "United Kingdom": "Regno Unito"}
SEDI = {"Berlin": "Berlino", "London": "Londra", "Helsinki": "Helsinki", "Melbourne": "Melbourne", "Rome": "Roma",
        "Tokyo": "Tokyo", "Mexico City": "Città del Messico", "Munich": "Monaco di Baviera", "Montreal": "Montréal",
        "Moscow": "Mosca", "Los Angeles": "Los Angeles", "Seoul": "Seul", "Barcelona": "Barcellona", "Atlanta": "Atlanta",
        "Sydney": "Sydney", "Athens": "Atene", "Beijing": "Pechino", "Rio de Janeiro": "Rio de Janeiro", "Paris": "Parigi"}


def righe(testo):
    out = []
    for r in testo.strip().splitlines():
        a, s, oro, ris, arg, bro = [x.strip() for x in r.split("|")]
        out.append({"anno": int(a), "sede": SEDI[s], "oro": P.get(oro, oro), "ris": ris, "argento": P.get(arg, arg), "bronzo": P.get(bro, bro)})
    return out


BASKET_M = """
1936|Berlin|United States|19–8|Canada|Mexico
1948|London|United States|65–21|France|Brazil
1952|Helsinki|United States|36–25|Soviet Union|Uruguay
1956|Melbourne|United States|89–55|Soviet Union|Uruguay
1960|Rome|United States|81–57|Soviet Union|Brazil
1964|Tokyo|United States|73–59|Soviet Union|Brazil
1968|Mexico City|United States|65–50|Yugoslavia|Soviet Union
1972|Munich|Soviet Union|51–50|United States|Cuba
1976|Montreal|United States|95–74|Yugoslavia|Soviet Union
1980|Moscow|Yugoslavia|86–77|Italy|Soviet Union
1984|Los Angeles|United States|96–65|Spain|Yugoslavia
1988|Seoul|Soviet Union|76–63|Yugoslavia|United States
1992|Barcelona|United States|117–85|Croatia|Lithuania
1996|Atlanta|United States|95–69|FR Yugoslavia|Lithuania
2000|Sydney|United States|85–75|France|Lithuania
2004|Athens|Argentina|84–69|Italy|United States
2008|Beijing|United States|118–107|Spain|Argentina
2012|London|United States|107–100|Spain|Russia
2016|Rio de Janeiro|United States|96–66|Serbia|Spain
2020|Tokyo|United States|87–82|France|Australia
2024|Paris|United States|98–87|France|Serbia
"""
BASKET_F = """
1976|Montreal|Soviet Union|112–77|United States|Bulgaria
1980|Moscow|Soviet Union|104–73|Bulgaria|Yugoslavia
1984|Los Angeles|United States|85–55|South Korea|China
1988|Seoul|United States|77–70|Yugoslavia|Soviet Union
1992|Barcelona|Unified Team|76–66|China|United States
1996|Atlanta|United States|111–87|Brazil|Australia
2000|Sydney|United States|76–54|Australia|Brazil
2004|Athens|United States|74–63|Australia|Russia
2008|Beijing|United States|92–65|Australia|Russia
2012|London|United States|86–50|France|Australia
2016|Rio de Janeiro|United States|101–72|Spain|Serbia
2020|Tokyo|United States|90–75|Japan|France
2024|Paris|United States|67–66|France|Australia
"""
VOLLEY_M = """
1964|Tokyo|Soviet Union|girone|Czechoslovakia|Japan
1968|Mexico City|Soviet Union|girone|Japan|Czechoslovakia
1972|Munich|Japan|3–1|East Germany|Soviet Union
1976|Montreal|Poland|3–2|Soviet Union|Cuba
1980|Moscow|Soviet Union|3–1|Bulgaria|Romania
1984|Los Angeles|United States|3–0|Brazil|Italy
1988|Seoul|United States|3–1|Soviet Union|Argentina
1992|Barcelona|Brazil|3–0|Netherlands|United States
1996|Atlanta|Netherlands|3–2|Italy|FR Yugoslavia
2000|Sydney|FR Yugoslavia|3–0|Russia|Italy
2004|Athens|Brazil|3–1|Italy|Russia
2008|Beijing|United States|3–1|Brazil|Russia
2012|London|Russia|3–2|Brazil|Italy
2016|Rio de Janeiro|Brazil|3–0|Italy|United States
2020|Tokyo|France|3–2|ROC|Argentina
2024|Paris|France|3–0|Poland|United States
"""
VOLLEY_F = """
1964|Tokyo|Japan|girone|Soviet Union|Poland
1968|Mexico City|Soviet Union|girone|Japan|Poland
1972|Munich|Soviet Union|3–2|Japan|North Korea
1976|Montreal|Japan|3–0|Soviet Union|South Korea
1980|Moscow|Soviet Union|3–1|East Germany|Bulgaria
1984|Los Angeles|China|3–0|United States|Japan
1988|Seoul|Soviet Union|3–2|Peru|China
1992|Barcelona|Cuba|3–1|Unified Team|United States
1996|Atlanta|Cuba|3–1|China|Brazil
2000|Sydney|Cuba|3–2|Russia|Brazil
2004|Athens|China|3–2|Russia|Cuba
2008|Beijing|Brazil|3–1|United States|China
2012|London|Brazil|3–1|United States|Japan
2016|Rio de Janeiro|China|3–1|Serbia|United States
2020|Tokyo|United States|3–0|Brazil|Serbia
2024|Paris|Italy|3–0|United States|Brazil
"""
BEACH_M = """
1996|Atlanta|Kiraly / Steffes (Stati Uniti)|2–0|Dodd / Whitmarsh (Stati Uniti)|Child / Heese (Canada)
2000|Sydney|Blanton / Fonoimoana (Stati Uniti)|2–0|Zé Marco / Ricardo (Brasile)|Ahmann / Hager (Germania)
2004|Athens|Emanuel / Ricardo (Brasile)|2–0|Bosma / Herrera (Spagna)|Heuscher / Kobel (Svizzera)
2008|Beijing|Dalhausser / Rogers (Stati Uniti)|2–1|Márcio / Fábio Luiz (Brasile)|Emanuel / Ricardo (Brasile)
2012|London|Brink / Reckermann (Germania)|2–1|Alison / Emanuel (Brasile)|Pļaviņš / Šmēdiņš (Lettonia)
2016|Rio de Janeiro|Alison / Bruno (Brasile)|2–0|Lupo / Nicolai (Italia)|Brouwer / Meeuwsen (Paesi Bassi)
2020|Tokyo|Mol / Sørum (Norvegia)|2–0|Krasilnikov / Stoyanovskiy (ROC)|Tijan / Younousse (Qatar)
2024|Paris|Åhman / Hellvig (Svezia)|2–0|Ehlers / Wickler (Germania)|Mol / Sørum (Norvegia)
"""
BEACH_F = """
1996|Atlanta|Pires / Silva (Brasile)|2–0|Rodrigues / Samuel (Brasile)|Cook / Pottharst (Australia)
2000|Sydney|Cook / Pottharst (Australia)|2–0|Shelda / Adriana Behar (Brasile)|Pires / Samuel (Brasile)
2004|Athens|May / Walsh (Stati Uniti)|2–0|Shelda / Adriana Behar (Brasile)|McPeak / Youngs (Stati Uniti)
2008|Beijing|May-Treanor / Walsh Jennings (Stati Uniti)|2–0|Tian / Wang (Cina)|Xue / Zhang (Cina)
2012|London|May-Treanor / Walsh Jennings (Stati Uniti)|2–0|Kessy / Ross (Stati Uniti)|Larissa / Juliana (Brasile)
2016|Rio de Janeiro|Ludwig / Walkenhorst (Germania)|2–0|Ágatha / Bárbara (Brasile)|Ross / Walsh Jennings (Stati Uniti)
2020|Tokyo|Klineman / Ross (Stati Uniti)|2–0|Artacho del Solar / Clancy (Australia)|Heidrich / Vergé-Dépré (Svizzera)
2024|Paris|Ana Patrícia / Duda (Brasile)|2–1|Humana-Paredes / Wilkerson (Canada)|Brunner / Hüberli (Svizzera)
"""


def wp(titolo, rev):
    return f("Wikipedia", f"{titolo} (revisione {rev}, tabelle «Results summary»)",
             f"https://en.wikipedia.org/w/index.php?title={titolo.replace(' ', '_')}&oldid={rev}")


ALBI = {
    "basket": {"titolo": "Albo d'oro olimpico del basket", "tornei": [
        {"nome": "Uomini", "righe": righe(BASKET_M)}, {"nome": "Donne", "righe": righe(BASKET_F)}],
        "fonti": [wp("Basketball at the Summer Olympics", 1383154364),
                  f(OC, "Athens 2004 Basketball Results", "https://www.olympics.com/en/olympic-games/athens-2004/results/basketball")]},
    "pallavolo": {"titolo": "Albo d'oro olimpico della pallavolo", "tornei": [
        {"nome": "Uomini", "righe": righe(VOLLEY_M)}, {"nome": "Donne", "righe": righe(VOLLEY_F)}],
        "fonti": [wp("Volleyball at the Summer Olympics", 1381863204),
                  f(OC, "Volleyball: a brief history", "https://www.olympics.com/en/news/volleyball-a-brief-history")]},
    "beach": {"titolo": "Albo d'oro olimpico del beach volley", "tornei": [
        {"nome": "Uomini", "righe": righe(BEACH_M)}, {"nome": "Donne", "righe": righe(BEACH_F)}],
        "fonti": [wp("Beach volleyball at the Summer Olympics", 1380739173),
                  f("FIVB", "History (beach volleyball)", "https://www.fivb.com/beach-volleyball/the-game/history/")]},
}
NOTA_ALBI = ("Trascritto il 26/11/2026 dalle tabelle di Wikipedia indicate (revisione fissata); controllato a campione "
             "su olympics.com, FIVB e FIBA (Berlino 1936, Tokyo 1964, Atlanta 1996, Atene 2004, Rio 2016, Parigi 2024). "
             "Nel 1964 e nel 1968 la pallavolo si giocava a girone unico, senza finale.")

dati = {"sport": [{"id": a, "nome": b, "colore": c, "icona": d} for a, b, c, d in SPORT],
        "voci": sorted(V, key=lambda x: (x["anno"], x["id"])), "albi": ALBI, "nota_albi": NOTA_ALBI,
        "aggiornato": "26 novembre 2026"}
ids = [x["id"] for x in V]
assert len(ids) == len(set(ids))
assert all(x["sport"] in {s[0] for s in SPORT} for x in V)
Path("sport/data").mkdir(parents=True, exist_ok=True)
Path("sport/data/almanacco.json").write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(V), "tessere;", sum(len(t["righe"]) for a in ALBI.values() for t in a["tornei"]), "righe di albo d'oro")
