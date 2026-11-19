# Elenca le voci ancora da verificare (base-draft), per rilevanza, escludendo quelle già nel registro indicato.
# Uso: python3 tools/verifica/da_fare.py [registro.json] [rilevanza]
import json, sys, os
d = json.load(open(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'atlante.json')))
reg = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else []
fatte = {r['id'] for r in reg}
liv = int(sys.argv[2]) if len(sys.argv) > 2 else 2
L = sorted((x for x in d['entities'] + d['events'] if x.get('editorial_status') == 'base-draft' and x.get('relevance') == liv), key=lambda x: x['start_year'])
resta = [x for x in L if x['id'] not in fatte]
print(f'rilevanza {liv}: {len(L)} da verificare all’inizio, {len(L) - len(resta)} nel registro, {len(resta)} restanti')
