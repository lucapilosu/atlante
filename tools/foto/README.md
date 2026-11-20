# Foto delle schede (v0.52)

- Fonte: Wikimedia Commons. Nel file `data/atlante.json` ogni voce può avere il campo `images` (massimo 3): `f` nome del file su Commons, `h` le prime due cifre dell'MD5 del nome con `_` al posto degli spazi (servono a comporre l'indirizzo della miniatura), `a` autore, `l` licenza.
- La pagina carica le miniature a 330 px solo quando si apre la scheda; l'ingrandimento usa 960 px (o l'originale se è più piccolo).
- `selezione_v052.tsv`: elenco delle 776 foto scelte (voce | h | file | autore | licenza). Raccolta fatta il 20 novembre 2026 dal browser integrato dell'app desktop (Wikipedia/Wikidata/Commons non sono raggiungibili dall'ambiente di Claude): candidati dalle voci di Wikipedia collegate, scartate mappe, stemmi, schemi e immagini non significative, controllo visivo di tutte le miniature.
- Verifica rapida dei nomi: `python3 -c "import hashlib;[print(l) for l in open('tools/foto/selezione_v052.tsv') if hashlib.md5(l.split('|')[2].replace(' ','_').encode()).hexdigest()[:2]!=l.split('|')[1]]"` non deve stampare niente.
