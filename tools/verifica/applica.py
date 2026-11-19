# Applica un registro delle verifiche a data/atlante.json (riscrive il file, rientro 1 spazio come l'originale).
# Uso: python3 tools/verifica/applica.py data/atlante.json <registro.json> "<nota editoriale della versione>"
# Per ogni record: fonti specifiche (riusa quelle con lo stesso URL), toglie le fonti generali OpenStax
# (e l'elenco UNESCO generico se richiesto), applica le correzioni, stato «source-checked», nota con data ed esito, campo verified_on.
import json, re, sys, unicodedata, collections, datetime

path, reg, nota_versione = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(path).read()
d = json.loads(raw)
R = json.load(open(reg))
S = d['sources']
per_url = {s['url'].rstrip('/'): s for s in S if s.get('url')}
ids_fonti = {s['id'] for s in S}
voci = {x['id']: x for x in d['entities'] + d['events']}
GENERALI = {'src-openstax-world-history-1', 'src-openstax-world-history-2'}
LISTA = 'src-unesco-world-heritage-list'


def tipo(inst):
    i = inst.lower()
    if any(k in i for k in ('britannica', 'world history encyclopedia', 'stanford', 'te ara', 'ebsco', 'mactutor', 'encyclop')):
        return 'encyclopedia'
    if any(k in i for k in ('museum', 'smarthistory', 'met', 'museo')):
        return 'museum_or_educational'
    if any(k in i for k in ('nature', 'pnas', 'science', 'emerging infectious', 'archaeology', 'journal', 'antiquity')):
        return 'academic_article'
    if 'slavevoyages' in i:
        return 'research_database'
    if 'unesco' in i:
        return 'world_heritage_record'
    return 'institutional_document'


def slug(s):
    s = unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:48].strip('-')


def data_it(iso):
    a, m, g = iso.split('-')
    return f'{g}/{m}/{a}'


nuove, toccate = 0, collections.Counter()
for r in R:
    x = voci[r['id']]
    giorno = r.get('data') or datetime.date.today().isoformat()
    fonti = []
    for f in r['fonti']:
        u = f['url'].rstrip('/')
        if u in per_url:
            s = per_url[u]
        else:
            base = 'src-v-' + slug(f['institution'].split('(')[0] + ' ' + f['title'])
            sid, n = base, 2
            while sid in ids_fonti:
                sid, n = f'{base}-{n}', n + 1
            s = dict(id=sid, institution=f['institution'], title=f['title'], url=f['url'],
                     source_type=tipo(f['institution']), supports=[],
                     notes=f'Fonte specifica usata nella verifica del {data_it(giorno)}.')
            S.append(s); per_url[u] = s; ids_fonti.add(sid); nuove += 1
        fonti.append(s['id'])
    vecchie = [s for s in x.get('source_ids') or [] if s not in GENERALI]
    if r.get('sostituisci_unesco_lista'):
        vecchie = [s for s in vecchie if s != LISTA]
    x['source_ids'] = list(dict.fromkeys(fonti + vecchie))
    for k, v in (r.get('correzioni') or {}).items():
        if x.get(k) != v:
            toccate[k] += 1
        x[k] = v
    x['editorial_status'] = 'source-checked'
    nota = f'Verificata il {data_it(giorno)}: ' + r['nota']
    if r.get('parziale'):
        nota += ' Non verificato sulle fonti: ' + r['parziale']
    x['notes'] = nota
    x['verified_on'] = giorno

sup = collections.defaultdict(list)
for x in d['entities'] + d['events']:
    for s in x.get('source_ids') or []:
        sup[s].append(x['id'])
for s in S:
    s['supports'] = list(dict.fromkeys(sup.get(s['id'], []))) if s['id'] in sup else s.get('supports', [])
usate = set(sup)
for t in d.get('technologies', []):
    usate.update(t.get('source_ids') or [])
orfane = [s['id'] for s in S if s['id'] not in usate]

d['update_date'] = max(r.get('data') or '' for r in R) or d.get('update_date')
if nota_versione and nota_versione not in d['editorial_notes']:
    d['editorial_notes'].append(nota_versione)
json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
if raw.endswith('\n'):
    open(path, 'a').write('\n')
print('voci verificate', len(R), '· fonti nuove', nuove, '· correzioni', dict(toccate))
print('fonti senza voci collegate:', orfane)
print('stati', collections.Counter(x['editorial_status'] for x in d['entities'] + d['events']))
