# Atlante storico del mondo

Atlante storico interattivo: mappa, timeline e schede per esplorare che cosa accadeva nel mondo nello stesso periodo, dalla preistoria a oggi. Progetto personale, in fase di prototipo.

## Struttura
- `index.html`: l'applicazione, in un unico file (HTML, CSS, JavaScript e dati).
- `tests/regression.py`: test automatici dei comportamenti da non rompere.
- `CHANGELOG.md`: registro delle versioni.

## Test
Richiede Python 3, Playwright e Chrome.

```
python3 tests/regression.py <percorso>/index.html <cartella-screenshot>
```

Ogni controllo viene eseguito su desktop (1440×900) e su iPhone 13 emulato. "NOTO" indica un difetto conosciuto che non fa fallire l'esecuzione. La simulazione non sostituisce la prova su un telefono reale, soprattutto per i gesti.

## Note sui contenuti
Coordinate, aree e cronologie sono indicative: le aree storiche sono ricostruzioni approssimative, non confini certi, e diverse voci sono ancora da verificare sulle fonti.
