"""책상 꾸미기 화면: 왼쪽 상점에서 끌어다 벽 · 책상 위 · 바닥 슬롯에 놓는다."""
from pico2d import *

import game_framework
import build_mode
import result_mode
import state
import ui
from common import WIDTH, HEIGHT, ITEMS, box, outline, text, to_canvas_y, inside
from room import LAYERS, LAYER_NAMES, SLOT_X0, SLOT_W, SLOT_COUNT, drop_target

SHOP_W, ROW_H, ROW_TOP = 270, 31, 600
SHOP_IDS = list(ITEMS)
PC_RECT = (1170, 80, 1250, 270)
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


def text_color(color):
    return (43, 45, 66) if sum(color) > 450 else (255, 255, 255)


def draw_item(item_id, x1, y1, x2, y2):
    c = tuple(ITEMS[item_id]['color'])
    box(x1, y1, x2, y2, c)
    outline(x1, y1, x2, y2)
    text(x1 + 6, (y1 + y2) // 2, ITEMS[item_id]['name'], 14, text_color(c))


def draw_room():
    box(SHOP_W, 190, WIDTH, HEIGHT - 70, (233, 228, 240))   # 벽
    box(SHOP_W, 0, WIDTH, 190, (201, 173, 167))             # 바닥
    box(SLOT_X0 - 10, 310, SLOT_X0 + SLOT_W * SLOT_COUNT + 10, 330, (139, 94, 60))  # 책상 상판
    box(SLOT_X0, 60, SLOT_X0 + 18, 310, (107, 68, 41))
    box(SLOT_X0 + SLOT_W * SLOT_COUNT - 18, 60, SLOT_X0 + SLOT_W * SLOT_COUNT, 310, (107, 68, 41))
    box(*PC_RECT, (43, 45, 66))
    pc_ok = len(state.pc) == 5
    text(PC_RECT[0] + 22, PC_RECT[3] - 24, 'PC', 22, (242, 165, 65) if pc_ok else (255, 255, 255))
    text(PC_RECT[0] + 8, PC_RECT[1] + 20, f"{len(state.pc)}/5", 16, (255, 255, 255))
    for layer, (bottom, h) in LAYERS.items():
        text(SHOP_W + 8, bottom + h // 2, LAYER_NAMES[layer], 14, (141, 153, 174))
        if held and ITEMS[held]['layer'] == layer:  # 놓을 수 있는 레이어 슬롯 표시
            for s in range(SLOT_COUNT):
                outline(SLOT_X0 + s * SLOT_W + 4, bottom, SLOT_X0 + (s + 1) * SLOT_W - 4, bottom + h, (242, 165, 65))
    for p in state.room.placed:
        draw_item(p['id'], *state.room.rect(p))


def draw_shop():
    box(0, 0, SHOP_W, HEIGHT - 70, (255, 255, 255))
    text(14, ROW_TOP + 20, '상점  (드래그해서 배치)', 18)
    left = state.money_left()
    for i, item_id in enumerate(SHOP_IDS):
        it = ITEMS[item_id]
        x1, y1, x2, y2 = shop_row(i)
        dim = it['price'] > left
        box(x1, y1, x1 + 22, y2, tuple(it['color']))
        outline(x1, y1, x1 + 22, y2)
        text(x1 + 30, (y1 + y2) // 2, it['name'], 15, (170, 170, 170) if dim else (43, 45, 66))
        text(x2 - 92, (y1 + y2) // 2, f"{it['price']}만 · {LAYER_NAMES[it['layer']]}", 13, (141, 153, 174))


def draw():
    clear_canvas()
    draw_room()
    draw_shop()
    ui.top_bar()
    ui.button(BTN_PC, 'PC 조립 [Tab]')
    ui.button(BTN_DONE, '완료 [Enter]', (106, 156, 120))
    text(SHOP_W + 10, 30, '우클릭: 되돌리기(환불)', 14, (74, 78, 105))
    if toast:
        text(SHOP_W + 230, 30, toast, 16, (231, 111, 81))
    if held:
        w = ITEMS[held]['size'] * SLOT_W - 12
        h = LAYERS[ITEMS[held]['layer']][1]
        x, y = mouse
        draw_item(held, x - w // 2, y - h // 2, x + w // 2, y + h // 2)
    update_canvas()
