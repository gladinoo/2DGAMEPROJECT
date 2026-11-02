"""여러 화면이 함께 쓰는 상단 바와 버튼."""
from common import WIDTH, HEIGHT, box, outline, text, inside
import state

DARK = (43, 45, 66)
AMBER = (242, 165, 65)
WHITE = (255, 255, 255)


def top_bar():
    req = state.request()
    box(0, HEIGHT - 70, WIDTH, HEIGHT, DARK)
    text(20, HEIGHT - 24, f"의뢰 {state.request_index + 1}. {req['customer']}", 20, AMBER)
    text(20, HEIGHT - 52, req['intro'], 16, WHITE)
    left = state.money_left()
    text(WIDTH - 260, HEIGHT - 36, f"남은 예산  {left}만 원", 22, AMBER if left >= 0 else (231, 111, 81))


def button(rect, label, color=AMBER):
    box(*rect, color)
    outline(*rect)
    text(rect[0] + 14, (rect[1] + rect[3]) // 2, label, 18, DARK)


def clicked(rect, x, y):
    return inside(x, y, rect)
