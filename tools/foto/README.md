# Foto delle schede (v0.52, aggiornate nella v0.54)

- Fonte: Wikimedia Commons. Nel file `data/atlante.json` ogni voce può avere il campo `images` (massimo 3): `f` nome del file su Commons, `h` le prime due cifre dell'MD5 del nome con `_` al posto degli spazi (servono a comporre l'indirizzo della miniatura), `a` autore, `l` licenza.
- La pagina carica le miniature a 330 px solo quando si apre la scheda; l'ingrandimento usa 960 px (o l'originale se è più piccolo).
- `selezione_v052.tsv`: elenco delle 776 foto scelte (voce | h | file | autore | licenza). Raccolta fatta il 20 novembre 2026 dal browser integrato dell'app desktop (Wikipedia/Wikidata/Commons non sono raggiungibili dall'ambiente di Claude): candidati dalle voci di Wikipedia collegate, scartate mappe, stemmi, schemi e immagini non significative, controllo visivo di tutte le miniature.
- Verifica rapida dei nomi: `python3 -c "import hashlib;[print(l) for l in open('tools/foto/selezione_v052.tsv') if hashlib.md5(l.split('|')[2].replace(' ','_').encode()).hexdigest()[:2]!=l.split('|')[1]]"` non deve stampare niente.

## v0.54: foto più viste

- Candidate: immagini delle pagine di Wikipedia collegate a ogni voce (it, en, es, fr, de) e immagine della voce su Wikidata (P18); tenute solo JPEG/PNG di almeno 500×300 px con autore e licenza; al massimo 12 per voce.
- Popolarità: visualizzazioni del file negli ultimi 12 mesi (novembre 2025 – ottobre 2026) dall’API Wikimedia `metrics/mediarequests/per-file/all-referers/user/…/monthly/20251101/20261031`, somma del campo `requests`.
- Scelta: prima la foto più vista; poi, due volte, la più vista di soggetto diverso da quelle già scelte, salvo che la più vista dello stesso soggetto abbia più di 10 volte le visualizzazioni. Soggetto: proprietà «raffigura» (P180) dei dati strutturati di Commons quando c’è, altrimenti parole del nome del file (tolte quelle del nome della voce).
- Una candidata vale per la voce solo se era già tra le foto della voce, oppure «raffigura» la voce, oppure il nome del file contiene una parola del nome della voce (in una delle cinque lingue).
- Controllo: tutte le foto viste a occhio e tutti i nomi letti. Scartate mappe e schemi, soggetti sbagliati, foto di persone reali riconoscibili (anche personaggi pubblici), immagini violente o mediche, doppioni dello stesso soggetto.
- Raccolta e calcolo fatti dal browser integrato dell’app desktop (Wikimedia non è raggiungibile dall’ambiente di Claude); risultato trascritto in `diff_v054.txt` e controllato con SHA-256 (`04b47c7c…e342`).
- `python3 tools/foto/applica_selezione.py tools/foto/diff_v054.txt tools/foto/selezione_v054.tsv` applica la selezione a `data/atlante.json`, pulisce i nomi degli autori come nella v0.52 («Autore sconosciuto», «Vedi Wikimedia Commons» per i crediti lunghi) e controlla che il campo `h` corrisponda al nome del file. Va applicato ai dati della v0.53 (le righe `voce|=N` indicano la N-esima foto che la voce aveva prima).
