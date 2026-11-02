from pico2d import *

import game_framework
import request_mode
import title_mode
import scorer
import state
from common import WIDTH, HEIGHT, REQUESTS, box, outline, text

result = None


def init():
    global result
    result = scorer.score(state.request(), state.room.placed, state.pc, state.spent())


def finish():
    pass


def next_mode():
    if state.request_index + 1 < len(REQUESTS):
        state.request_index += 1
        game_framework.change_mode(request_mode)
    else:
        state.request_index = 0
        title_mode.message = '모든 의뢰 완료! (자유 모드는 개발 예정)'
        game_framework.change_mode(title_mode)


def handle_events():
    for e in get_events():
        if e.type == SDL_QUIT or (e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE):
            game_framework.quit()
        elif e.type == SDL_MOUSEBUTTONDOWN or (e.type == SDL_KEYDOWN and e.key == SDLK_RETURN):
            next_mode()


def update():
    pass


def draw():
    clear_canvas()
    box(0, 0, WIDTH, HEIGHT, (18, 12, 38))
    stars = '★' * result['stars'] + '☆' * (3 - result['stars'])
    text(120, 620, state.request()['customer'], 24, (200, 192, 240))
    text(120, 550, stars, 60, (255, 214, 92))
    text(420, 550, f"{result['total']}점", 48, (255, 255, 255))
    for i, (k, v) in enumerate(result['parts'].items()):
        y = 450 - i * 44
        text(120, y, k, 20, (200, 192, 240))
        text(320, y, f"{v:.0f} / {scorer.MAX[k]}", 20, (255, 255, 255))
    syn = ', '.join(result['synergies']) or '없음'
    text(120, 210, f"달성 시너지: {syn}", 18, (120, 255, 170))
    box(640, 300, 1180, 460, (34, 24, 70))
    outline(640, 300, 1180, 460)
    text(670, 380, f"\"{result['line']}\"", 20)
    text(120, 120, '클릭해서 다음 의뢰로', 18, (140, 128, 200))
    update_canvas()
