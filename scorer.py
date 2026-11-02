"""채점: 테마 30 + 필수/금지 20 + PC 성능 20 + 시너지 20 + 예산 10 = 100점."""
from common import ITEMS, PARTS

PC_TYPES = ['CPU', 'GPU', 'RAM', 'PSU', 'CASE']
STAR_CUTS = [(90, 3), (75, 2), (60, 1)]


def pc_stats(pc):
    """pc: {type: part_id} -> (성능 점수, 소비전력, 파워 용량, 성능 별)"""
    perf = sum(PARTS[pid].get('perf', 0) for pid in pc.values())
    watt = sum(PARTS[pid].get('watt', 0) for pid in pc.values())
    cap = PARTS[pc['PSU']]['capacity'] if 'PSU' in pc else 0
    stars = 3 if perf >= 19 else 2 if perf >= 12 else 1 if perf >= 6 else 0
    return perf, watt, cap, stars


def boot_status(pc):
    if any(t not in pc for t in PC_TYPES):
        return 'missing'
    _, watt, cap, _ = pc_stats(pc)
    return 'ok' if watt <= cap else 'power'


def synergies(placed, pc):
    ids = [p['id'] for p in placed]
    tags = [t for i in ids for t in ITEMS[i]['tags']]
    case = pc.get('CASE')
    found = []

    def adjacent(a, b):
        return a['layer'] == b['layer'] and (
            a['slot'] + ITEMS[a['id']]['size'] == b['slot'] or b['slot'] + ITEMS[b['id']]['size'] == a['slot'])

    lamps = [p for p in placed if p['id'] in ('lamp_warm', 'lamp_cool')]
    books = [p for p in placed if p['id'] == 'book']
    if any(adjacent(l, b) for l in lamps for b in books):
        found.append('독서 콤보')
    if tags.count('plant') >= 3:
        found.append('플랜테리어')
    if case == 'case3' and 'rgb_bar' in ids and 'gaming_kb' in ids:
        found.append('풀 RGB 셋업')
    if case == 'case2' and tags.count('minimal') >= 3:
        found.append('화이트 셋업')
    if 1 <= sum(p['layer'] == 'desk' for p in placed) <= 3:
        found.append('미니멀리즘')
    if 'wall_light' in ids and lamps:
        found.append('균형 조명')
    return found


def score(request, placed, pc, spent):
    ids = [p['id'] for p in placed]
    theme = set(request['theme'])

    objects = [ITEMS[i]['tags'] for i in ids] + ([PARTS[pc['CASE']]['tags']] if 'CASE' in pc else [])
    theme_s = 30 * sum(bool(theme & set(t)) for t in objects) / len(objects) if objects else 0

    reqs = request['required']
    met = sum(min(1, sum(ids.count(i) for i in r['any']) / r['count']) for r in reqs)
    req_s = 20 * met / len(reqs) if reqs else 20
    req_s = max(0, req_s - 10 * sum(ids.count(f) for f in request['forbidden']))

    boot = boot_status(pc)
    stars_pc = pc_stats(pc)[3] if boot == 'ok' else 0
    pc_s = 0 if boot != 'ok' else max(0, 20 - 8 * max(0, request['perf'] - stars_pc))

    syn = synergies(placed, pc)
    syn_s = min(20, 10 * len(syn))

    budget_s = 10 * max(0, request['budget'] - spent) / request['budget']

    parts = {'테마 일치': theme_s, '필수 · 금지': req_s, 'PC 성능': pc_s, '조합 시너지': syn_s, '예산 절약': budget_s}
    total = round(sum(parts.values()))
    stars = next((s for cut, s in STAR_CUTS if total >= cut), 0)
    return {'parts': parts, 'total': total, 'stars': stars, 'synergies': syn, 'boot': boot,
            'line': reaction(request, parts, boot)}


MAX = {'테마 일치': 30, '필수 · 금지': 20, 'PC 성능': 20, '조합 시너지': 20, '예산 절약': 10}
LINES = {
    '테마 일치': '음… 제가 말한 분위기랑은 좀 달라요.',
    '필수 · 금지': '부탁드린 게 빠졌거나, 싫다는 게 들어갔어요.',
    'PC 성능': '켜지긴 하는데 좀 느리네요…',
    '조합 시너지': '하나하나는 좋은데, 어울림이 아쉬워요.',
    '예산 절약': '좋긴 한데… 돈을 너무 많이 쓰셨어요.',
}


def reaction(request, parts, boot):
    if boot == 'missing':
        return 'PC가 안 켜져요. 부품이 빠진 것 같아요.'
    if boot == 'power':
        return '게임 켜자마자 꺼졌어요… 파워가 부족한가 봐요.'
    worst = min(parts, key=lambda k: parts[k] / MAX[k])
    if parts[worst] / MAX[worst] >= 0.8:
        return '상상한 그대로예요! 단골 할게요.'
    return LINES[worst]


if __name__ == '__main__':
    from common import REQUESTS
    dev = REQUESTS[1]
    good_pc = {'CPU': 'cpu2', 'GPU': 'gpu2', 'RAM': 'ram2', 'PSU': 'psu1', 'CASE': 'case1'}
    placed = [{'id': 'monitor', 'layer': 'desk', 'slot': 0}, {'id': 'monitor', 'layer': 'desk', 'slot': 2},
              {'id': 'lamp_warm', 'layer': 'desk', 'slot': 4}, {'id': 'book', 'layer': 'desk', 'slot': 5},
              {'id': 'wall_light', 'layer': 'wall', 'slot': 0}]
    assert boot_status(good_pc) == 'ok'
    assert boot_status({**good_pc, 'GPU': 'gpu3'}) == 'power'  # 105 + 350 > 400W
    assert boot_status({'CPU': 'cpu1'}) == 'missing'
    assert set(synergies(placed, good_pc)) == {'독서 콤보', '균형 조명'}
    r = score(dev, placed, good_pc, 110 + 50 + 4 + 2 + 5)
    assert r['parts']['필수 · 금지'] == 20 and r['parts']['PC 성능'] == 20 and r['stars'] >= 2, r
    bad = score(dev, placed + [{'id': 'lamp_cool', 'layer': 'desk', 'slot': 7}], {**good_pc, 'GPU': 'gpu3'}, 200)
    assert bad['parts']['PC 성능'] == 0 and bad['parts']['필수 · 금지'] == 10
    print('scorer ok', r['total'], r['stars'])
