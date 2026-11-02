"""여러 화면이 함께 쓰는 상단 바와 버튼."""
from common import WIDTH, HEIGHT, box, outline, text, inside
import state

DARK = (18, 12, 38)
BAR = (24, 16, 52)
AMBER = (46, 230, 214)
WHITE = (255, 255, 255)


def top_bar():
    req = state.request()
    box(0, HEIGHT - 70, WIDTH, HEIGHT, BAR)
    box(0, HEIGHT - 72, WIDTH, HEIGHT - 70, (255, 77, 141))
    text(20, HEIGHT - 24, f"의뢰 {state.request_index + 1}. {req['customer']}", 20, AMBER)
    text(20, HEIGHT - 52, req['intro'], 16, WHITE)
    left = state.money_left()
    text(WIDTH - 260, HEIGHT - 36, f"남은 예산  {left}만 원", 22, AMBER if left >= 0 else (255, 77, 141))


def button(rect, label, color=AMBER):
    box(*rect, color)
    outline(*rect)
    text(rect[0] + 14, (rect[1] + rect[3]) // 2, label, 18, DARK)


def clicked(rect, x, y):
    return inside(x, y, rect)
