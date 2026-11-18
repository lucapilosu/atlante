# Atlante storico del mondo

Atlante storico interattivo: mappa, timeline e schede per esplorare che cosa accadeva nel mondo nello stesso periodo, dalla preistoria a oggi. Progetto personale, in fase di prototipo.

Sito: https://lucapilosu.github.io/atlante/

## Viste
- `#esplora`: anno, ricerca, mappa e scheda.
- `#contemporanei`: scelta una voce, tutte le voci esistite per almeno una parte della sua durata, per area e sulla mappa; più Universo storico, storie parallele e confronto.
- `#archivio`: elenco delle voci con filtri propri, copertura per epoca, fonti.
- `#impostazioni`: palette dei colori.

## Struttura
- `src/atlante.html`: modello della pagina (HTML, CSS, JavaScript) con i segnaposto per dati e versione.
- `data/atlante.json`: voci, eventi e fonti.
- `versione.json`: numero di versione e data mostrati nella pagina.
- `build.py`: controlla i dati e costruisce `index.html`, un file unico che si apre anche senza connessione.
- `index.html`: la pagina pubblicata (generata: non modificarla a mano).
- `tests/regression.py`: test automatici dei comportamenti da non rompere.
- `CHANGELOG.md`: registro delle versioni.

## Costruire e verificare
```
python3 build.py
python3 tests/regression.py "$PWD/index.html" <cartella-screenshot>
```
I test richiedono Python 3, Playwright e Chrome. Ogni controllo gira su desktop (1440×900) e su iPhone 13 emulato; la simulazione non sostituisce la prova su un telefono reale, soprattutto per i gesti.

## Note sui contenuti
Coordinate, aree e cronologie sono indicative: le aree storiche sono ricostruzioni approssimative, non confini certi, e diverse voci sono ancora da verificare sulle fonti.
