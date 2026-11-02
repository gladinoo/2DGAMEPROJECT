"""책상 꾸미기 화면: 상점에서 끌어다 벽 · 책상 위에 놓고, 케이블 모드(C)에서 기기를 PC 포트에 잇는다."""
from pico2d import *

import game_framework
import build_mode
import result_mode
import state
import ui
import cables as cab
from common import WIDTH, HEIGHT, ITEMS, box, outline, text, to_canvas_y, inside, sprite, draw_fit
from room import LAYERS, LAYER_NAMES, SLOT_X0, SLOT_W, SLOT_COUNT, drop_target

SHOP_W, ROW_H, ROW_TOP = 270, 31, 600
SHOP_IDS = list(ITEMS)
PC_RECT = (1095, 210, 1255, 470)
BTN_PC = (930, 10, 1090, 50)
BTN_DONE = (1100, 10, 1270, 50)
BTN_CABLE = (760, 10, 920, 50)
CABLE_HINT = {'DP': '모니터는 DP 포트에', 'USB': 'USB 기기는 USB 포트에', 'AUDIO': '스피커 · 헤드셋은 오디오 포트에'}

held = None   # 끌고 있는 소품 id
cable_mode = False
wiring = None  # 케이블을 끌고 있는 기기 (room.placed 항목)
mouse = (0, 0)
toast = ''


def init():
    global held, toast, wiring
    held, toast, wiring = None, '', None


def finish():
    pass


def shop_row(i):
    y = ROW_TOP - i * ROW_H
    return 10, y - ROW_H + 4, SHOP_W - 10, y


def on_down(x, y, button):
    global held, toast, wiring
    port = cab.port_at(x, y, state.pc)
    if button == SDL_BUTTON_RIGHT and port:
        state.cables = [c for c in state.cables if (c['type'], c['port']) != port]
        return
    if inside(x, y, BTN_CABLE):
        toggle_cable_mode()
        return
    if cable_mode and button == SDL_BUTTON_LEFT:
        p = state.room.item_at(x, y)
        if p and cab.needs_cable(p):
            state.cables = [c for c in state.cables if c['dev'] is not p]
            wiring, toast = p, ''
        elif p:
            toast = f"{ITEMS[p['id']]['name']}은(는) 케이블이 필요 없어요"
        return
    if button == SDL_BUTTON_RIGHT:
        p = state.room.item_at(x, y)
        if p:
            state.room.placed.remove(p)  # 되돌리면 전액 환불(프로토타입)
        return
    for i, item_id in enumerate(SHOP_IDS):
        if inside(x, y, shop_row(i)):
            if ITEMS[item_id]['price'] > state.money_left():
                toast = '예산이 부족해요!'
            else:
                held, toast = item_id, ''
            return
    p = state.room.item_at(x, y)
    if p:
        state.room.placed.remove(p)
        held = p['id']
    elif inside(x, y, PC_RECT) or inside(x, y, BTN_PC):
        game_framework.change_mode(build_mode)
    elif inside(x, y, BTN_DONE):
        game_framework.change_mode(result_mode)


def toggle_cable_mode():
    global cable_mode, held, toast
    cable_mode, held, toast = not cable_mode, None, ''


def on_up(x, y):
    global held, toast, wiring
    if wiring:
        need = ITEMS[wiring['id']]['port']
        port = cab.port_at(x, y, state.pc)
        if port and port[0] != need:
            toast = CABLE_HINT[need] + ' 꽂아야 해요'
        elif port and any((c['type'], c['port']) == port for c in state.cables):
            toast = '이미 쓰고 있는 포트예요'
        elif port:
            state.cables.append({'dev': wiring, 'type': port[0], 'port': port[1]})
        wiring = None
        return
    if not held:
        return
    target = drop_target(held, x, y)
    if target and state.room.fits(held, *target):
        state.room.place(held, *target)
    elif target:
        toast = f"{ITEMS[held]['name']}은(는) '{LAYER_NAMES[ITEMS[held]['layer']]}'의 빈 칸에만 놓을 수 있어요"
    held = None


def handle_events():
    global mouse
    for e in get_events():
        if e.type == SDL_QUIT or (e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE):
            game_framework.quit()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_TAB:
            game_framework.change_mode(build_mode)
        elif e.type == SDL_KEYDOWN and e.key == SDLK_c:
            toggle_cable_mode()
        elif e.type == SDL_KEYDOWN and e.key == SDLK_RETURN:
            game_framework.change_mode(result_mode)
        elif e.type == SDL_MOUSEMOTION:
            mouse = (e.x, to_canvas_y(e.y))
        elif e.type == SDL_MOUSEBUTTONDOWN:
            mouse = (e.x, to_canvas_y(e.y))
            on_down(*mouse, e.button)
        elif e.type == SDL_MOUSEBUTTONUP and e.button == SDL_BUTTON_LEFT:
            on_up(e.x, to_canvas_y(e.y))


def update():
    state.cables = cab.prune(state.cables, state.room, state.pc)  # 치운 기기 · 사라진 포트의 선은 자동으로 뽑힘


