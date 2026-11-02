from pico2d import *

import game_framework
import decorate_mode
import state
from common import WIDTH, HEIGHT, ITEMS, THEME_NAMES, box, outline, text

STARS = ['-', '★', '★★', '★★★']


def init():
    state.reset()


def finish():
    pass


def handle_events():
    for e in get_events():
        if e.type == SDL_QUIT or (e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE):
            game_framework.quit()
        elif e.type == SDL_MOUSEBUTTONDOWN or (e.type == SDL_KEYDOWN and e.key == SDLK_RETURN):
            game_framework.change_mode(decorate_mode)


def update():
    pass


def draw():
    req = state.request()
    clear_canvas()
    box(0, 0, WIDTH, HEIGHT, (18, 12, 38))
    box(340, 110, 940, 620, (34, 24, 70))
    outline(340, 110, 940, 620)
    text(380, 580, f"의뢰 {state.request_index + 1}", 20, (255, 77, 141))
    text(380, 535, req['customer'], 36)
    text(380, 480, f"\"{req['intro']}\"", 18, (170, 160, 220))
    rows = [
        ('테마', ' · '.join(THEME_NAMES[t] for t in req['theme'])),
        ('필수', ', '.join(f"{'/'.join(ITEMS[i]['name'] for i in r['any'])} {r['count']}개" for r in req['required'])),
        ('금지', ', '.join(ITEMS[i]['name'] for i in req['forbidden']) or '없음'),
        ('PC 성능', STARS[req['perf']] + ' 이상'),
        ('예산', f"{req['budget']}만 원"),
    ]
    for i, (k, v) in enumerate(rows):
        y = 410 - i * 52
        text(380, y, k, 20, (255, 77, 141))
        text(500, y, v, 20)
    text(380, 140, '클릭해서 의뢰 수락', 18, (140, 128, 200))
    update_canvas()
