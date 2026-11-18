# Registro delle versioni

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
