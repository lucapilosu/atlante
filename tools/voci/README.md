# Voci nuove e posizioni

1. Scrivere le voci in un file JSON (esempio: `nuove_v068.json`), con dati, punto sulla mappa, fonti e nota di verifica.
2. `python3 tools/voci/inserisci.py data/atlante.json nuove tools/voci/nuove_vNNN.json` crea le voci (si ferma se un id esiste già o un collegamento punta a una voce inesistente).
3. `python3 tools/verifica/applica.py data/atlante.json tools/voci/nuove_vNNN.json "<nota>"` aggiunge le fonti e segna le voci come verificate.
4. Posizioni per voci esistenti: `python3 tools/voci/inserisci.py data/atlante.json posizioni tools/voci/posizioni_vNNN.json` (salta le voci che hanno già un punto).

Le coordinate delle posizioni sono punti di orientamento (`representative_anchor`) scelti da Claude: città o siti noti, non confini.

Precisione delle date: se il record non indica `date_precision`, un anno singolo con affidabilità alta diventa `year` (la scheda mostra l'anno senza «circa»); tutto il resto diventa `approximate` («circa»). Per un intervallo con estremi certi (es. 1545–1563) indicare `"date_precision": "range"`.
