# Pilu Sports Almanac

Pagina a parte dell'atlante, pubblicata in `lucapilosu.github.io/atlante/sport/`.

- `src/almanacco.html` modello (pagina, stile, codice), `data/almanacco.json` dati, `build.py` unisce i due in `index.html`.
- I dati si generano con `python3 sport/tools/dati.py` (tessere con fonti, albi d'oro olimpici); le note di verifica sono in `tools/note_fonti.md`.
- Il titolo «Pilu Sports Almanac 1896–AAAA» prende l'ultimo anno dai dati: aggiungendo una tessera o una riga d'albo del 2027 diventa da solo «1896–2027».
- Prove: `python3 tests/sport.py` (PC e iPhone emulato, 27 controlli).
- Grafica originale (nessuna ripresa della copertina dell'almanacco del film, scelta concordata con Luca il 26/11/2026).
