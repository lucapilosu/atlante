# Verifica delle voci

Registri delle verifiche delle voci di base su fonti specifiche, con gli script per applicarli ai dati.

- `registro_v050_rilevanza1.json`: le 86 voci con rilevanza 1, verificate il 19/11/2026 e già applicate nella v0.50.
- `registro_v051_rilevanza2.json`: le 176 voci con rilevanza 2, applicate nella v0.51.
- `registro_v055_anni_esatti.json`: i 20 eventi con anno esatto e affidabilità media, applicati nella v0.55.
- `registro_v062_altre.json`: blocco 1, le 34 voci di rilevanza 1 non ancora verificate (v0.62).
- `registro_v064_rel2.json`: blocco 2, le 41 voci di rilevanza 2 non ancora verificate (v0.64).
- `registro_v066_rel3a.json`: blocco 3a, 33 voci di rilevanza 3 (Oceania e Rapa Nui, Sardegna ed Europa, America meridionale) (v0.66). Il campo `parziale` segnala le affermazioni della voce non coperte dalle fonti lette.
- `registro_v067_rel3b.json`: blocco 3b, le ultime 33 voci di rilevanza 3 (Asia, Africa e Medio Oriente, Americhe) (v0.67). Con questo blocco tutte le voci hanno fonti specifiche.
- Prima dei due blocchi le voci non verificate erano 141 (23/11/2026). Con almeno una fonte nuova, `applica.py` toglie anche le fonti generiche (CFR, corsi Open University, World History Project); il campo `togli` rimuove altre fonti fuori tema.
- `v.py <registro> add '<lista json>'`: aggiunge o sostituisce record. Campi: `id`, `fonti` [{institution, title, url}], `nota` (esito, in italiano), facoltativi `data` (ISO, predefinita oggi), `correzioni` {campo: valore}, `parziale` (dettagli non verificati), `sostituisci_unesco_lista`, `togli` [id fonti].
- `applica.py data/atlante.json <registro> "<nota editoriale>"`: applica il registro. Si può rilanciare: ogni volta riparte dallo stato attuale della voce.
- Avanzamento: `python3 tools/verifica/da_fare.py`.
- `../voci/nuove_v068.json`: 23 voci nuove della v0.68; lo stesso file serve a `tools/voci/inserisci.py` (crea le voci) e ad `applica.py` (fonti e nota).
