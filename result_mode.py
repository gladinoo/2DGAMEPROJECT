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
    box(0, 0, WIDTH, HEIGHT, (43, 45, 66))
    stars = '★' * result['stars'] + '☆' * (3 - result['stars'])
    text(120, 620, state.request()['customer'], 24, (216, 218, 229))
    text(120, 550, stars, 60, (242, 165, 65))
    text(420, 550, f"{result['total']}점", 48, (255, 255, 255))
    for i, (k, v) in enumerate(result['parts'].items()):
        y = 450 - i * 44
        text(120, y, k, 20, (216, 218, 229))
        text(320, y, f"{v:.0f} / {scorer.MAX[k]}", 20, (255, 255, 255))
    syn = ', '.join(result['synergies']) or '없음'
    text(120, 210, f"달성 시너지: {syn}", 18, (106, 156, 120))
    box(640, 300, 1180, 460, (255, 255, 255))
    outline(640, 300, 1180, 460)
    text(670, 380, f"\"{result['line']}\"", 20)
    text(120, 120, '클릭해서 다음 의뢰로', 18, (141, 153, 174))
    update_canvas()
