"""한 의뢰 동안 유지되는 상태. 꾸미기 화면과 PC 조립 화면이 함께 쓴다."""
from common import ITEMS, PARTS, REQUESTS
from room import Room

request_index = 0
room = Room()
pc = {}  # 부품 종류(CPU/GPU/RAM/PSU/CASE) -> part id


def request():
    return REQUESTS[request_index]


def reset():
    global room, pc
    room = Room()
    pc = {}


def spent():
    return sum(ITEMS[p['id']]['price'] for p in room.placed) + sum(PARTS[pid]['price'] for pid in pc.values())


def money_left():
    return request()['budget'] - spent()
