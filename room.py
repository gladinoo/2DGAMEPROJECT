"""정면 뷰 책상: 벽 · 책상 위 · 바닥 3레이어, 각 레이어는 가로 슬롯 8칸."""
from common import ITEMS

SLOT_X0, SLOT_W, SLOT_COUNT = 340, 100, 8
LAYERS = {  # layer -> (bottom y, height)
    'wall': (470, 90),
    'desk': (330, 80),
    'floor': (80, 90),
}
LAYER_NAMES = {'wall': '벽', 'desk': '책상 위', 'floor': '바닥'}


class Room:
    def __init__(self):
        self.placed = []  # {'id', 'layer', 'slot'}

    def fits(self, item_id, layer, slot):
        size = ITEMS[item_id]['size']
        if ITEMS[item_id]['layer'] != layer or slot < 0 or slot + size > SLOT_COUNT:
            return False
        for p in self.placed:
            if p['layer'] == layer:
                ps = ITEMS[p['id']]['size']
                if slot < p['slot'] + ps and p['slot'] < slot + size:
                    return False
        return True

    def place(self, item_id, layer, slot):
        self.placed.append({'id': item_id, 'layer': layer, 'slot': slot})

    def rect(self, p):
        bottom, h = LAYERS[p['layer']]
        size = ITEMS[p['id']]['size']
        x1 = SLOT_X0 + p['slot'] * SLOT_W + 6
        return x1, bottom, x1 + size * SLOT_W - 12, bottom + h

    def item_at(self, x, y):
        for p in reversed(self.placed):
            x1, y1, x2, y2 = self.rect(p)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return p
        return None

    def ids(self):
        return [p['id'] for p in self.placed]


def drop_target(item_id, x, y):
    """마우스 위치(물건 중심) -> 놓일 (layer, slot). 레이어 밴드 밖이면 None."""
    for layer, (bottom, h) in LAYERS.items():
        if bottom - 40 <= y <= bottom + h + 40:
            size = ITEMS[item_id]['size']
            slot = round((x - SLOT_X0) / SLOT_W - size / 2)
            return layer, slot
    return None