def draw_sprite(item_id, x1, y1, x2, y2):
    """칸(rect) 안에 소품을 그린다. 책상 위는 상판에 붙이고, 벽은 가운데 정렬."""
    img = sprite(item_id)
    cx = (x1 + x2) // 2
    layer = ITEMS[item_id]['layer']
    if layer == 'wall':
        img.draw(cx, (y1 + y2) // 2)
    else:
        img.draw(cx, y1 + img.h // 2)


def draw_room():
    sprite('room_bg').draw(SHOP_W + (WIDTH - SHOP_W) // 2, (HEIGHT - 70) // 2)
    by_layer = lambda *layers: [p for p in state.room.placed if p['layer'] in layers]
    for p in by_layer('wall') + by_layer('desk'):
        draw_sprite(p['id'], *state.room.rect(p))
    case = state.pc.get('CASE')
    img = sprite(case or 'case_empty')
    img.draw((PC_RECT[0] + PC_RECT[2]) // 2, PC_RECT[1] + img.h // 2)
    label = '부팅 준비' if len(state.pc) == 5 else f"PC 부품 {len(state.pc)}/5"
    text(PC_RECT[0] + 20, PC_RECT[3] + 16, label, 14, (46, 230, 214))
    if held:
        bottom, h = LAYERS[ITEMS[held]['layer']]
        for s in range(SLOT_COUNT):
            if state.room.fits(held, ITEMS[held]['layer'], s):  # 놓을 수 있는 칸만 표시
                outline(SLOT_X0 + s * SLOT_W + 4, bottom, SLOT_X0 + (s + 1) * SLOT_W - 4, bottom + h, (46, 230, 214))


def thick_line(points, color):
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        for d in (-1, 0, 1):
            draw_line(x1, y1 + d, x2, y2 + d, *color)
            draw_line(x1 + d, y1, x2 + d, y2, *color)


def cable_points(a, b):
    """처지는 선: a → b 2차 베지어."""
    (x0, y0), (x2, y2) = a, b
    cx, cy = (x0 + x2) / 2, min(y0, y2) - 46
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y2)
            for t in (i / 16 for i in range(17))]


def draw_ports():
    x1, y1, x2, y2 = cab.PANEL
    box(x1, y1, x2, y2, (14, 9, 30))
    outline(x1, y1, x2, y2, (124, 92, 255))
    text(x1 + 8, y2 - 12, 'PC 후면 포트', 12, (170, 160, 220))
    used = {(c['type'], c['port']) for c in state.cables}
    for t in cab.ORDER:
        n = cab.port_count(t, state.pc)
        for i in range(3 if t == 'DP' else cab.PORT_COUNT[t]):
            px, py = cab.port_pos(t, i)
            color = cab.PORT_COLOR[t] if i < n else (60, 50, 90)
            box(px - 13, py - 9, px + 13, py + 9, color if (t, i) in used else (24, 16, 52))
            outline(px - 13, py - 9, px + 13, py + 9, color)
        lx, _ = cab.port_pos(t, 0)
        text(lx - 13, y1 + 10, cab.PORT_NAMES[t] + ('' if t != 'DP' or n else ' (GPU 필요)'), 12, cab.PORT_COLOR[t])


def draw_cables():
    blink = int(get_time() * 3) % 2
    for c in state.cables:
        a = cab.plug_pos(state.room, c['dev'])
        b = cab.port_pos(c['type'], c['port'])
        thick_line(cable_points((a[0], a[1] - 8), b), cab.PORT_COLOR[c['type']])
        box(a[0] - 5, a[1] - 12, a[0] + 5, a[1] - 4, cab.PORT_COLOR[c['type']])
    plugged = {id(c['dev']) for c in state.cables}
    for p in state.room.placed:
        if cab.needs_cable(p) and id(p) not in plugged:
            x, y = cab.plug_pos(state.room, p)
            color = cab.PORT_COLOR[ITEMS[p['id']]['port']] if cable_mode else ((255, 77, 141) if blink else (120, 40, 80))
            draw_circle(x, y - 8, 6, *color, 255, True)
    if wiring:
        a = cab.plug_pos(state.room, wiring)
        thick_line(cable_points((a[0], a[1] - 8), mouse), cab.PORT_COLOR[ITEMS[wiring['id']]['port']])
    if cable_mode:
        _, unplugged, tangles = cab.wiring_score(state.cables, state.room)
        text(cab.PANEL[0], cab.PANEL[3] + 14, f"미연결 {unplugged}  ·  꼬임 {tangles}", 14,
             (120, 255, 170) if not unplugged and not tangles else (255, 214, 92))


def draw_shop():
    box(0, 0, SHOP_W, HEIGHT - 70, (34, 24, 70))
    text(14, ROW_TOP + 20, '상점  (드래그해서 배치)', 18)
    left = state.money_left()
    for i, item_id in enumerate(SHOP_IDS):
        it = ITEMS[item_id]
        x1, y1, x2, y2 = shop_row(i)
        dim = it['price'] > left
        draw_fit(item_id, x1 + 14, (y1 + y2) // 2, 28, 25)
        text(x1 + 34, (y1 + y2) // 2, it['name'], 15, (90, 78, 130) if dim else (232, 226, 255))
        text(x2 - 92, (y1 + y2) // 2, f"{it['price']}만 · {LAYER_NAMES[it['layer']]}", 13, (140, 128, 200))


def draw():
    clear_canvas()
    draw_room()
    draw_ports()
    draw_cables()
    draw_shop()
    ui.top_bar()
    ui.button(BTN_PC, 'PC 조립 [Tab]')
    ui.button(BTN_DONE, '완료 [Enter]', (255, 77, 141))
    ui.button(BTN_CABLE, '케이블 끄기 [C]' if cable_mode else '케이블 [C]', (255, 214, 92) if cable_mode else (124, 92, 255))
    hint = '기기를 끌어 같은 색 포트에 꽂기 · 우클릭: 선 뽑기' if cable_mode else '우클릭: 되돌리기(환불)'
    text(SHOP_W + 10, 30, hint, 14, (170, 160, 220))
    if toast:
        text(SHOP_W + 10, 62, toast, 16, (255, 77, 141))
    if held:
        x, y = mouse
        sprite(held).draw(x, y)
    update_canvas()
