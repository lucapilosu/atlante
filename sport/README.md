# Pilu Sports Almanac

Pagina a parte dell'atlante, pubblicata in `lucapilosu.github.io/atlante/sport/`.

- `src/almanacco.html` modello (pagina, stile, codice), `data/almanacco.json` dati, `build.py` unisce i due in `index.html`.
- I dati si generano con `python3 sport/tools/dati.py` (tessere con fonti, albi d'oro olimpici); le note di verifica sono in `tools/note_fonti.md`.
- Albi d'oro non olimpici (v0.2): `tools/albi_grezzi.txt` contiene le tabelle di Wikipedia così come estratte nel browser, una sezione per competizione; `tools/albi.py` controlla l'impronta SHA-256 di ogni sezione (se il testo cambia, la generazione si ferma) e traduce in italiano nazioni, sedi e punteggi. Per aggiornare una competizione: rigenerare la sezione dal browser, aggiornare l'impronta in `HASH`, rilanciare `dati.py`.
- Ricerca: indice costruito nella pagina da tessere e righe d'albo; parole in AND, inizio di parola, senza accenti.
- Il titolo «Pilu Sports Almanac 1896–AAAA» prende l'ultimo anno dai dati: aggiungendo una tessera o una riga d'albo del 2027 diventa da solo «1896–2027».
- Atleti (v0.3): `tools/atleti.py` → `data/atleti.json`; `build.py` lo copia compatto in `sport/atleti.json`, che la pagina scarica solo quando si apre la ricerca o un atleta (meno dati sul telefono). In `dati.py`: genere degli atleti e collegamenti palmarès → righe d'albo, controllati.
- Albi con podio di Giro, Tour, Formula 1 e Coppa del Mondo di sci (v0.5): `tools/altri/c0..c4.txt` + `tools/altri_albi.py`. Una tabella può dare i propri nomi di colonna (`colonne`) e la stagione (`stag`).
- Slam di tennis (era Open), nuoto e ginnastica olimpici (v0.6): `tools/altri/t_*.txt`, `n1`, `n2`, `g1` + `tools/albi_v06.py`. Con `colonne` di due nomi la tabella non ha il terzo posto (finali di tennis). In `dati.py`, `GARA_ALBO` traduce la gara del palmarès nel torneo dell'albo quando i nomi non coincidono; le voci più vecchie dell'inizio di un albo non vengono collegate.
- Albo olimpico dell'atletica (v0.3): `tools/atletica/a0..a5.txt` + `tools/albo_atletica.py`.
- Versione: `build.py` scrive `sport/versione.json` con l'impronta del contenuto; la pagina la ricontrolla quando torna in primo piano e propone «Aggiorna» se è cambiata.
- Stili Notte e Pastello (scelta salvata nel browser), favicon a medaglia (`favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`).
- Prove: `python3 tests/sport.py` (PC e iPhone emulato, 126 controlli; avvia da sé un piccolo server locale).
- Grafica originale (nessuna ripresa della copertina dell'almanacco del film, scelta concordata con Luca il 26/11/2026).
