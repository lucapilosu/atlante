# Verifica delle voci

Registri delle verifiche delle voci di base su fonti specifiche, con gli script per applicarli ai dati.

- `registro_v050_rilevanza1.json`: le 86 voci con rilevanza 1, verificate il 19/11/2026 e già applicate nella v0.50.
- `registro_v051_rilevanza2.json`: le voci con rilevanza 2 (in corso).
- `v.py <registro> add '<lista json>'`: aggiunge o sostituisce record. Campi: `id`, `fonti` [{institution, title, url}], `nota` (esito, in italiano), facoltativi `data` (ISO, predefinita oggi), `correzioni` {campo: valore}, `parziale` (dettagli non verificati), `sostituisci_unesco_lista`.
- `applica.py data/atlante.json <registro> "<nota editoriale>"`: applica il registro. Si può rilanciare: ogni volta riparte dallo stato attuale della voce.
- Avanzamento: `python3 tools/verifica/da_fare.py`.
