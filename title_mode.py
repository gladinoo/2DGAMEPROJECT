from pico2d import *

import game_framework
import request_mode
from common import WIDTH, HEIGHT, box, text

message = ''


def init():
    pass


def finish():
    pass


def handle_events():
    for e in get_events():
        if e.type == SDL_QUIT or (e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE):
            game_framework.quit()
        elif e.type == SDL_MOUSEBUTTONDOWN or (e.type == SDL_KEYDOWN and e.key == SDLK_RETURN):
            game_framework.change_mode(request_mode)


def update():
    pass


def draw():
    clear_canvas()
    box(0, 0, WIDTH, HEIGHT, (43, 45, 66))
    text(120, 470, '데스크테리어 의뢰소', 64, (255, 255, 255))
    text(124, 400, '손님의 취향과 예산에 맞춰 책상을 꾸미고 PC를 조립하세요', 22, (216, 218, 229))
    text(124, 260, '클릭하거나 Enter를 눌러 시작', 22, (242, 165, 65))
    if message:
        text(124, 200, message, 20, (106, 156, 120))
    update_canvas()
