# Inserisce voci nuove e posizioni sulla mappa in data/atlante.json (rientro 1 spazio come l'originale).
# Uso:
#   python3 tools/voci/inserisci.py data/atlante.json nuove <file.json>
#       ogni record: tipo (entity|event), id, name, start_year, end_year, date_confidence, summary,
#       region, subregion, lat, lon, label, layer, relevance, world_area, entity_type o event_type,
#       place_name (eventi), related (id collegati). I campi fonti/nota/parziale servono poi ad
#       applica.py (tools/verifica), che aggiunge le fonti e segna la voce come verificata.
#   python3 tools/voci/inserisci.py data/atlante.json posizioni <file.json>
#       ogni record: id, lat, lon, label. Aggiunge un punto solo alle voci che non ne hanno.
import json, sys

path, modo, src = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(path).read()
d = json.loads(raw)
R = json.load(open(src))
voci = {x['id']: x for x in d['entities'] + d['events']}
NOTA_MAPPA = 'Punto rappresentativo per orientamento; non indica confini o distribuzione territoriale.'


def punto(r):
    return {'type': 'point', 'latitude': r['lat'], 'longitude': r['lon'], 'label': r['label'],
            'precision': 'representative_anchor'}


if modo == 'nuove':
    ids_nuovi = {r['id'] for r in R}
    errori = [r['id'] for r in R if r['id'] in voci]
    errori += [f"{r['id']} → {i}" for r in R for i in r.get('related', []) if i not in voci and i not in ids_nuovi]
    if errori:
        sys.exit('id già presenti o collegamenti inesistenti: ' + ', '.join(errori))
    for r in R:
        assert r['start_year'] <= r['end_year'] and 0 not in (r['start_year'], r['end_year']), r['id']
        v = dict(id=r['id'], name=r['name'], start_year=r['start_year'], end_year=r['end_year'],
                 date_precision='approximate', date_confidence=r['date_confidence'], summary=r['summary'],
                 region=r['region'], subregion=r['subregion'], map_geometry=punto(r), source_ids=[],
                 editorial_status='research-seed', layer=r['layer'], relevance=r['relevance'],
                 world_area=r['world_area'])
        if r['tipo'] == 'entity':
            v.update(entity_type=r['entity_type'], related_entities=list(r.get('related', [])),
                     key_sites=[], map_note=NOTA_MAPPA)
            d['entities'].append(v)
        else:
            v.update(event_type=r['event_type'], place_name=r.get('place_name') or r['subregion'],
                     related_entity_ids=list(r.get('related', [])))
            d['events'].append(v)
    print('voci nuove', len(R), '· totale', len(d['entities']) + len(d['events']))
elif modo == 'posizioni':
    fatte = 0
    for r in R:
        x = voci[r['id']]
        if x.get('map_geometry'):
            print('ha già una posizione, saltata:', r['id'])
            continue
        x['map_geometry'] = punto(r)
        x.setdefault('map_note', NOTA_MAPPA)
        fatte += 1
    senza = sum(1 for x in d['entities'] + d['events'] if not x.get('map_geometry'))
    print('posizioni aggiunte', fatte, '· voci ancora senza posizione', senza)
else:
    sys.exit('modo sconosciuto: ' + modo)

json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
if raw.endswith('\n'):
    open(path, 'a').write('\n')
