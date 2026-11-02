"""책상 꾸미기 화면: 왼쪽 상점에서 끌어다 벽 · 책상 위 · 바닥 슬롯에 놓는다."""
from pico2d import *

import game_framework
import build_mode
import result_mode
import state
import ui
from common import WIDTH, HEIGHT, ITEMS, box, outline, text, to_canvas_y, inside, sprite, draw_fit
from room import LAYERS, LAYER_NAMES, SLOT_X0, SLOT_W, SLOT_COUNT, drop_target

SHOP_W, ROW_H, ROW_TOP = 270, 31, 600
SHOP_IDS = list(ITEMS)
PC_RECT = (1168, 80, 1252, 276)
BTN_PC = (930, 10, 1090, 50)
BTN_DONE = (1100, 10, 1270, 50)

held = None   # 끌고 있는 소품 id
mouse = (0, 0)
toast = ''


def init():
    global held, toast
    held, toast = None, ''


def finish():
    pass


def shop_row(i):
    y = ROW_TOP - i * ROW_H
    return 10, y - ROW_H + 4, SHOP_W - 10, y


def on_down(x, y, button):
    global held, toast
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


def on_up(x, y):
    global held, toast
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
    pass


def draw_sprite(item_id, x1, y1, x2, y2):
    """칸(rect) 안에 소품을 그린다. 책상 위 · 바닥은 바닥선에 붙이고, 벽은 가운데 정렬."""
    img = sprite(item_id)
    cx = (x1 + x2) // 2
    layer = ITEMS[item_id]['layer']
    if item_id == 'rug':
        img.draw(cx, 60 + img.h // 2)
    elif layer == 'wall':
        img.draw(cx, (y1 + y2) // 2)
    else:
        img.draw(cx, y1 + img.h // 2)


def draw_room():
    sprite('room_bg').draw(SHOP_W + (WIDTH - SHOP_W) // 2, (HEIGHT - 70) // 2)
    by_layer = lambda *layers: [p for p in state.room.placed if p['layer'] in layers]
    for p in by_layer('wall') + [p for p in by_layer('floor') if p['id'] == 'rug']:
        draw_sprite(p['id'], *state.room.rect(p))
    sprite('desk').draw(SLOT_X0 + SLOT_W * SLOT_COUNT // 2, 330 - 136)
    for p in by_layer('desk') + [p for p in by_layer('floor') if p['id'] != 'rug']:
        draw_sprite(p['id'], *state.room.rect(p))
    case = state.pc.get('CASE')
    sprite(case or 'case_empty').draw((PC_RECT[0] + PC_RECT[2]) // 2, PC_RECT[1] + 98)
    label = '부팅 준비' if len(state.pc) == 5 else f"PC 부품 {len(state.pc)}/5"
    text(PC_RECT[0] - 6, PC_RECT[3] + 14, label, 14, (46, 230, 214))
    if held:
        bottom, h = LAYERS[ITEMS[held]['layer']]
        for s in range(SLOT_COUNT):
            if state.room.fits(held, ITEMS[held]['layer'], s):  # 놓을 수 있는 칸만 표시
                outline(SLOT_X0 + s * SLOT_W + 4, bottom, SLOT_X0 + (s + 1) * SLOT_W - 4, bottom + h, (46, 230, 214))


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
    draw_shop()
    ui.top_bar()
    ui.button(BTN_PC, 'PC 조립 [Tab]')
    ui.button(BTN_DONE, '완료 [Enter]', (255, 77, 141))
    text(SHOP_W + 10, 30, '우클릭: 되돌리기(환불)', 14, (170, 160, 220))
    if toast:
        text(SHOP_W + 230, 30, toast, 16, (255, 77, 141))
    if held:
        x, y = mouse
        sprite(held).draw(x, y)
    update_canvas()
