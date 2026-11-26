# Foto v0.73: voci senza foto

- `mappa.py` / `mappa.json`: pagine Wikipedia (en, it) e parole chiave per ognuna delle 118 voci senza foto; `mappa2.json` secondo giro per le voci rimaste vuote.
- `raccogli.js`: da eseguire nel browser integrato su una pagina di wikidata.org (`window.MAPPA_FILE` sceglie la mappa). Raccoglie le immagini delle pagine e l'immagine di Wikidata (P18), tiene JPEG/PNG di almeno 500×300 px con licenza, segna come pertinenti quelle con una parola chiave nel nome o che sono l'immagine principale, legge le visualizzazioni 11/2025–10/2026 (solo per le prime 12 di ogni voce) e lascia le prime 8 in `window.FOTO.cand`.
  - Attenzione: l'indirizzo restituito da `imageinfo` ha in coda `?utm_source=…`, che va tolto prima di chiedere le visualizzazioni (altrimenti tutte le richieste danno 404).
- `foglio.js`: `FOGLIO(da, a)` mostra le candidate come foglio di miniature per il controllo a occhio.
- Scelta a mano (Claude, 25 novembre 2026), stesse regole della v0.54. Risultato trascritto in `selezione_grezza_v073.txt` (gruppo|voce|file|autore|licenza|visualizzazioni; SHA-256 `ec2eecb182a8b2f99e0694bd4b54c6c682fa6057e260d21ff6f01b047d9ab7ae`, identico a quello calcolato nel browser), convertito in `selezione_v073.tsv`.
- `python3 tools/foto/v073/aggiungi.py tools/foto/v073/selezione_v073.tsv` aggiunge le foto solo alle voci che non ne hanno.
- Dopo la pubblicazione due nomi risultavano reindirizzamenti (miniature in 404) e sono stati sostituiti col nome vero del file: «Temple of Concordia, Agrigento BW 2012-10-07 13-09-13.jpg» e «P. Oxy. I 29.jpg». Per le prossime raccolte: chiedere `imageinfo` con `redirects=1` e usare il titolo restituito.

- **v0.76** (26 novembre 2026): foto per le 31 voci della v0.75. Mappe `mappa4.py`/`mappa4.json` e `mappa5.json` (secondo giro con pagine trovate con `opensearch`); raccolta dal ramo `foto-v076` (nel browser si sostituisce `/foto-v073/` con `/foto-v076/`); selezione in `selezione_grezza_v076.txt` (SHA-256 `db7c4b974d72fc2a2fdb51dad6cef110303d23b17b3cbb7cc2ee7d97dc7f012d`) e `selezione_v076.tsv`; titoli controllati con `redirects=1` su Commons prima della pubblicazione.
