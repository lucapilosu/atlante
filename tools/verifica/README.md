# Verifica delle voci

Registri delle verifiche delle voci di base su fonti specifiche, con gli script per applicarli ai dati.

- `registro_v050_rilevanza1.json`: le 86 voci con rilevanza 1, verificate il 19/11/2026 e già applicate nella v0.50.
- `registro_v051_rilevanza2.json`: le 176 voci con rilevanza 2, applicate nella v0.51.
- `registro_v055_anni_esatti.json`: i 20 eventi con anno esatto e affidabilità media, applicati nella v0.55.
- `registro_v062_altre.json`: le voci del pacchetto iniziale e degli ampliamenti non ancora verificate (141 al 23/11/2026), a blocchi per rilevanza; applicate dalla v0.62. Con almeno una fonte nuova, `applica.py` toglie anche le fonti generiche (CFR, corsi Open University, World History Project); il campo `togli` rimuove altre fonti fuori tema.
- `v.py <registro> add '<lista json>'`: aggiunge o sostituisce record. Campi: `id`, `fonti` [{institution, title, url}], `nota` (esito, in italiano), facoltativi `data` (ISO, predefinita oggi), `correzioni` {campo: valore}, `parziale` (dettagli non verificati), `sostituisci_unesco_lista`, `togli` [id fonti].
- `applica.py data/atlante.json <registro> "<nota editoriale>"`: applica il registro. Si può rilanciare: ogni volta riparte dallo stato attuale della voce.
- Avanzamento: `python3 tools/verifica/da_fare.py`.
