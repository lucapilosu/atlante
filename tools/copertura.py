"""Copertura dei contenuti per area del mondo e periodo (v0.49).

uso: python3 tools/copertura.py [data/atlante.json]

Conta le voci per area (campo world_area) e periodo (anno di inizio) e le confronta
con gli obiettivi del piano dei contenuti: H = 6, M = 4, L = 2, m = 1 voci per casella.
Le voci con focus (Sardegna, Maya, Rapa Nui, Europa) sono contate e anche indicate a parte.
"""
import json
import sys
from collections import Counter

AREE = ['EU', 'AO', 'AN', 'AS', 'AM', 'AE', 'AC', 'SE', 'NA', 'MC', 'SA', 'OC', 'GL']
PERIODI = [(-99999, -3500, 'fino al 3500 a.C.'), (-3500, -500, '3500–500 a.C.'), (-500, 500, '500 a.C.–500'),
           (500, 1000, '500–1000'), (1000, 1500, '1000–1500'), (1500, 1750, '1500–1750'),
           (1750, 1914, '1750–1914'), (1914, 99999, '1914–oggi')]
H, M, L, m = 6, 4, 2, 1
OBIETTIVI = {  # righe = periodi, colonne = aree nell'ordine AREE
    0: [L, M, L, M, m, L, m, m, m, m, m, m, L],
    1: [M, H, H, L, M, M, L, m, m, L, L, m, L],
    2: [H, M, L, L, H, H, L, L, m, M, L, m, M],
    3: [M, H, M, L, L, H, L, L, m, M, L, L, L],
    4: [H, M, L, M, L, H, M, L, L, M, M, L, M],
    5: [H, M, L, M, M, H, L, L, M, M, M, L, H],
    6: [H, L, L, M, M, H, L, L, H, M, M, L, H],
    7: [H, M, L, M, M, H, L, M, H, M, M, L, H],
}


def periodo(anno):
    return next(i for i, (a, b, _) in enumerate(PERIODI) if a <= anno < b)


def main():
    db = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'data/atlante.json'))
    voci = db['entities'] + db['events']
    nomi = {a['id']: a['name'] for a in db.get('world_areas', [])}
    senza = [v['id'] for v in voci if v.get('world_area') not in AREE]
    if senza:
        print('voci senza area mondiale:', ', '.join(senza))
    c = Counter((v.get('world_area'), periodo(v['start_year'])) for v in voci)
    f = Counter((v.get('world_area'), periodo(v['start_year'])) for v in voci if v.get('focus'))
    print(f"{'':26}" + ''.join(f'{i:>8}' for i in range(8)))
    for j, a in enumerate(AREE):
        print(f"{nomi.get(a, a):26}" + ''.join(f"{c[(a, p)]:>4}/{OBIETTIVI[p][j]:<3}" for p in range(8)))
    utile = sum(min(c[(a, p)], OBIETTIVI[p][j]) for p in range(8) for j, a in enumerate(AREE))
    totale = sum(sum(r) for r in OBIETTIVI.values())
    print(f'\nvoci {len(voci)} · di cui con focus {sum(1 for v in voci if v.get("focus"))}')
    print(f'copertura utile {utile} su {totale}')
    vuote = [(nomi.get(a, a), PERIODI[p][2]) for p in range(8) for a in AREE if c[(a, p)] == 0]
    sotto = [(nomi.get(a, a), PERIODI[p][2], c[(a, p)], OBIETTIVI[p][j]) for p in range(8) for j, a in enumerate(AREE)
             if 0 < c[(a, p)] < OBIETTIVI[p][j]]
    print('caselle vuote:', vuote or 'nessuna')
    print('sotto obiettivo:', sotto or 'nessuna')
    sopra = [(nomi.get(a, a), PERIODI[p][2], c[(a, p)], f[(a, p)]) for p in range(8) for j, a in enumerate(AREE)
             if c[(a, p)] - f[(a, p)] > OBIETTIVI[p][j] * 1.5 and c[(a, p)] - OBIETTIVI[p][j] >= 3]
    print('molto sopra obiettivo anche senza focus (voci, di cui focus):', sopra or 'nessuna')


if __name__ == '__main__':
    main()
