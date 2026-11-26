"""Tessere nuove della v0.3 (26/11/2026): risultati e record dal mondo, per bilanciare l'Italia.
Ogni fatto è stato letto sulla fonte indicata (ricerche del 26/11/2026)."""


def aggiungi(v, f):
    OC = "olympics.com"
    v("owens-1936", "atletica", 1936, "Owens, quattro ori a Berlino",
      "Ai Giochi di Berlino Jesse Owens vince 100 m, 200 m, salto in lungo e staffetta 4×100. Il record di quattro ori nell'atletica in una sola edizione resterà ineguagliato fino a Carl Lewis, a Los Angeles 1984.",
      "Berlino", [f(OC, "Berlin 1936 Summer Olympics", "https://www.olympics.com/en/olympic-games/berlin-1936"),
                  f(OC, "Jesse Owens – biografia", "https://www.olympics.com/en/athletes/jesse-owens")])
    v("bannister-1954", "atletica", 1954, "Il primo miglio sotto i 4 minuti",
      "Il 6 maggio 1954, in una gara a Oxford, lo studente di medicina inglese Roger Bannister corre il miglio in 3'59\"4: è il primo uomo sotto i quattro minuti.",
      "Oxford (Regno Unito)", [f("Britannica", "Roger Bannister", "https://www.britannica.com/biography/Roger-Bannister")], data="6 maggio 1954")
    v("bikila-1960", "atletica", 1960, "Bikila, maratona a piedi nudi",
      "A Roma l'etiope Abebe Bikila vince la maratona olimpica correndo scalzo, in 2h15'16\": è il primo africano nero campione olimpico della maratona. Quattro anni dopo, a Tokyo, vincerà di nuovo.",
      "Roma", [f(OC, "Abebe Bikila wins men's marathon barefoot", "https://www.olympics.com/en/news/this-week-in-olympic-history-9-15-september-abebe-bikila-wins-mens-marathon-barefoot"),
               f(OC, "Abebe Bikila – biografia", "https://www.olympics.com/en/athletes/abebe-bikila")], data="10 settembre 1960")
    v("beamon-1968", "atletica", 1968, "Beamon, 8,90 nel lungo",
      "Ai Giochi di Città del Messico Bob Beamon salta 8,90 m al primo tentativo della finale e migliora il record del mondo di 55 centimetri. Resta tuttora il record olimpico.",
      "Città del Messico", [f(OC, "Beamon breaks World and Olympic record", "https://www.olympics.com/en/news/week-in-olympic-history-14-20-october"),
                            f(OC, "Olympic jump records", "https://www.olympics.com/en/news/olympic-records-jump-high-long-triple-pole-vault")], data="18 ottobre 1968")
    v("kipchoge-2019", "atletica", 2019, "La maratona sotto le due ore",
      "A Vienna, in una prova organizzata apposta con 41 lepri, Eliud Kipchoge corre i 42,195 km in 1h59'40\". È il primo sotto le due ore, ma non vale come record del mondo perché non è una gara in condizioni regolari.",
      "Vienna", [f(OC, "Eliud Kipchoge runs first sub two hour marathon", "https://www.olympics.com/en/news/eliud-kipchoge-first-sub-two-hour-marathon"),
                 f(OC, "Eliud Kipchoge – biografia", "https://www.olympics.com/en/athletes/eliud-kipchoge")], data="12 ottobre 2019")
    v("comaneci-1976", "ginnastica", 1976, "Comăneci, il primo 10",
      "A Montréal la romena Nadia Comăneci, 14 anni, ottiene alle parallele asimmetriche il primo 10 della storia olimpica. Il tabellone, che non prevedeva il 10, mostra «1.00». Ne prenderà altri sei in quei Giochi.",
      "Montréal", [f(OC, "Nadia Comaneci scores the first perfect 10", "https://www.olympics.com/en/news/this-week-in-olympic-history-july-15-21-nadia-comaneci-scores-the-first-perfect-10-in-gymnastics"),
                   f(OC, "Nadia Comaneci – biografia", "https://www.olympics.com/en/athletes/nadia-comaneci")], data="18 luglio 1976")
    v("spitz-1972", "nuoto", 1972, "Spitz, sette ori e sette record",
      "A Monaco di Baviera Mark Spitz vince sette gare su sette, tutte con il record del mondo. Il primato di ori in una sola edizione durerà 36 anni.",
      "Monaco di Baviera", [f(OC, "Mark Spitz – biografia", "https://www.olympics.com/en/athletes/mark-spitz"),
                            f(OC, "Munich 1972 Summer Olympics", "https://www.olympics.com/en/olympic-games/munich-1972")])
    v("phelps-2008", "nuoto", 2008, "Phelps, otto ori a Pechino",
      "A Pechino Michael Phelps vince tutte le otto gare a cui partecipa, sette con il record del mondo, e supera i sette ori di Spitz. Chiuderà la carriera con 28 medaglie olimpiche, 23 d'oro.",
      "Pechino", [f(OC, "Phelps' eight-gold haul ten years on", "https://www.olympics.com/en/news/phelps-eight-gold-haul-ten-years-on-could-it-happen-again"),
                  f(OC, "Michael Phelps – biografia", "https://www.olympics.com/en/athletes/michael-phelps-ii")], data="17 agosto 2008")
    v("chamberlain-1962", "basket", 1962, "Chamberlain, 100 punti",
      "A Hershey, in Pennsylvania, Wilt Chamberlain segna 100 punti nella vittoria dei Philadelphia Warriors sui New York Knicks (169-147). È ancora il record NBA in una partita.",
      "Hershey (Stati Uniti)", [f("NBA", "Top Moments: Wilt Chamberlain scores 100", "https://www.nba.com/news/history-top-moments-wilt-chamberlain-scores-100")], data="2 marzo 1962")
    v("dream-team-1992", "basket", 1992, "Il Dream Team",
      "Barcellona 1992 è la prima Olimpiade aperta ai giocatori NBA. Gli Stati Uniti di Jordan, Magic Johnson, Bird e Barkley vincono l'oro battendo gli avversari con una media di 44 punti di scarto.",
      "Barcellona", [f(OC, "Dream Team 1992 Revisited", "https://www.olympics.com/en/news/dream-team-1992-usa-basketball-olympics"),
                     f(OC, "The Barcelona 1992 Dream Team", "https://www.olympics.com/en/topics/this-is-the-dream-team")])
    v("lebron-2023", "basket", 2023, "LeBron miglior marcatore di sempre",
      "Il 7 febbraio 2023 LeBron James supera i 38.387 punti di Kareem Abdul-Jabbar e diventa il miglior marcatore nella storia della NBA. Il record di Abdul-Jabbar resisteva da 39 anni.",
      "Los Angeles", [f("NBA", "LeBron James surpasses Kareem Abdul-Jabbar for NBA career scoring record", "https://www.nba.com/news/lebron-james-scoring-tracker"),
                      f("NBA", "LeBron James set to become 1st player to score 50,000 total points", "https://www.nba.com/news/lebron-james-50000-total-points-milestone")], data="7 febbraio 2023")
    v("cuba-volley-2000", "pallavolo", 2000, "Cuba, tre ori di fila",
      "Con il successo di Sydney 2000 la nazionale femminile cubana, quella di Regla Torres e Mireya Luis, vince il terzo oro olimpico consecutivo dopo Barcellona 1992 e Atlanta 1996. Nessun'altra squadra femminile ci è riuscita.",
      "Sydney", [f("FIVB", "Cuba aim to reignite past glory on World Championship return", "https://www.fivb.com/cuba-aim-to-reignite-past-glory-on-world-championship-return/"),
                 f(OC, "The history of Olympic volleyball", "https://www.olympics.com/en/news/the-history-of-olympic-volleyball")])
    v("may-walsh-2012", "beach", 2012, "May-Treanor e Walsh, tre ori",
      "A Londra Misty May-Treanor e Kerri Walsh Jennings battono le connazionali Kessy e Ross e vincono il terzo oro olimpico consecutivo, dopo Atene 2004 e Pechino 2008.",
      "Londra", [f(OC, "Misty May-Treanor – biografia", "https://www.olympics.com/en/athletes/misty-may-treanor"),
                 f(OC, "How May-Treanor and Walsh Jennings danced to victory", "https://www.olympics.com/en/news/how-may-treanor-and-walsh-jennings-danced-to-victory")])
    v("pele-1958", "calcio", 1958, "Pelé, campione a 17 anni",
      "In Svezia il Brasile vince il suo primo Mondiale battendo i padroni di casa 5-2 in finale. Pelé, 17 anni, segna due gol: è ancora il più giovane marcatore in una finale mondiale.",
      "Solna (Svezia)", [f("FIFA", "Brazil v Sweden, 1958", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/brazil-sweden-1958"),
                         f("FIFA", "Behind the World Cup record: Pele", "https://inside.fifa.com/tournaments/mens/worldcup/1958sweden/news/behind-the-world-cup-record-pele")], data="29 giugno 1958")
    v("brasile-1970", "calcio", 1970, "La Coppa Rimet resta al Brasile",
      "Battendo l'Italia 4-1 in finale a Città del Messico, il Brasile vince il terzo Mondiale e tiene per sempre la Coppa Jules Rimet. Dal 1974 si gioca per un trofeo nuovo.",
      "Città del Messico", [f("Britannica", "Jules Rimet Trophy", "https://www.britannica.com/sports/Jules-Rimet-Trophy"),
                            f("FIFA", "The World Cup Trophy in numbers", "https://www.fifa.com/en/articles/world-cup-trophy-in-numbers-fifa-world-cup-qatar-2022")], data="21 giugno 1970")
    v("maradona-1986", "calcio", 1986, "Maradona e il «gol del secolo»",
      "Nei quarti del Mondiale messicano Diego Maradona segna all'Inghilterra il gol di mano e, quattro minuti dopo, quello partito da metà campo poi votato gol del secolo. L'Argentina vincerà il Mondiale.",
      "Città del Messico", [f("FIFA", "Diego Maradona spurs Argentina past England at Mexico 1986", "https://www.fifa.com/en/tournaments/mens/worldcup/articles/argentina-england-1986-diego-maradona"),
                            f("Britannica", "Diego Maradona", "https://www.britannica.com/biography/Diego-Maradona")], data="22 giugno 1986")
    v("laver-1969", "tennis", 1969, "Laver, il secondo Grande Slam",
      "L'australiano Rod Laver vince nello stesso anno Australian Open, Roland Garros, Wimbledon e US Open, come nel 1962. È l'unico ad averlo fatto due volte, e l'unico uomo nell'era Open.",
      "", [f("Britannica", "Rod Laver", "https://www.britannica.com/biography/Rod-Laver"),
           f("ATP Tour", "Grand Slams: Tournaments, Records, Stats", "https://www.atptour.com/en/news/grand-slams-tournaments-records-stats")])
    v("graf-1988", "tennis", 1988, "Graf, il Golden Slam",
      "Steffi Graf vince i quattro tornei del Grande Slam e poi l'oro olimpico a Seul, battendo in finale Gabriela Sabatini. È l'unica ad aver vinto tutto nello stesso anno.",
      "Seul", [f(OC, "Tennis' first Golden Slam winner: Steffi Graf", "https://www.olympics.com/en/news/tennis-golden-slam-steffi-graf-1988-olympics-gold"),
               f("Britannica", "Steffi Graf", "https://www.britannica.com/biography/Steffi-Graf")])
    v("tour-1903", "ciclismo", 1903, "Il primo Tour de France",
      "Il giornalista Henri Desgrange lancia il Tour de France per far vendere il suo giornale, L'Auto. Partono in 60, arrivano in 21: vince il francese Maurice Garin.",
      "Francia", [f("Britannica", "When was the Tour de France first held?", "https://www.britannica.com/sports/When-was-the-Tour-de-France-first-held"),
                  f("Britannica", "Tour de France winners", "https://www.britannica.com/sports/Tour-de-France-winners-2227411")])
    v("merckx-1969", "ciclismo", 1969, "Merckx vince il primo Tour",
      "Il belga Eddy Merckx vince il suo primo Tour de France; ne vincerà cinque (1969-72 e 1974), oltre a cinque Giri d'Italia e una Vuelta. In carriera conterà 445 vittorie.",
      "Francia", [f("Britannica", "Eddy Merckx", "https://www.britannica.com/biography/Eddy-Merckx")])
    v("hamilton-2020", "motori", 2020, "Hamilton, sette titoli come Schumacher",
      "Vincendo sotto la pioggia il Gran Premio di Turchia, Lewis Hamilton conquista il settimo titolo mondiale di Formula 1 ed eguaglia il record di Michael Schumacher.",
      "Istanbul", [f("Formula 1", "Hamilton seals historic 7th title in Turkey", "https://www.formula1.com/en/latest/article/hamilton-seals-historic-7th-title-with-peerless-wet-weather-victory-in.4wK1atemiXDvWXQxOknL4J")], data="15 novembre 2020")
    v("shiffrin-2023", "sci", 2023, "Shiffrin supera Stenmark",
      "Con lo slalom di Åre, in Svezia, Mikaela Shiffrin arriva a 87 vittorie in Coppa del Mondo e supera il record di Ingemar Stenmark, che durava da 34 anni.",
      "Åre (Svezia)", [f("FIS", "Unbelievable Shiffrin re-writes record books", "https://www.fis-ski.com/alpine-skiing/news/2022-23/unbelievable-shiffrin-re-writes-record-books-to-becomes-the-greatest"),
                       f(OC, "Mikaela Shiffrin sets new World Cup wins record in Are slalom", "https://www.olympics.com/en/news/mikaela-shiffrin-sets-new-world-cup-wins-record-are-slalom")], data="11 marzo 2023")
