# Atlante storico del mondo

Atlante storico interattivo: mappa, timeline e schede per esplorare che cosa accadeva nel mondo nello stesso periodo, dalla preistoria a oggi. Progetto personale, in fase di prototipo.

Sito: https://lucapilosu.github.io/atlante/

## Viste
- `#esplora`: anno, ricerca, mappa e scheda.
- `#contemporanei`: scelta una voce, tutte le voci esistite per almeno una parte della sua durata, per area e sulla mappa.
- `#tecnologia`: scelta una voce, per ogni ambito tecnico e per area le attestazioni note fino a quel momento, con la distanza in anni (Sintesi infografica e Dettaglio).
- `#universo`: Universo storico, una riga per area, con la finestra che segue la barra del tempo.
- `#confronto`: confronto fino a 5 voci (caratteristiche, cronologie, relazioni).
- `#archivio`: elenco delle voci con filtri propri, copertura per epoca, fonti.
- `#impostazioni`: palette dei colori, reimpostazione.

## Struttura
- `src/atlante.html`: modello della pagina (HTML, CSS, JavaScript) con i segnaposto per dati e versione.
- `data/atlante.json`: voci, eventi, fonti, ambiti tecnici (`technology_domains`) e attestazioni tecniche (`technologies`).
- `data/mappa-dettaglio.json`: cartografia di dettaglio (Natural Earth 1:50m, dominio pubblico, tramite il pacchetto npm world-atlas), caricata dalla pagina quando si ingrandisce la mappa.
- `tools/cartografia_dettaglio.mjs`: rigenera `data/mappa-dettaglio.json`.
- `tools/copertura.py`: copertura dei contenuti per area del mondo e periodo, confrontata con gli obiettivi del piano.
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
I test avviano un piccolo server locale (la cartografia di dettaglio si carica con una richiesta di rete) e richiedono Python 3, Playwright e Chrome. Ogni controllo gira su desktop (1440×900) e su iPhone 13 emulato, più un controllo su iPad emulato; la simulazione non sostituisce la prova su un telefono reale, soprattutto per i gesti.

## Crediti
Cartografia: Natural Earth (dominio pubblico), via world-atlas di Mike Bostock (licenza ISC).

## Note sui contenuti
Coordinate, aree e cronologie sono indicative: le aree storiche sono ricostruzioni approssimative, non confini certi, e diverse voci sono ancora da verificare sulle fonti.

Dalla v0.49 l’atlante ha una base di storia mondiale bilanciata (13 aree, 8 periodi, dal Neolitico a oggi) e approfondimenti su Sardegna, Maya e Yucatán, Rapa Nui e Italia. Lo stato di ogni voce è nel campo `editorial_status`: `base-draft` indica una sintesi di livello manuale con un riferimento generale (OpenStax World History, ed eventualmente UNESCO), non verificata riga per riga; `deep-dive-sourced` indica una voce di approfondimento con fonti specifiche. Ogni voce ha anche `layer`, `relevance` (1–3), `world_area` e, se c’è, `focus`.
