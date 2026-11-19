# Registro delle versioni

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
