# Registro delle verifiche: un record per voce.
# Uso: python3 tools/verifica/v.py <registro.json> add '<lista json>'   |   python3 tools/verifica/v.py <registro.json> stato
# Record: {"id", "fonti":[{"institution","title","url"}], "nota", "data"?, "correzioni"?{campo:valore}, "parziale"?, "sostituisci_unesco_lista"?}
import json, sys, os, datetime
F = sys.argv[1]
R = json.load(open(F)) if os.path.exists(F) else []
if len(sys.argv) > 2 and sys.argv[2] == 'add':
    oggi = datetime.date.today().isoformat()
    for r in json.loads(sys.argv[3]):
        assert r.get('id') and r.get('fonti') and r.get('nota'), r
        r.setdefault('data', oggi)
        R = [x for x in R if x['id'] != r['id']] + [r]
    json.dump(R, open(F, 'w'), ensure_ascii=False, indent=1)
print(len(R), 'voci registrate; ultime:', ', '.join(x['id'].split('-', 1)[1][:20] + ('*' if x.get('correzioni') else '') for x in R[-10:]))
