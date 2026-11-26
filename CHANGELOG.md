# Registro delle versioni

## Pilu Sports Almanac v0.3 · 26 novembre 2026

- **Nuova grafica «Figurine»** in due stili, scelti da Luca: **Notte** (predefinito) e **Pastello**, con il pulsante «Stile» come nell'Atlante; la scelta resta salvata sul dispositivo. Tessere con bordo del colore dello sport, anno in un'etichetta in alto a destra, bandierina in alto a sinistra.
- **Favicon a medaglia** (disegno originale; i cerchi olimpici sono un simbolo protetto del CIO).
- **Bandierina al posto dell'evidenziazione verde** negli albi d'oro: segna l'Italia accanto al nome, senza colorare la riga.
- **Ricerca con filtri**: cosa (tessere, albi d'oro, atleti), paese, sport, competizione (Olimpiadi, Mondiali, Europei, campionati), risultato (oro, argento, bronzo), anni, genere. Sul telefono i filtri stanno in una riga «Filtri» che si apre e mostra il riepilogo. Con paese o risultato scelti, la medaglia corrispondente è messa in evidenza.
- **Ricerca per atleta** (100 atleti, anche con altri nomi: «Yuri Chechi», «Mondo Duplantis», «Djokovic»): porta a una **vista filtrata** con solo gli sport dell'atleta (Kiraly: pallavolo e beach volley), medaglie sull'asse degli anni (piene da atleta, tratteggiate da allenatore) e la scheda del palmarès divisa tra «da atleta» e «da allenatore». 398 voci del palmarès portano alla riga giusta dell'albo d'oro («albo →»); ogni collegamento è controllato. Gli atleti si scaricano solo quando servono (circa 17 kB compressi).
- **Albo d'oro olimpico dell'atletica**: 100, 200, 400, 5000, 10.000 m, maratona, staffette 4×100 e 4×400, salti in alto, con l'asta e in lungo, uomini e donne, più la 4×400 mista (490 righe; in tutto 1.248). Scelta per genere e poi per gara; pari merito e medaglie non assegnate annotati (Sydney 2000, oro dei 100 m donne non riassegnato).
- **Telefono**: la scheda si chiude tirandola giù, come nell'Atlante. Per aggiornare la pagina si tira giù la **barra in alto** (il gesto nativo non può funzionare perché il trascinamento muove il mosaico); in più, quando torni sulla pagina e c'è una versione nuova compare l'avviso «Aggiorna».
- Giba, titolo inglese 2018-19: verificato sulla CEV, fonte aggiunta.
- Prove: 101 controlli su PC e iPhone emulato (erano 57).

## Pilu Sports Almanac v0.2.1 · 26 novembre 2026

- **Più mondo, meno Italia:** 22 tessere nuove con risultati e record non italiani (Owens 1936, Bannister 1954, Bikila 1960, Beamon 1968, Kipchoge 2019, Comăneci 1976, Spitz 1972, Phelps 2008, Chamberlain 1962, Dream Team 1992, LeBron 2023, Cuba 2000, May-Treanor e Walsh 2012, Pelé 1958, Brasile 1970, Maradona 1986, Laver 1969, Graf 1988, primo Tour 1903, Merckx 1969, Hamilton 2020, Shiffrin 2023), ognuna con fonte (olympics.com, FIFA, NBA, FIVB, FIS, Formula 1, ATP, Britannica). Le tessere italiane passano dal 37% al 26%.
- Nuova colonna **Ginnastica** (pittogramma originale con due anelli dell'attrezzo).
- Preparati (non ancora visibili) i palmarès di 100 atleti per la ricerca per atleta della v0.3: `sport/data/atleti.json`, generato da `sport/tools/atleti.py`.

## Pilu Sports Almanac v0.2 · 26 novembre 2026

- **Pagina di ricerca** (pulsante «Cerca», tasto `/`, indirizzo `#cerca=…`): cerca in tessere e albi d'oro per squadra, nazione, atleta, città o anno, anche combinati («Italia 1982») e senza accenti («peru» trova Perù). Filtri per sport e per tipo (tessere / albi d'oro). Toccando un risultato si apre la tessera o l'albo giusto con la riga evidenziata.
- **Nuovi albi d'oro** (676 righe in più, 758 in tutto), con più competizioni per sport e un selettore in alto nella scheda:
  - Calcio: Mondiali uomini (1930–2026) e donne (1991–2023), Europei (1960–2024), Scudetto (1898–2025-26, con titoli revocati e non assegnati annotati).
  - Basket: Mondiali uomini e donne, Europei uomini e donne, finali NBA (1947–2026).
  - Pallavolo: Mondiali e Europei uomini e donne, Scudetto maschile (SuperLega) e femminile (Serie A1) dal 1946.
  - Beach volley: Mondiali uomini e donne (1997–2025).
- Trascrizione dalle tabelle di Wikipedia a revisione fissata, con controllo d'integrità SHA-256 per ciascuna delle 17 tabelle; i risultati del 2025-2026 riscontrati su fonti ufficiali o giornalistiche (FIFA, NBA, Inter, Lega Pallavolo, CEV, FIVB, Al Jazeera, Il Post).
- Indirizzi condivisibili anche per competizione e riga (`#sport=basket&g=nba&r=2026`).
- Prove: 57 controlli su PC e iPhone emulato (erano 27).

## Pilu Sports Almanac v0.1 · 26 novembre 2026

- Nuova pagina `sport/` (lucapilosu.github.io/atlante/sport/), senza copertina, scelta di Luca: si apre direttamente sul mosaico degli sport.
- Titolo «Pilu Sports Almanac 1896–2026»: l'anno finale viene dai dati e si aggiornerà da solo con i risultati degli anni successivi.
- 11 colonne (Olimpiadi e mondo, basket, pallavolo, beach volley, atletica, calcio, ciclismo, tennis, motori, sci, nuoto) e 52 tessere con fonti verificate (CIO, IPC, FIBA, FIVB, World Athletics, FIFA, FA, Giro d'Italia, Coppa Davis, FIS, World Aquatics, F1, ACO, Britannica). Fascia «Prima del 1896» in fondo. Bandierina tricolore sulle tessere italiane.
- Albi d'oro olimpici di basket, pallavolo e beach volley, uomini e donne (82 edizioni), con l'Italia evidenziata.
- Scheda con testo, fonti e note di verifica; indirizzi condivisibili (`#voce=…`, `#sport=…`, `#albi`).
- Il Tour de France non c'è: la ricerca delle fonti è stata rifiutata due volte dal servizio di ricerca e non è stato possibile verificarlo.

## v0.76 · 26 novembre 2026

- **Foto per le 31 voci della v0.75**: 66 foto da Wikimedia Commons, tutte le voci nuove ne hanno almeno una. In tutto **567 voci su 580** hanno foto (1.468 foto); restano senza le stesse 13 di prima.
  - Stesse regole delle versioni precedenti: niente fotografie di persone riconoscibili, niente immagini crude. Per guerre, genocidi e carestie ci sono memoriali, edifici, mezzi, documenti e banconote d'epoca (per esempio Tsitsernakaberd per il genocidio armeno, la lapide di Almaty per la carestia kazaka, le banconote d'occupazione giapponesi, il monumento Tortura Nunca Mais di Recife per la dittatura brasiliana).
  - Scelte di Claude da far vedere a Luca: per la Rivoluzione dei garofani c'è solo il ponte 25 de Abril (le foto del 1974 mostrano persone da vicino); per la guerra d'Etiopia l'obelisco di Axum portato a Roma nel 1937; per il Sessantotto le scritte situazioniste e una folla vista dall'alto; per la sentenza Mabo un acquerello del 1845 dell'isola di Mer e la sede dell'Alta Corte; per la guerra del Chaco un carro Vickers dello stesso modello (collegamento indiretto).
  - Selezione in `tools/foto/v073/selezione_grezza_v076.txt` (SHA-256 `db7c4b97…012d`, identico a quello calcolato nel browser); nessun nome è un reindirizzamento.
- Controlli sul sito pubblicato (26 novembre, dal browser integrato): la v0.75 è online con 580 voci e tutte le 68 foto della v0.74 si caricano. Copie della v0.74 e della v0.75 salvate su OneDrive.

## v0.75 · 25 novembre 2026

- **31 voci nuove di storia contemporanea, secondo blocco**, tutte con fonti specifiche e punto sulla mappa. Totale **580 voci**.
  - Mondo (4): epidemia di AIDS (dal 1981, in corso), conferenza di Bretton Woods, il Sessantotto, nascita dell'Organizzazione mondiale del commercio.
  - Europa (3): Chernobyl, Solidarność, Rivoluzione dei garofani.
  - Africa (4): guerra d'Etiopia, indipendenza di Angola e Mozambico, guerre del Congo (1996–2003), la Libia di Gheddafi.
  - Asia occidentale (3): genocidio armeno, accordo Sykes-Picot e mandati, guerra dei sei giorni.
  - Asia meridionale (2): guerra civile in Sri Lanka, disastro di Bhopal.
  - Asia orientale (4): Corea sotto il dominio giapponese, Lunga marcia, Grande balzo in avanti, seconda guerra sino-giapponese.
  - Asia centrale (3): rivoluzione mongola, carestia in Kazakistan, indipendenza delle repubbliche dell'Asia centrale.
  - Sud-est asiatico (4): occupazione giapponese, indipendenza della Birmania, indipendenza di Timor Est, crisi finanziaria asiatica.
  - Americhe (3): indipendenza di Giamaica e Trinidad e Tobago, guerra del Chaco, dittatura militare in Brasile.
  - Oceania (1): sentenza Mabo.
- La Dichiarazione universale dei diritti umani, prevista nel piano, è stata sostituita dall'OMC perché è già trattata nella voce sull'ONU.
- Fonti: Britannica per quasi tutte (126 fonti); UNAIDS per l'AIDS, sito dell'OMC per l'OMC. Dove le fonti non concordano il testo lo dice o usa una formula prudente: morti del Grande balzo («decine di milioni»: Britannica riporta stime da 6–7 a 45 milioni), date della carestia kazaka (date_confidence media), vittime del genocidio armeno (da 600.000 a oltre un milione). Le frasi di sintesi di Claude sono segnalate nella nota di verifica.
- **Senza foto per ora**: il PC non era collegato, quindi le foto delle 31 voci nuove vanno raccolte alla prossima sessione con il PC acceso (servono il browser integrato e wikidata.org).

## v0.74 · 25 novembre 2026

- **31 voci nuove di storia contemporanea** (richiesta di Luca: infoltire gli eventi più recenti), tutte con fonti specifiche, punto sulla mappa e foto. Totale **549 voci**.
  - Mondo (4): Società delle Nazioni, crisi petrolifera del 1973, crisi finanziaria del 2007–2008, smartphone.
  - Europa (3): Primavera di Praga, guerre nella ex Jugoslavia (1991–1999), guerra russo-ucraina (dal 2014, in corso).
  - Africa (4): indipendenza del Congo e crisi congolese, rivolta Mau Mau e indipendenza del Kenya, guerra del Biafra, rivoluzione egiziana e Nasser.
  - Asia occidentale (3): guerra Iran-Iraq, guerra del Golfo, guerra civile siriana (2011–2024).
  - Asia meridionale (2): questione del Kashmir, riforme economiche indiane del 1991.
  - Asia orientale (3): guerra russo-giapponese, proteste di piazza Tiananmen, Hong Kong torna alla Cina.
  - Asia centrale (3): prosciugamento del lago d’Aral, poligono nucleare di Semipalatinsk, guerra in Afghanistan (2001–2021).
  - Sud-est asiatico (4): rivoluzione filippina, indipendenza della Malesia e nascita di Singapore, People Power nelle Filippine, tsunami dell’Oceano Indiano.
  - Americhe (4): Nunavut, rivoluzione sandinista, guerra delle Falkland, il «No» a Pinochet.
  - Oceania (1): nascita del Commonwealth d’Australia.
- Scelta delle voci di Claude, con criterio di equilibrio: l'Europa pesa il 10% del blocco (contro il 20% dell'atlante); Asia centrale e Sud-est asiatico, le aree con meno voci, ne ricevono 3 e 4.
- Fonti: soprattutto Britannica; Nazioni Unite e CTBTO per Semipalatinsk; Archivi nazionali e Parlamento australiano per la federazione; The Canadian Encyclopedia per il Nunavut; Al Jazeera (13 novembre 2026) per lo stato della guerra in Ucraina. Le frasi che non vengono dalle fonti citate (ad esempio «potenze nucleari» per il Kashmir, le cifre arrotondate sui profughi) sono segnalate nella nota di verifica.
- Date «in corso»: guerra russo-ucraina, questione del Kashmir e lago d'Aral finiscono al 2026. La guerra civile siriana si ferma al 2024 (caduta di Assad), anche se Britannica la considera ancora in corso: è scritto nella nota.
- **Foto**: 68 foto per 29 voci nuove, con le stesse regole delle versioni precedenti (niente fotografie di persone riconoscibili, niente immagini crude: per le guerre mezzi, edifici distrutti, monumenti e memoriali). Restano senza foto le riforme indiane del 1991 e la rivoluzione sandinista (c'erano solo ritratti, grafici, bandiere o mappe). In tutto 536 voci su 549 hanno foto (1.402 foto). Selezione controllata con SHA-256 `df371a78…ac6f`; nomi dei file controllati contro i reindirizzamenti di Commons.

## v0.73 · 25 novembre 2026

- **Foto per 107 voci che non ne avevano** (269 foto nuove da Wikimedia Commons): ora hanno foto 507 voci su 518 (1.334 foto in tutto). Restano senza foto 11 voci per cui non c'era niente di adatto (solo mappe, schemi o ritratti fotografici): migrazioni bantu, Nora, Watson Brake, doppia elica del DNA, quattro eventi di Rapa Nui (paesaggio agricolo, incursioni schiaviste, annessione al Cile, studio genomico 2024), Organizzazione dell'unità africana, eradicazione della malaria in Sardegna, editto delle chiudende.
  - Candidate dalle pagine Wikipedia (inglese e italiana) collegate a ogni voce e dall'immagine di Wikidata; solo JPEG/PNG di almeno 500×300 px con autore e licenza; visualizzazioni degli ultimi 12 mesi come criterio di ordine. Tutte le miniature viste a occhio.
  - Stesse regole della v0.54: niente mappe, stemmi, schemi; niente fotografie di persone reali riconoscibili (restano dipinti, sculture, monete, francobolli, banconote); niente immagini violente. Eccezione da confermare con Luca: per le epidemie nelle Americhe c'è la tavola del Codice fiorentino che raffigura i malati di vaiolo (disegno del Cinquecento).
  - Per la missione cattolica di Rapa Nui si usa la chiesa di Hanga Roa; per i Vespri, il Sacco di Roma e simili, dipinti e incisioni d'epoca o dell'Ottocento.
  - Strumenti e selezione in `tools/foto/v073/` (raccolta dal browser integrato, testo trascritto e controllato con SHA-256 `ec2eecb1…b7ae`). Tutte le 269 miniature controllate sul sito pubblicato: due nomi erano reindirizzamenti e sono stati corretti.
- **Mosaico: comparsa delle foto più discreta** (scelta B di Luca). Prima ogni tessera che rientrava nel riquadro scivolava dall'angolo in alto a sinistra in 0,28 s, a ogni passaggio avanti e indietro. Ora la tessera compare al suo posto e sfuma in 0,2 s solo la prima volta; tornando su una zona già vista è già lì, ferma. Se la foto arriva dopo la cornice, sfuma dentro la cornice. «Riduci movimento» spegne tutto.
- **Tecnologia, Sintesi come «linea dell'epoca»** (scelta B di Luca):
  - asse degli anni vero al posto della scala logaritmica: lineare dall'inizio dell'epoca della voce alla sua fine; con «+ epoche precedenti» la stessa scala a tratti della barra del tempo;
  - una riga per ambito con tutte le attestazioni (non più solo la prima per area), all'anno in cui compaiono, con una linea per la durata e il nome breve accanto quando c'è spazio;
  - un tocco su un punto apre un riquadro sotto il grafico (nome, data, luogo, riassunto, «Apri la scheda» se c'è una voce collegata, «Vedi nel dettaglio»): il grafico resta;
  - toccando un'area nella legenda si evidenziano solo i suoi punti; toccando il nome di un ambito si apre il Dettaglio di quell'ambito.
- Test: 129 controlli; T34 riscritto per la nuova Sintesi; nuovo T66 (tessere del Mosaico che sfumano al loro posto, solo la prima volta).

## v0.72 · 24 novembre 2026

- **«Storia di questo luogo» solo in Esplora.** Nel riepilogo di un punto sulla mappa il collegamento compariva anche in Contemporanei, dove non apriva nulla (segnalazione di Luca). Ora c'è solo in Esplora; dalle altre viste «Apri scheda» porta comunque in Esplora.
- **Barra del tempo più facile da usare con il dito** (telefono e tablet, richiesta di Luca):
  - zona sensibile invisibile alta 49 px invece di 20, che sale anche sopra il numero dell'anno senza coprire i tasti − + e i pulsanti delle epoche;
  - finché il dito è appoggiato il cursore diventa grande (30 px con alone), così si vede di averlo preso;
  - toccare un punto qualsiasi della barra «prende» il cursore ma non fa saltare all'anno toccato: l'anno cambia solo trascinando, di quanto si sposta il dito.
  - Su PC la barra resta com'era.
- Il pulsante «Vedi nel Mosaico» proposto nella v0.69 non si fa (Luca: il Mosaico resta una vista a sé). I simboli della barra in basso restano quelli della v0.69.
- Test: 127 controlli; nuovo T65 (collegamento solo in Esplora; su iPhone emulato zona sensibile, cursore grande col dito giù, nessun salto al tocco, trascinamento che cambia l'anno).

## v0.71 · 23 novembre 2026

- **31 voci nuove su tecnologie e idee** (direzione C), tutte con fonti specifiche e punto sulla mappa. Totale **518 voci**.
  - Tecnologie (20): ruota, alfabeto, prime monete in Lidia, calcestruzzo romano e Pantheon, bronzi di Igbo-Ukwu, khipu inca, chinampas azteche, porcellana bianca e blu di Jingdezhen, Jantar Mantar di Jaipur, occhiali, pila di Volta, telegrafo senza fili di Marconi, primo volo dei Wright, penicillina, Sputnik, eradicazione del vaiolo, Euclide, Canone di Avicenna, Liber abaci di Fibonacci, relatività di Einstein.
  - Persone e idee (11): Socrate, Platone e Aristotele; zoroastrismo; Nalanda; esami imperiali cinesi; Carta del Manden a Kurukan Fuga; Muqaddima di Ibn Khaldun; Il Principe di Machiavelli; Las Casas e la disputa di Valladolid; Dei delitti e delle pene di Beccaria; José Rizal; voto alle donne in Nuova Zelanda.
- Per area: Europa 11, Asia occidentale 5, due ciascuna per Nord Africa, Africa subsahariana, Asia meridionale e Asia orientale, una ciascuna per Asia centrale, Sud-est asiatico, America settentrionale, Mesoamerica, America meridionale, Oceania e Globale. L'Europa pesa più che nel resto dell'atlante (35% contro 20%).
- Fonti principali: Britannica, Treccani, UNESCO (patrimonio mondiale e immateriale), British Museum, Metropolitan Museum, Smithsonian (Museo degli indiani d'America e dell'aria e dello spazio), National Park Service, NASA, ESA, OMS, CDC, Fondazione Nobel, Museo Galileo, MacTutor, Encyclopaedia Iranica, American Chemical Society, American Physical Society, FAO, NZHistory e Te Ara.
- Datazione «discussa» per lo zoroastrismo (le fonti mettono Zarathustra tra il 1500 e il 600 a.C.); affidabilità media dove le fonti danno solo secoli o date in disaccordo (ruota, alfabeto, monete, Igbo-Ukwu, Jantar Mantar, occhiali, Avicenna, Kurukan Fuga, Muqaddima e altre). Le date scelte da Claude sono segnate nella nota di verifica (inizio delle chinampas al 1325, degli esami imperiali al 618, Kurukan Fuga al 1235).
- Le voci nuove non hanno ancora foto (icona del tipo nel Mosaico e nelle schede).
- Test: 125 controlli; T53 conta 17 datazioni discusse (si aggiunge lo zoroastrismo).

## v0.70 · 23 novembre 2026

- **27 voci nuove sui luoghi che Luca conosce** (direzione B, «approfondimenti»), tutte con fonti specifiche e punto sulla mappa. Totale **487 voci**.
  - Sardegna (7): tombe dei giganti, giudicati sardi, conquista aragonese (1323–1410), Regno di Sardegna dei Savoia (1720–1861), editto delle chiudende, Brigata «Sassari» nella Grande Guerra, Grazia Deledda premio Nobel 1926.
  - Maya (7): El Mirador, scrittura maya, codici maya e Codice di Dresda, Tulum, Popol Vuh, fondazione di Mérida sulla città maya di T’hó (1542), boom dell’henequén nello Yucatán.
  - Rapa Nui (3): l'isola affittata come allevamento di pecore (1895–1953), Ley Pascua e cittadinanza cilena (1966), il parco affidato alla comunità Ma’u Henua (2017).
  - Italia (10): Ravenna e i mosaici, san Benedetto a Montecassino, Federico II e la corte di Sicilia, Vespri siciliani, Divina Commedia, Repubblica di Venezia, Sacco di Roma (1527), Concilio di Trento, Resistenza e Liberazione, miracolo economico.
- Fonti principali: Britannica, Treccani, UNESCO, INAH e governo messicano, Memoria Chilena e Biblioteca del Congreso Nacional del Cile, Regione Sardegna e Sardegna Cultura, Esercito italiano, Fondazione Nobel, SLUB di Dresda, Library of Congress, Senato. Datazione «discussa» per i codici maya (l'età del Codice di Dresda è dibattuta); affidabilità media per 9 voci con date ricavate da fasi archeologiche, da periodizzazioni o dalla tradizione.
- Sintesi rese più prudenti dove le fonti non bastavano: fine dei giudicati al 1410 (non 1420), fronti della Brigata «Sassari» indicati con le fonti (Isonzo, Carso, Grappa), Deledda senza «prima italiana a vincerlo».
- Date: gli eventi di un solo anno con affidabilità alta (Deledda, Mérida, Ley Pascua, Ma’u Henua, Sacco di Roma) mostrano l'anno senza «circa», come le altre 70 voci dello stesso tipo; gli intervalli con estremi certi (es. Concilio di Trento) usano la precisione «intervallo». Lo strumento `tools/voci/inserisci.py` ora lo fa da solo per gli anni singoli.
- Le voci nuove non hanno ancora foto (icona del tipo nel Mosaico e nelle schede).
- Test: 125 controlli; T53 conta 16 datazioni discusse (si aggiungono i codici maya).

## v0.69 · 23 novembre 2026

- **Mosaico in primo piano** (richiesta di Luca): su telefono e tablet ha un tasto proprio nella barra in basso, al secondo posto dopo Esplora (prima stava in «Altro»); su PC la scheda «Mosaico» è passata al secondo posto nella barra in alto.
- **Simboli nuovi nella barra in basso**, disegnati (SVG) al posto dei caratteri tipografici: globo (Esplora), tessere di mosaico (Mosaico), fasce di una linea del tempo (Contemporanei), ruota (Tecnologia), pianeta con orbita (Universo), tre puntini (Altro). Il tasto attivo ha uno sfondo a pillola. Funzionano con i tre stili perché prendono il colore del testo. Scelte di Claude, da confermare con Luca.
- In «Altro» restano Archivio e Confronto, con simboli disegnati anche lì (scatola d'archivio, bilancia).
- Con sei tasti la larghezza di ognuno segue la lunghezza del nome, così «Contemporanei» entra anche su schermi stretti (provato a 360, 375, 390 px e su iPad); sotto i 380 px il testo scende a 10 px.
- Test: 125 controlli; T64 controlla il tasto del Mosaico in basso e in alto, che non sia più in «Altro» e che ogni tasto abbia simbolo ed etichetta.

## v0.68 · 23 novembre 2026

- **23 voci nuove dove nel tempo non c'era nessuna voce attiva** (scelta di Luca: direzione A, «buchi nel tempo»). Cina: Liangzhu, Longshan, Erlitou, Sanxingdui. Steppe e Asia centrale: Yamnaya, civiltà dell'Oxus, Andronovo. Asia meridionale: Dholavira. Africa: regno di Kerma, Lothagam North, domesticazione del miglio perlato. Nord America: Watson Brake, Adena, Hohokam, L'Anse aux Meadows, migrazione dei Thule. Sud America: Valdivia, Kotosh. Sud-est asiatico e Oceania: espansione austronesiana, Tonga e Samoa, popolamento della Polinesia orientale, Budj Bim (prima voce sull'Australia aborigena prima del 1788). Globale: siccità di 4200 anni fa (inizio del Meghalayano). Totale **460 voci**.
- Ogni voce nuova entra già con fonti specifiche (UNESCO, Britannica, Met, Museum of Fine Arts di Boston, National Park Service, Parks Canada, Canadian Encyclopedia, Te Ara, governo australiano e della Louisiana, Ohio History Connection, Commissione internazionale di stratigrafia, articoli di Nature, PNAS, Scientific Reports) e posizione sulla mappa. Dove le fonti non concordano la nota lo dice; datazione «discussa» per l'espansione austronesiana e il popolamento della Polinesia orientale.
- Effetto: le finestre di 250 anni senza nessuna voce, contate area per area dal 3500 a.C., scendono **da 55 a 19**. Restano vuote Mesoamerica 3500–2250 a.C., Nord America 2750–2000 a.C., Africa subsahariana 3250–3000 e 2250–1750 a.C. e buona parte di Globale tra 2750 e 1500 a.C.
- **Mappa: 26 voci esistenti hanno ora un punto** (Pompei, Costantinopoli, Ravenna per la fine dell'Impero d'Occidente, Medina, Baghdad, Luoyang per Cai Lun, Tenochtitlan, Cusco, Norimberga per il De revolutionibus, Londra per Royal Society, Principia e Origine delle specie, San Pietroburgo, Cambridge, 12 voci di Rapa Nui con Rano Raraku e Orongo). Restano senza punto 10 voci diffuse (religioni, Via della Seta, industrializzazione, bussola, polvere da sparo, stampa).
- Le voci nuove non hanno ancora foto: nel Mosaico e nelle schede mostrano l'icona del tipo. Le foto si raccolgono dal browser dell'app desktop.
- Nuovo strumento `tools/voci/inserisci.py` (voci nuove e posizioni); le fonti si aggiungono con `tools/verifica/applica.py` sullo stesso file.
- Test: 125 controlli; T53 prende il totale delle voci dai dati e conta 15 datazioni discusse.

## v0.67 · 23 novembre 2026

- **Verifica, blocco 3b: le ultime 33 voci di rilevanza 3** con fonti specifiche: Asia (Botai, osservatorio di Ulugh Beg, khanato di Bukhara, ossa oracolari Shang, guerra sino-giapponese, editti di Ashoka, Congresso nazionale indiano, stampa Song, Bangladesh, Isfahan, ASEAN, Ban Chiang), Africa e Medio Oriente (Nabta Playa, Egitto predinastico, Numidia, reggenze barbaresche, Suez, Gerico, Giovani Turchi, OPEC, Ounjougou, Unione africana), Americhe (Calakmul, Uxmal, Toltechi, Mayapán, Purépecha, Haudenosaunee, St. Augustine, Nuova Amsterdam, corsa all'oro, Confederazione canadese) e gesuiti. Fonti principali: Britannica, UNESCO, INAH, National Park Service, Canadian Encyclopedia, siti ufficiali di OPEC, ASEAN e Unione africana, la rivista Antiquity. **Ora tutte le 437 voci hanno fonti specifiche** (423 verificate in questi blocchi, 14 con le fonti degli approfondimenti).
- Date corrette: ceramica di Ounjougou 10.000–9400 a.C. (prima 9400–9000; la fonte la dice anteriore al 9400); Uxmal dal 700 (prima 500; UNESCO: fondata verso il 700); Toltechi 850–1150 (prima 650–1200; Britannica, periodo d'importanza di Tula); corsa all'oro fino al 1859 (prima 1855). Datazione della Numidia segnata come sicura, quella della Confederazione Haudenosaunee come discussa (le fonti vanno dal 1142 al 1570–1600).
- Sintesi corrette: **ASEAN conta undici paesi, non dieci** (Timor Est è entrato il 26 ottobre 2025); la Confederazione canadese unì tre delle cinque colonie britanniche, non tutte; i Giovani Turchi costrinsero il sultano a ripristinare la costituzione ma non presero subito il potere; Ounjougou senza l'etichetta «cacciatori-raccoglitori», che la fonte non usa; corsa all'oro con il numero di arrivi (oltre 300.000).
- Mappa: nuovo punto per la Confederazione Haudenosaunee (regione dei Finger Lakes); ossa oracolari spostate ad Anyang (Yinxu) ed editti di Ashoka a Lumbini. Le voci senza posizione scendono a 36.
- Tolte fonti generiche (i due volumi OpenStax di storia mondiale e l'elenco UNESCO generico per Bukhara e Ban Chiang) e una fuori tema (la mostra sulla strada inca collegata agli editti di Ashoka).
- Test: 125 controlli; T63 ora controlla che nessuna voce, di qualunque rilevanza, sia senza fonti verificate; T53 conta 13 datazioni discusse (prima 12, si aggiunge Haudenosaunee).

## v0.66 · 23 novembre 2026

- **Verifica, blocco 3a: 33 voci di rilevanza 3** con fonti specifiche: le 18 voci dell'Oceania (Rapa Nui con UNESCO, Britannica, Met, Nature 2024, Scientific Reports 2024, Science 2006; viaggi di Tasman; indipendenze del Pacifico), le 9 della Sardegna e dell'Europa (domus de janas, Ozieri, Monte d'Accoddi, Su Nuraxi, Villanoviani, Tharros, conquista romana, macchina a vapore, referendum del 1946; fonti UNESCO, Ministero della Cultura, Regione Sardegna, Senato, Britannica) e le 6 dell'America meridionale (Paracas, Wari, Chimú, riduzioni gesuitiche, guerra del Paraguay, Brasília). Restano 33 voci, il blocco 3b.
- Correzioni: domus de janas fino al 2000 a.C. (UNESCO: dal V al III millennio a.C.; prima fino al 3000); torre di Su Nuraxi segnata come datazione approssimata. Nuovi punti sulla mappa per la torre di Su Nuraxi e la conquista romana della Sardegna.
- Dove le fonti non coprono una frase della voce, la nota lo dice (per esempio le date del culto dell'uomo-uccello, Ahu Nau Nau ad Anakena, il nome dell'accordo di annessione di Rapa Nui al Cile).
- Tolte fonti generiche o fuori tema: pagina turistica sul Perù, mostra sulla strada inca su Wari e Chimú, homepage del Quirinale, elenco UNESCO generico per riduzioni gesuitiche e Brasília.

## v0.65 · 23 novembre 2026

- **La «Tavola del tempo · prova» diventa «Il mosaico del tempo»** (nome scelto da Luca): «Mosaico» nella barra in alto su PC, «Il mosaico del tempo» in «Altro» su telefono e tablet e come titolo della pagina; tolto «prova». Nuovo indirizzo `#mosaico`; il vecchio `#tavola` funziona ancora.
- Test: 125 controlli (nuovo T64: nome, assenza di «prova», indirizzi nuovo e vecchio).

## v0.64 · 23 novembre 2026

- **Verificate le 41 voci di rilevanza 2 che non lo erano ancora** (blocco 2 della verifica), soprattutto con Britannica, World History Encyclopedia, Met, UNESCO e, per l'Italia, Senato e Camera. Ora sono verificate tutte le voci di rilevanza 1 e 2, tranne 5 che hanno già le fonti degli approfondimenti. Restano 66 voci di rilevanza 3.
- Date corrette: Chavín 900–200 a.C. (prima 1500–300; le fonti non concordano, affidabilità segnata come media); Olmechi dal 1200 a.C. (prima 1500); Aksum fino all'800 (prima 940); caratteri mobili in Asia orientale dal 1041, l'invenzione di Bi Sheng (prima 900); bussola dal 1044, prima menzione certa (prima 1000). Datazione segnata come sicura per sette voci: guerre persiane, Songhai, Safavidi, shogunato Tokugawa, Zheng He, Galileo, World Wide Web.
- **14 voci che non comparivano sulla mappa ora hanno un punto**: Aksum, Grande Zimbabwe, Gao (Songhai), Isfahan (Safavidi), Edo (Tokugawa), Timbuctù (commercio trans-sahariano), Niani (Mansa Musa), Baghdad (Casa della Sapienza), Calicut (Zheng He), Padova (Galileo), CERN (Web), Bandung, Luoyang (carta), arcipelago di Bismarck (Lapita). Altri tre punti spostati sul luogo che conta: Pataliputra (Gupta), Monte Albán (Zapotechi), Caral.
- Fonti sostituite o tolte: le pagine principali di Senato e Quirinale, sostituite da pagine specifiche; la scheda UNESCO di Teotihuacan collegata per errore ai Zapotechi; la mostra sulla strada inca collegata a Chavín; una fonte turistica su Caral.
- Sintesi corrette: Su Nuraxi (la torre è della seconda metà del II millennio a.C.) e stampa in Asia orientale.
- **«Qui vicino»** nel riepilogo di un punto elenca prima le voci nello stesso identico punto, poi quelle vicine (prima l'ordine era solo per importanza e data, e con i nuovi punti la dinastia Han finiva dietro «+4» quando si toccava Xi'an su telefono).
- Test: 123 controlli (T63 ora controlla anche le voci di rilevanza 2).

## v0.63 · 23 novembre 2026

- **Epoche scolastiche** (richiesta di Luca): Preistoria fino alla scrittura (circa 3500 a.C.), Antichità fino al 476, Medioevo 476–1492, Età moderna 1492–1789, Età contemporanea dal 1789. Prima erano 1250 a.C., 500, 1700 e 1963, per cui il 1600 risultava «Medioevo». Valgono ovunque si usano le epoche: barra del tempo, colore della mappa, Storia del luogo, finestra «stessa epoca» di Tecnologia, filtro dell'Archivio, fasce della Tavola, epoche evidenziate in Contemporanei.
- **Barra del tempo ridistribuita** secondo le voci di ogni epoca (pesi 14/22/20/17/27 al posto di 18/22/20/20/20): l'Età contemporanea, che ora comincia nel 1789 e ha 131 voci, prende più spazio, la Preistoria (23 voci) meno. Il Novecento occupa circa il 14% della barra (prima circa il 25%, quasi tutto dopo il 1963, dove le voci sono 26); l'Ottocento passa da circa l'8% a circa l'11%. Su telefono il pulsante della Preistoria si accorcia in «Preist.».
- I pulsanti − e + si fermano sui confini delle epoche (476, 1492 e 1789 non sono multipli del passo); il cursore raggiunge esattamente i confini.
- Una voce che finisce proprio su un confine non conta nell'epoca dopo (Roma, che finisce nel 476, è solo Antichità); un evento di un solo anno sta nell'epoca di quell'anno (la caduta di Granada del 1492 è Età moderna).
- Tavola: al massimo dello zoom su iPhone entrano 433 voci su 437 (prima 431); su PC tutte.
- Test: 123 controlli (T27, T44, T56 aggiornati ai nuovi confini; in T62 la foto da toccare si cerca in un'area più ampia).

## v0.62 · 23 novembre 2026

- **Verificate le 34 voci di rilevanza 1 che non lo erano ancora** (ora tutte quelle di rilevanza 1 hanno fonti specifiche, soprattutto Britannica, World History Encyclopedia, Imperial War Museums e Nazioni Unite). Restano da verificare 107 voci meno importanti (41 di rilevanza 2 e 66 di rilevanza 3), oltre alle 14 che hanno già le fonti degli approfondimenti.
- Correzioni di date: Antico Egitto dal 3100 a.C.; Maurya dal 321 a.C.; Rivoluzione scientifica 1543–1687 (Copernico → Principia di Newton), prima 1540–1700. Datazione segnata come sicura per dieci dinastie e periodi (Zhou, Achemenidi, campagne di Alessandro, Han, Abbasidi, Song, Ming, Moghul, Qing, Rivoluzione francese).
- **9 voci importanti che non comparivano sulla mappa di Esplora ora hanno il loro punto**: Bizantini (Costantinopoli), Song (Kaifeng), Mali (Niani), Ottomani (Istanbul), Moghul (Agra), Qing (Pechino), Buddha (Bodh Gaya), Confucio (Qufu), Gutenberg (Magonza). Altre 7 hanno il nome del luogo al posto di «punto di orientamento» (Pataliputra, Chang'an, Baghdad, Nanchino) e tre punti si spostano sul luogo che conta: Babilonia per Alessandro, Caffa per la peste nera, Varsavia per la seconda guerra mondiale.
- Tolte fonti fuori tema (per esempio una mostra sulla strada inca collegata al Buddhismo) e le fonti generiche iniziali dove ora ce ne sono di specifiche.
- **Icona del sito su iPad e iPhone**: oltre all'icona SVG dentro la pagina ci sono ora tre PNG (32 e 192 px, e 180 px per la schermata Home di iOS). Chrome su iPad mostrava l'icona vuota perché non usa le favicon SVG.
- Test: 123 controlli (nuovo T63: icone PNG presenti e della misura giusta, nessuna voce di rilevanza 1 senza verifica).

## v0.61 · 22 novembre 2026

- **Tavola del tempo: foto leggere.** Le mini foto usano la versione da 120 px di Wikimedia; da vicino, quando la foto è grande, passano a quella da 250 px (prima 330 px per tutte). Sono misure standard di Wikimedia. Le schede caricano le loro foto più grandi solo quando si aprono.
- **Tavola del tempo: dove siamo.** Colonne nell'ordine del planisfero, raggruppate per continente: Americhe · Europa · Africa · Asia · Oceania · Globale. In alto una barra colorata per continente (stessi colori delle cornici delle foto importanti); da lontano i sei nomi su due righe sfalsate, così entrano per intero anche sul telefono; da vicino si aggiungono i nomi delle aree. Quando si è ingranditi, al posto del suggerimento compare un piccolo planisfero (la mappa di Esplora, niente da scaricare) con le aree in vista evidenziate e i loro nomi.
- Ai bordi le foto restano dentro il riquadro solo nella vista d'insieme (da vicino si sovrapponevano alle vicine).
- Test: 121 controlli (T62 controlla anche continenti, planisfero e misura delle foto).

## v0.60 · 22 novembre 2026

- **Tavola del tempo (prova)**, nuova vista `#tavola` ispirata a Calculating Empires: una grande pagina da esplorare con lo zoom come una mappa. Colonne = 13 aree del mondo, tempo in verticale con oggi in alto (stessa scala a tratti della barra del tempo). Ogni voce è una mini foto (la prima di Wikimedia Commons, 330 px, caricata solo quando entra nel riquadro; icona della tipologia se manca): da lontano solo le più importanti, zoomando compaiono le altre e le foto crescono; quelle che non trovano posto restano come puntini, che si possono toccare. Un tocco su una foto apre la scheda dell’atlante sopra la tavola (su telefono la tendina, su PC un pannello a destra); la tavola porta in vista la voce scelta. Stile proprio, scuro.
- Gesti: trascinare (con inerzia), due dita, doppio tocco o doppio clic, rotella per scorrere nel tempo e Ctrl + rotella per lo zoom, frecce e + − 0 da tastiera; pulsanti −, + e «Tutta la storia».
- Dove si trova: scheda «Tavola · prova» in alto su PC, «Altro» → «Tavola del tempo · prova» su telefono e tablet.
- Copertura delle foto al massimo dello zoom: tutte le 437 voci su PC, 431 su iPhone (le altre 6 restano puntini da toccare).
- Corretta la posizione della tendina della scheda su telefono quando la barra del tempo è nascosta.
- Test: 121 controlli (nuovo T62).

## v0.59 · 22 novembre 2026

- **Contemporanei e Tecnologia senza voce scelta: torna la barra dell’anno.** Finché non si sceglie niente, in basso c’è la barra con l’anno e gli esempi («Nel 1630 d.C.: …») cambiano scorrendola; anche i punti della mappa di Contemporanei seguono l’anno. Appena si sceglie una voce la barra sparisce, come prima. Nuovo pulsante **«Scegli per anno»** nell’intestazione delle due viste: toglie la voce scelta (anche per le altre viste) e riporta la barra.
- **Tecnologia: di norma solo la stessa epoca.** Le attestazioni «prima» della voce si fermano all’inizio della sua epoca (le cinque della barra del tempo: Preistoria, Antichità, Medioevo, Età moderna, Età contemporanea), invece di risalire a migliaia di anni prima. Il pulsante **«+ epoche precedenti»** (accanto a «Stessa epoca») le aggiunge tutte per un confronto. Testi di intestazione, indicatori e note dicono quale finestra è attiva.
- Test: 119 controlli (nuovo T61; T26 e T34 verificano il confronto con tutte le epoche; T43 aggiornato: la barra è nascosta solo con una voce scelta).

## v0.58 · 21 novembre 2026

- **Storia del luogo a strati.** Le epoche sono disegnate come strati di uno scavo archeologico: in alto il più recente («Oggi · superficie»), in basso il più antico («Più antico · in profondità»), con colori della terra che si scuriscono in profondità. Restano al massimo 4 voci per strato, «+N altre», l’interruttore «Intorno all’anno» e la mappa con le sole voci del luogo.
- **Pulsante fisso «Storia di un luogo»** in alto a sinistra sulla mappa di Esplora: lo si tocca, poi si tocca un punto della mappa (Esc o un secondo tocco annullano). Il tieni premuto e il doppio clic restano. La frase sotto il titolo della mappa spiega i tre modi. Nessun fumetto.
- Test: 117 controlli (nuovo T60; T59 aggiornato all’ordine degli strati).

## v0.57 · 21 novembre 2026

- **Ottanio torna lo stile predefinito** (scuro, i colori caratteristici dell’Atlante), con Museo e Cartografo come alternative in Impostazioni → Aspetto. Contemporaneo morbido è tolto: chi lo aveva passa a Ottanio. Il tono della mappa per epoca vale anche in Ottanio.
- **Collegamenti solo a richiesta.** Aprendo una scheda non compaiono più archi. Il pulsante «Mostra i collegamenti · N» nella scheda li disegna e adatta la mappa perché tutti gli archi arrivino dentro il riquadro (prima un arco poteva uscire dal bordo senza arrivare alla voce). Su telefono la tendina si chiude per lasciare vedere la mappa; una barra sulla mappa riapre la scheda o nasconde i collegamenti. Toccando l’estremo di un arco si apre quella voce.
- **Contesto coerente tra le viste** (controllato con un giro automatico su tutte le viste):
  - Contemporanei e Tecnologia partono dalla voce scelta solo se la sua scheda è aperta o se la voce è attiva nell’anno della barra del tempo; altrimenti propongono le voci attive in quell’anno (prima restava la voce vecchia, per esempio Roma con l’anno al 1500). Anche gli esempi iniziali di Contemporanei vengono dall’anno.
  - Una voce scelta in Contemporanei o in Tecnologia vale per tutto l’atlante: se non è attiva nell’anno, l’anno si sposta come quando la si apre in Esplora, e tornando in Esplora si ritrova con la sua scheda.
  - La mappa di Esplora ritrova la sua inquadratura dopo un passaggio in Contemporanei (che la allarga per mostrare tutti i contemporanei).
  - Aggiungere o togliere voci dal confronto non cambia più la voce scelta in Esplora né l’inquadratura della mappa; l’area storica disegnata è sempre quella della voce scelta.
- **Storia di questo luogo (prototipo).** Tieni premuto un punto della mappa di Esplora (su PC doppio clic), oppure «Storia di questo luogo» nel riepilogo di un punto: nella scheda compaiono le voci la cui zona copre quel punto, divise per epoca (le stesse della barra del tempo), al massimo 4 per epoca scelte per importanza e vicinanza, le altre in «+N altre». Ogni riga ha una piccola linea del tempo. Interruttore «Tutte le epoche» / «Intorno all’anno» (± 50 anni). Sulla mappa restano accese solo le voci del pannello. Dalla scheda di una voce si torna con «← Storia del luogo». La zona di una voce è la sua area storica dove c’è (Roma, Maya, Cristianesimo, Buddhismo), altrimenti un cerchio con raggio per tipologia: siti 50 km, eventi e invenzioni 200, culture 300, movimenti 400, stati 700, religioni 800, dinastie e imperi 1.000. Valori provvisori, da tarare provando.
- Test di regressione: 115 controlli (T55 riscritto per i collegamenti a richiesta; nuovi T58 sulla coerenza tra le viste e T59 sulla storia del luogo; T10, T28 e T44 aggiornati).

## v0.56 · 21 novembre 2026

- **Tre stili al posto delle palette.** In Impostazioni → Aspetto si sceglie tra **Contemporaneo morbido** (predefinito: chiaro, testata ottanio, angoli morbidi), **Museo** (carta avorio, titoli e testi con grazie, etichette bronzo, filetti sottili) e **Cartografo** (toni da carta geografica, titoli in corsivo, reticolo tratteggiato, filo colorato dell’area sul bordo della scheda). Cambia solo l’aspetto, non la struttura. Tolte Ottanio profondo, Pergamena, Notte stellata e Terracotta: chi le aveva scelte passa a Contemporaneo morbido (Pergamena e Terracotta a Museo). Per ora non c’è uno stile scuro.
- **La scheda nasce dal punto della mappa.** Su PC si apre ingrandendosi dal punto toccato e ci torna quando si chiude; su telefono e tablet la tendina sale con un piccolo rimbalzo e scende alla chiusura. Il punto aperto pulsa due volte. Passando da una voce all’altra il contenuto cambia con una breve dissolvenza. Con «riduci movimento» attivo nel sistema non ci sono animazioni.
- **Fili verso le voci collegate.** Con la scheda aperta in Esplora, dalla voce partono archi verso le voci collegate che hanno una posizione sulla mappa (al massimo 14), disegnati con una breve animazione; spariscono alla chiusura. Esempio: Roma → Egitto, Cartagine, Etruschi, Nora, Su Nuraxi, Guerre puniche.
- **Icone per tipologia.** Sette icone (civiltà, regno/stato, sito, evento, religione, movimento, invenzione) nella scheda, nel riepilogo del punto e nei risultati della ricerca. Sulla mappa ogni punto porta una piccola forma per tipologia (triangolo, rombo, quadrato) e il punto aperto mostra l’icona piena; la legenda della mappa spiega le forme.
- **La mappa cambia tono con l’epoca.** Terre e mari prendono una sfumatura diversa per Preistoria, Antichità, Medioevo, Età moderna e Contemporanea (stessi confini della barra del tempo), con un passaggio graduale.
- Test di regressione: 111 controlli (T06, T10, T28 e T35 aggiornati ai nuovi stili; nuovi T54–T57 su icone, archi, tono d’epoca e animazione della scheda). Il file cresce di circa 16 KB.

## v0.55 · 21 novembre 2026

- **Scheda: semaforo della datazione.** Sotto il titolo restano due etichette invece di quattro: la data e un semaforo. La precisione entra nella data («circa 450 – 1500 d.C.» quando è approssimata; anno secco quando è esatta). Il semaforo unisce affidabilità e verifica delle fonti: verde «solida» (affidabilità alta e voce verificata su una fonte specifica, 210 voci), giallo «indicativa» (affidabilità media o voce non ancora verificata, 215), arancio «discussa» (12). Toccandolo si aprono i dettagli: affidabilità, precisione delle date, stato delle fonti e legenda. Scelta di Luca (proposta A).
- **Verificati 20 eventi con l’anno esatto** che avevano affidabilità media (Colombo 1492, Pompei 79, caduta di Tenochtitlan 1521, Muro di Berlino 1989…), con fonti specifiche, soprattutto Encyclopaedia Britannica. 17 passano ad affidabilità alta; 3 restano media perché la data è tradizionale o discussa: Qarawiyyin 859, Cai Lun 105, patto di Diriyah 1744 (alcune fonti dicono 1745). Per Pompei la nota segnala che il giorno (24 agosto o autunno) è discusso, l’anno no. 26 fonti nuove; registro in `tools/verifica/registro_v055_anni_esatti.json`.
- Test di regressione: 103 controlli (nuovo T53 sul semaforo).

## v0.54 · 20 novembre 2026

- **Foto più viste, con soggetti diversi.** Per ogni voce le candidate vengono dalle pagine di Wikipedia collegate (italiano, inglese, spagnolo, francese, tedesco) e dall’immagine della voce su Wikidata; per ciascuna si è letto quante volte è stata vista negli ultimi 12 mesi (novembre 2025 – ottobre 2026, statistiche Wikimedia). La prima foto è la più vista; la seconda e la terza sono le più viste di soggetto diverso, a meno che una foto dello stesso soggetto sia vista più di 10 volte tanto (criterio di Luca). Il soggetto si riconosce da ciò che la foto «raffigura» su Commons o dal nome del file, poi con un controllo a occhio. Esempio: Chichén Itzá ora ha El Castillo (circa 8,4 milioni di visualizzazioni in un anno), il campo del gioco della pelota e lo tzompantli; l’osservatorio non era tra le candidate.
- **Controllo di tutte le foto.** Viste tutte una per una e controllati i nomi dei file. Scartate: mappe e schemi; foto di altri soggetti con lo stesso nome (per esempio il gioco awalé per la cultura Wari); foto di persone reali riconoscibili, compresi i personaggi pubblici (restano dipinti, sculture, monete e francobolli); immagini violente o mediche.
- **Numeri.** 400 voci su 437 hanno foto (erano 381), 1.065 foto in tutto (erano 776): 522 confermate dalla v0.52, 543 nuove, 254 tolte (sostituite da foto più viste, oppure mappe, doppioni dello stesso soggetto e ritratti fotografici di personaggi pubblici come Karl Marx, Mao, Mussolini, Kennedy e Chruščëv). Sei voci restano senza foto perché tra le candidate c’erano solo ritratti o mappe: fondazione della Repubblica Popolare Cinese, Rivoluzione verde, Rivoluzione culturale, indipendenza dell’Indonesia, Rivoluzione cubana, Piano Condor. Il file cresce di circa 33 KB.
- Strumenti in `tools/foto/`: `diff_v054.txt` (la selezione), `applica_selezione.py` (la applica a `data/atlante.json`), `selezione_v054.tsv` (elenco completo).
- Test di regressione: 101 controlli, tutti superati.

## v0.53 · 20 novembre 2026

- **Ricerca da tastiera (PC).** Nella ricerca di Esplora le frecce ↑ ↓ ← → si muovono tra i risultati (disposti su due colonne), Invio apre la scheda, Esc chiude l’elenco; Invio senza frecce apre il primo risultato. Finché nessun risultato è evidenziato, ← e → spostano il cursore nel testo. ↑ ↓ e Invio funzionano anche nelle caselle di Contemporanei, Tecnologia e Confronto.
- **Ricerca ordinata per rilevanza.** Conta dove e come la parola compare nel nome della voce: nome identico, nome che inizia con la parola, parola intera, parte di parola; a parità vincono le voci più importanti e i nomi più corti. Esempio: «inca» → prima «Impero inca», non più «Conquista di Cusco…».
- **Contemporanei: la mappa mostra tutto.** Arrivando da una voce selezionata in Esplora la mappa restava ingrandita su quella zona (per Roma 33 punti visibili su 69). Ora si adatta a tutti i punti delle voci contemporanee (le 64 voci senza posizione, come religioni e movimenti, non possono comparire).
- **Contemporanei: vista Grafico.** Un unico grafico: in alto la voce principale, il suo periodo come fascia chiara che attraversa tutte le righe; sotto, per area, ogni voce con la sua durata intera (bordo dritto se continua oltre il grafico). Toccando una riga compaiono anni in comune, descrizione e azioni. Il pulsante «Elenco» riporta alla vista precedente; la scelta viene ricordata.
- **Apri la scheda** della voce di riferimento in Contemporanei e Tecnologia. In Tecnologia anche le attestazioni collegate a una voce hanno il pulsante: collegate altre 12 (Göbekli Tepe, Stonehenge, Nan Madol, Uruk, Gutenberg, Vinland, Mezzaluna fertile, Grecia neolitica, mais, Kuk, Dujiangyan, computo lungo), 29 su 38 in tutto.
- **Tecnologia, sintesi:** tolta la griglia «Ambiti attestati per area».
- **Confronto: sintesi prima della tabella.** Linea del tempo comune a tutte le voci, con la fascia del periodo in cui esistono tutte insieme, e frasi su sovrapposizioni (per ogni coppia: anni in comune o distanza) e collegamenti registrati.
- Test di regressione: 101 controlli (nuovi T48–T52).

## v0.52 · 20 novembre 2026

- **Foto nelle schede.** 381 voci su 437 hanno da 1 a 3 foto da Wikimedia Commons (776 in tutto), scelte una per una: monumenti, reperti, opere e documenti dell’epoca; niente mappe, stemmi o immagini poco significative (dove non c’era niente di adatto la scheda resta senza foto). Le foto si scaricano solo quando apri una scheda; nel file ci sono soltanto nome, autore e licenza (il file cresce di circa 90 KB). Sotto la galleria ci sono autore e licenza di ogni foto con il collegamento alla pagina di Commons; toccando una foto si ingrandisce, con le frecce per passare alle altre. Senza connessione le foto non si vedono, il resto funziona come prima.
- **Contemporanei: dove si colloca la voce.** Sotto il riepilogo, la durata della voce scelta è evidenziata sulle epoche della barra del tempo (stessa scala, non proporzionale). In cima alla lista c’è un righello con gli anni di inizio, di fine e qualche anno intermedio, allineato alle barrette delle righe; resta visibile mentre scorri la lista. Per scorrere nel tempo resta la vista Universo (scelta di Luca).
- **Universo: la rotella fa scorrere la pagina.** Su PC, con il puntatore sopra le linee temporali la rotella non faceva più scorrere la pagina: il riquadro tratteneva lo scorrimento verticale. Ora la pagina scorre; lo scorrimento orizzontale (trackpad) e Ctrl + rotella per lo zoom restano come prima.
- **Contemporanei: esempio «Han».** All’apertura gli esempi erano tre invece di quattro perché «Han» puntava a una voce inesistente; ora apre la dinastia Han.
- **Universo: filtri dei temi più pratici.** Prima stavano sotto le linee temporali: spegnendo o riaccendendo un tema il riquadro cambiava altezza e i pulsanti si spostavano, anche fuori schermo. Ora i temi sono in una barra sopra il riquadro, accanto a «Finestra», e restano fermi a ogni tocco. Nuovo pulsante «Tutti» per riaccenderli in un tocco. Su PC la barra con Finestra e Temi resta in alto mentre scorri le righe; su telefono e tablet no, per non togliere spazio.
- Test di regressione: 92 controlli (nuovi T44 Contemporanei, T45 rotella e T46 filtri dei temi nell’Universo, T47 foto nelle schede; T01 ora ammette come unica risorsa esterna le foto di Wikimedia Commons).

## v0.51 · 19 novembre 2026

- **Contemporanei senza barra del tempo.** La vista parte da una voce, non da un anno: spostare l’anno non cambiava niente (verificato da Claude e confermato da Luca). La barra ora è nascosta, come in Tecnologia e Confronto.
- **Verifica delle voci di rilevanza 2.** Le 176 voci di base con rilevanza 2 sono state controllate una per una su fonti specifiche, come le 86 di rilevanza 1 nella v0.50: soprattutto Encyclopaedia Britannica e World History Encyclopedia, poi schede UNESCO, ONU, OMS, CDC, National Park Service, Office of the Historian del Dipartimento di Stato, Archivi nazionali USA, Parlamento europeo, UNFCCC, Te Ara e NZHistory, Royal Museums Greenwich, Computer History Museum, National Security Archive e articoli scientifici. Il riferimento generale al manuale (e, in 30 voci, l’elenco UNESCO generico) è stato sostituito con 354 fonti nuove. Registro in `tools/verifica/registro_v051_rilevanza2.json`.
- **Correzioni (29 voci).** Date: Clovis 11.100–10.800 a.C.; Mehrgarh dal 5200 a.C. (datazione discussa); Chinchorro 5450–890 a.C.; Kuk dal 5000 a.C.; agricoltura in Europa dal 6500 a.C.; Hemudu fino al 3000 a.C.; Carnac fino al 3300 a.C.; Poverty Point 1750–1150 a.C.; Dong Son dal 500 a.C.; Yayoi fino al 250 d.C.; Tiwanaku fino al 1100; Ajanta fino al 550; Hopewell 1–400 d.C.; Chaco Canyon fino al 1250; Regno del Benin dal 1200; Dahomey 1625–1894; dominio della Compagnia dopo Plassey fino al 1858; Gran Colombia fino al 1830; Progetto Manhattan fino al 1947. Affidabilità: unificazione dell’Egitto approssimata, Tre Regni di Corea discussa; rivoluzione haitiana e guerre dell’oppio con date certe. Sintesi riscritte: Mehrgarh, Chinchorro, Kuk, Sintashta, La Tène, Ajanta, Silla unificata, Costituzione degli Stati Uniti («la più antica costituzione nazionale scritta ancora in vigore»), conquista russa dell’Asia centrale (Bukhara e Khiva protettorati, non annessi), Rivoluzione culturale (da mezzo milione a due milioni di morti invece di «milioni di vittime»).
- **Dettagli non verificati (26 voci).** Dove una parte della sintesi non compare nelle fonti consultate, la nota della voce lo dice (per esempio l’anno d’inizio 1242 dell’Orda d’Oro, il 1499 del sikhismo, Chan Santa Cruz nella Guerra delle Caste, «unico grande impero delle Americhe» per il Brasile).
- Strumenti della verifica delle voci spostati nel repository (`tools/verifica/`), con il registro della v0.50.

## v0.50 · 19 novembre 2026
- **Verifica delle voci principali.** Le 86 voci di base con rilevanza 1 (le più importanti a livello di manuale) sono state controllate una per una su fonti specifiche: Encyclopaedia Britannica, World History Encyclopedia, Metropolitan Museum, Smarthistory, UNESCO, ONU, OMS, Museo dell’Olocausto di Washington, archivi e servizi pubblici statunitensi, Te Ara, SlaveVoyages, articoli su Nature, PNAS e Science. Il riferimento generale al manuale è stato sostituito con 153 fonti nuove. Stato «Verificata su fonte specifica»; nella nota editoriale di ogni voce c’è cosa è stato confermato.
- **Correzioni.** Migrazioni bantu: fine al 1500 e datazione segnata come discussa. Unificazione Qin: fine al 207 a.C. Machu Picchu: fine al 1550 e tolta l’affermazione «mai raggiunta dagli spagnoli». Epidemie nelle Americhe: inizio al 1519. Shoah: 1933–1945 con la «soluzione finale» nel 1941–1945. Guerra del Vietnam: inizio al 1954. Magellano e rivoluzione Xinhai: sintesi riscritte su ciò che le fonti confermano.
- **Rimasti da verificare** su tre voci: i bacini idrici di Angkor, la fine formale del Regno del Kongo (1914) e la data di chiusura (1890) della voce sull’espansione verso ovest degli Stati Uniti; lo dice la nota della voce.
- **Tecnologia senza voce di partenza fissa.** Prima, se non si era scelto nulla, la vista partiva sempre da «Grande stagione degli ahu e dei moai». Ora resta vuota finché non si sceglie una voce; se una voce è già selezionata (in Esplora, sulla mappa, nell’Universo o in Contemporanei) si parte da quella, come prima. I suggerimenti sono le voci di rilevanza 1 attive nell’anno della barra del tempo, al massimo 6 e una per area finché ce n’è posto; se sono meno di 3 si aggiungono voci di rilevanza 2 e poi 3.
- **Anno di apertura vario.** Il sito sceglieva a caso un anno con 2–14 voci attive: con le 437 voci della v0.49 quasi tutti quegli anni (320 su 322) cadevano prima del 500 a.C., quindi si apriva quasi sempre nella preistoria. Ora sceglie a caso uno degli 8 periodi del piano dei contenuti e poi, al suo interno, un anno con almeno 3 voci di rilevanza 1 attive (almeno 2 nella preistoria, dove sono poche), mai lo stesso della volta prima.
- **Togliere dal confronto con lo stesso tasto.** «✓ Nel confronto» toccato di nuovo toglie la voce dal confronto: nel riepilogo della mappa (richiesta di Luca) e, per coerenza, nella scheda, in «Nel mondo intorno» e nel riepilogo dell’Universo. La voce resta selezionata e un avviso conferma «tolto dal confronto». Corretta anche l’etichetta della scheda, che per una voce già nel confronto mostrava «＋ Nel confronto».
- **Confronto senza barra del tempo.** Nella vista Confronto spostare l’anno non cambiava niente: il codice ereditato costruisce una «Linea del tempo comparativa» e un riquadro «Che cosa accadeva nel resto del mondo?» che userebbero l’anno, ma non li ha mai mostrati (dalla v0.43). La barra ora è nascosta, come in Tecnologia; l’anno resta quello di prima nelle altre viste. Mostrare quelle due parti resta un’idea da valutare più avanti.
- Test: 85 controlli (42 su desktop, 42 su iPhone 13 emulato, 1 su iPad emulato). T39 ora controlla anche che ogni voce verificata abbia una fonte specifica; nuovi T40 (Tecnologia senza voce scelta e suggerimenti per anno), T41 (anno di apertura su 800 aperture simulate), T42 (togliere dal confronto con lo stesso tasto) e T43 (barra del tempo per vista).

## v0.49 · 19 novembre 2026
- **Contenuti: base di storia mondiale bilanciata.** Da 176 a 437 voci (209 entità, 228 eventi), dal Neolitico (circa 11.000 a.C.) a oggi, distribuite su 13 aree del mondo e 8 periodi secondo il piano dei contenuti: 101 caselle su 104 hanno almeno una voce e la copertura rispetto agli obiettivi è 334 su 341. Restano vuote Sud-est asiatico prima del 3500 a.C. e Oceania tra 500 a.C. e 1000 d.C. (a livello di manuale le voci note sono paleolitiche o di datazione troppo incerta). Il Paleolitico è escluso di proposito.
- **Approfondimenti con fonti specifiche.** Sardegna (Mont’e Prama, pozzo di Santa Cristina, Nora, Carta de Logu, Sa die de sa Sardigna, eradicazione della malaria, Statuto speciale), Maya e Yucatán (dinastia di Copán, murales di Bonampak, auto da fé di Maní), Rapa Nui (Hoa Hakananai’a, spedizione Routledge), Italia (spedizione dei Mille, Costituzione). Le voci già presenti su questi luoghi sono marcate con il loro focus.
- **Fonti.** Ogni voce ora ha almeno una fonte. Le voci di base («Voce di base · fonte generale») hanno come riferimento il manuale aperto OpenStax World History (vol. 1 fino al 1450, vol. 2 dopo) e, dove il sito è Patrimonio UNESCO, la scheda o l’elenco UNESCO: sono sintesi di livello manuale, non confrontate riga per riga con le fonti. Le 38 voci che non avevano fonti ricevono lo stesso riferimento generale.
- **Pulizia.** Unite 27 voci doppie (per esempio «Dinastia Han» evento ed entità, le due Prime e Seconde guerre mondiali, Achemenidi, Inca, Mexica/Aztechi): fonti e collegamenti confluiscono nella voce tenuta. Aggiunte le aree mancanti alle voci di Rapa Nui e Su Nuraxi.
- **Campi nuovi nei dati.** `layer` (civiltà, eventi, tecnologie, persone e idee, luoghi), `relevance` (1 = centrale in un manuale, 3 = approfondimento), `world_area` (una delle 13 aree), `focus` (sardegna, maya, rapa-nui, europa). Servono alla futura linea del tempo a livelli; già ora l’Universo mostra per prime le voci con rilevanza 1 e sulla mappa queste stanno sopra le altre.
- **Mappa: «Qui vicino».** Quando più voci cadono nello stesso punto (per esempio Repubblica Italiana e Trattati di Roma), il riepilogo le elenca e un tocco porta all’altra voce.
- **Etichette leggibili.** Tipologie per religioni, movimenti e invenzioni; precisione, affidabilità e stato della voce in italiano nella scheda e nel confronto. La Preistoria va ora «fino al 1250 a.C.» e comprende anche le voci più antiche del 4000 a.C.
- `tools/copertura.py` stampa la copertura per area e periodo rispetto agli obiettivi.
- Test: 77 controlli (38 su desktop, 38 su iPhone 13 emulato, 1 su iPad emulato), con i nuovi su «Qui vicino» e sulla coerenza dei dati (fonte, livello, rilevanza e area per ogni voce, nessun collegamento rotto, nessun nome doppio).

## v0.48 · 19 novembre 2026
- **Mappa.** Il riepilogo di un punto si chiude anche toccando un altro punto vuoto della mappa, toccando fuori dalla mappa o con Esc, non solo con ×. Trascinare o ingrandire la mappa e usare la barra del tempo non lo chiudono.
- **Scheda a tendina.** Su telefono (e ora su tablet) la scheda si chiude trascinandola verso il basso, come su iPhone: dalla maniglia o dal contenuto quando è già in cima. Un tratto breve la rimette a posto, verso l’alto si allarga.
- **Tablet.** Su iPad e tablet le viste sono nella barra in basso come sul telefono, la barra del tempo sta sopra e la scheda è una tendina. Il riconoscimento si basa sullo schermo a tocco, non solo sulla larghezza.
- **Confronto subito raggiungibile.** Il Confronto ha una vista sua (scheda «Confronto» su desktop con il numero di voci, «Altro» su telefono e tablet). Ogni aggiunta mostra un avviso con «Vai al confronto»; anche «già nel confronto» e «confronto pieno» vengono segnalati.
- **Universo rifatto.** Una riga per area con i **nomi delle voci scritti** accanto alle barre, senza sovrapposizioni; le voci in eccesso finiscono in «+N altre» (un tocco le elenca). La finestra segue la barra del tempo (prima lo slider non aveva effetto): 100 anni, 500, 2.000 o Tutto; su telefono parte da 500 anni. Trascinando si esplora liberamente e compare «Torna all’anno»; due dita o Ctrl+rotella cambiano l’ampiezza. Tolti i comandi doppi (Centra, Vista completa, −/+), il grafico della densità e il riquadro delle categorie: i temi sono una legenda sotto il disegno che si tocca per filtrare. Il riepilogo di una voce porta alla scheda o al confronto.
- **Tecnologia: sintesi infografica.** Nuova vista iniziale «Sintesi» (l’elenco di prima è in «Dettaglio»): tre numeri chiave, un grafico con una riga per ambito e un punto per area nella prima attestazione nota, su scala logaritmica in «anni prima della voce», con la fascia «durante»; sotto, gli ambiti attestati per area. Un tocco su un punto apre la sua attestazione nel dettaglio.
- **Palette.** Dettagli del confronto leggibili in Pergamena e Terracotta (prima testo chiaro su fondo chiaro e riquadri scuri con testo scuro) e corretti anche in Notte stellata; testo secondario un po’ più scuro nelle palette chiare (contrasto ≥ 4,5:1).
- Test: 73 controlli (36 su desktop, 36 su iPhone 13 emulato, 1 su iPad emulato), con i nuovi su chiusura del riepilogo, gesto della tendina, avviso del confronto, Universo che segue l’anno ed etichette senza sovrapposizioni, sintesi Tecnologia, contrasto nelle quattro palette e tablet.

## v0.47 · 18 novembre 2026
- **Vista Tecnologia (nuova).** Si sceglie una voce (all'apertura: la stagione dei moai di Rapa Nui) e, per sette ambiti (architettura monumentale, metallurgia, scrittura e stampa, navigazione, agricoltura, astronomia e calendari, idraulica), si vede area per area la prima attestazione nota e le più recenti fino alla fine della voce, con la distanza in anni ("≈ 3700 anni prima") o "durante". Il confronto è per ambito, non su un'unica scala di progresso; un'area senza voci è segnalata come assenza nel dataset, non come assenza della capacità. Ogni attestazione si apre con riassunto, affidabilità della data, fonti e collegamenti alle voci dell'atlante. In questa vista la barra del tempo è nascosta, perché conta la voce scelta e non l'anno.
- **Dati.** 38 attestazioni con 38 fonti nuove (UNESCO, musei, articoli scientifici), segnate come "voce di partenza, da approfondire". `build.py` ora controlla anche le attestazioni (ambito, area, anni, fonti).
- **Barra del tempo a tratti.** Ogni epoca occupa sullo slider lo spazio del suo blocco (più spazio alle epoche recenti, più dense di voci). Pulsanti − e + con passo per epoca: 100 anni in preistoria, 10 in antichità, 5 nel medioevo, 1 in età moderna e contemporanea.
- **Universo più semplice.** Una corsia per area (Europa, Asia, Africa, Americhe, Oceania, Globale e altro), voci vicine raggruppate, collegamenti mostrati solo toccando una voce, legenda dei temi sopra il disegno.
- **Palette.** Ottanio profondo resta la principale; al posto delle quattro precedenti ci sono Pergamena, Notte stellata e Terracotta mediterranea.
- **Navigazione su telefono.** La barra in basso è Esplora · Contemporanei · Tecnologia · Universo · Altro; l'Archivio si apre da "Altro" (su desktop resta tra le schede in alto).
- **Codice.** Tolto il codice della vecchia timeline "Storie parallele" (funzioni, stili e controlli non più usati).
- Test: 58 controlli (29 per dispositivo), con i nuovi su vista Tecnologia, slider a tratti, palette e Universo.

## v0.46 · 18 novembre 2026
- **Scheda a comparsa.** In Esplora la scheda compare solo quando scegli una voce (dalla ricerca, dall'archivio, da "Apri scheda"); su desktop la mappa occupa tutta la larghezza finché non c'è una scheda. Su telefono la scheda è un pannello che sale dal basso, sopra la barra del tempo, lascia vedere la mappa, si allarga toccando la maniglia e si chiude con ×. Il semplice tocco su un punto della mappa apre il riepilogo, non la scheda.
- **Un solo comando per il tempo.** Le epoche sono nella barra in basso, sotto lo slider; tolto il riquadro dell'anno dalla pagina. "Reimposta" è in Impostazioni.
- **Vista Universo.** L'Universo storico ha una vista sua (scheda "Universo"), con il Confronto. Categorie e densità degli eventi sono in un riquadro richiudibile. "Storie parallele" è tolta dalla pagina (il codice verrà ripulito in seguito). Contemporanei ora contiene solo voce scelta, elenco e mappa.
- **Mappa più pulita.** Comandi di zoom piccoli sopra la mappa; su telefono resta solo "mondo intero" (lo zoom si fa con due dita). Legenda e note dentro "Livelli e filtri".
- **Mappa più definita e zoom fino a 40x.** Ingrandendo oltre 2,5x si carica la cartografia Natural Earth 1:50m (coste e confini molto più precisi, divisa in tasselli). Linee sottili a ogni ingrandimento (prima si ingrossavano con lo zoom) e punti della stessa misura su ogni schermo. Area di tocco dei punti più ampia sul telefono. Aperta dal disco senza connessione, la pagina resta con la cartografia semplice.
- Test: 50 controlli (25 per dispositivo), compresi scheda a comparsa, epoche nella barra, vista Universo, cartografia di dettaglio e comandi della mappa.

## v0.45 · 18 novembre 2026
**Struttura a viste.** La pagina unica è divisa in quattro viste, ognuna con il suo indirizzo: Esplora, Contemporanei, Archivio, Impostazioni. Anno, voce selezionata e confronto restano gli stessi passando da una vista all'altra. Su telefono la barra in basso porta alle viste; su desktop le schede sono in alto.
- Esplora: anno con le epoche, ricerca, mappa sempre aperta e scheda. Lo slider dell'anno è solo nella barra in basso (prima era doppio); l'elenco delle voci dell'anno è in un riquadro richiudibile.
- Contemporanei (nuova): si sceglie una voce e compaiono tutte le voci esistite per almeno una parte della sua durata, raggruppate per area, con gli anni in comune e una barra che mostra la sovrapposizione; la mappa mostra i loro luoghi. Ogni voce si apre per leggere il riassunto, vederla sulla mappa, metterla al centro o aprirne la scheda. Universo storico, storie parallele e confronto sono qui, in riquadri richiudibili.
- Archivio: elenco con ricerca e filtri propri (epoca, area, tipologia, solo voci attive nell'anno), copertura per epoca e fonti. Prima l'elenco dipendeva in modo nascosto dall'epoca scelta in alto e dalla ricerca principale.
- Impostazioni: palette dei colori.
- Tolto il pannello "mostra/nascondi sezioni"; un'eventuale scelta salvata in precedenza viene ignorata.
- Ricerca: scegliendo un risultato l'anno resta lo stesso se la voce esisteva già in quell'anno, altrimenti passa al suo periodo. La ricerca principale ora cerca sempre in tutto l'atlante e non cancella più la selezione mentre si scrive.
- Mappa: i filtri Civiltà e culture, Siti, Reti e idee funzionano, più un nuovo filtro Eventi; un filtro senza voci localizzate della sua tipologia viene nascosto (oggi "Reti e idee": religioni, movimenti e invenzioni non hanno ancora coordinate). I filtri sono raccolti in "Livelli e filtri". Tolto il menu "Punti", che non aveva effetto.
- Su telefono intestazione e pannelli più compatti: la mappa compare già nella prima schermata.
- Dati separati dal codice (`data/atlante.json`); `build.py` controlla i dati e costruisce la pagina, che resta un file unico.
- Test: 42 controlli (21 per dispositivo), compresi viste, Contemporanei, ricerca, filtri della mappa, archivio e larghezza delle viste.

## v0.44 · 18 novembre 2026
- Mappa: il pulsante "Apri scheda" nel popup era quasi invisibile (testo chiaro su fondo chiaro); ora è leggibile in tutte e cinque le palette.
- Mappa: il popup non copre più il punto toccato. Si apre sopra il punto se c'è spazio, altrimenti sotto; la freccia indica sempre il punto; evita la barra temporale e la navigazione in basso; segue il punto quando si scorre la pagina o si fa zoom sulla mappa. Prima, su iPhone, il riquadro della mappa lo ritagliava e lo spingeva sopra il punto.
- Timeline: su desktop la rotella scorre la finestra temporale anche quando il puntatore è sopra una barra (prima si fermava).
- Footer: indicava "versione 0.34"; ora la versione è allineata a titolo e intestazione.
- Aggiunti i test automatici di regressione (`tests/regression.py`), eseguiti su desktop e iPhone 13 emulato.

Difetto noto (corretto nella v0.45): i filtri della mappa "Civiltà e culture", "Siti" e "Reti e idee" non nascondevano alcun punto.

## v0.43 · 17 novembre 2026 (base ereditata)
Versione sviluppata con ChatGPT e consegnata con il pacchetto di handover. Alla scelta di un risultato di ricerca: campo svuotato, anteprima e tastiera chiuse, scheda aperta.
