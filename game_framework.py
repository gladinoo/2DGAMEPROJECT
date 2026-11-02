import time

running = True
stack = []


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def quit():
    global running
    running = False


def run(start_mode):
    global running
    running = True
    stack.append(start_mode)
    start_mode.init()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        time.sleep(0.01)
    while stack:
        stack.pop().finish()
