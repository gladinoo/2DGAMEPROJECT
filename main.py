from pico2d import open_canvas, close_canvas

import game_framework
import title_mode
from common import WIDTH, HEIGHT

open_canvas(WIDTH, HEIGHT)
game_framework.run(title_mode)
close_canvas()
