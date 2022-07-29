import curses


debug = None


def main(screen):
    global debug
    curses.flushinp()
    curses.set_escdelay(100)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    win = curses.newwin(5, 30, 5, 30)
    win.keypad(True)
    win.box()
    win.addstr(1, 1, 'hold click and drag me')
    win.addstr(2, 1, 'ESC to quit')

    moving = None

    while True:
        key = win.getch()
        if key == 27: # escape
            break

        elif key == curses.KEY_MOUSE:
            _, x, y, _, btn = curses.getmouse()

            if btn & curses.BUTTON1_PRESSED:
                wy, wx = win.getbegyx()
                h, w = win.getmaxyx()

                if x >= wx and x < wx + w and y >= wy and y < wy + h:
                    moving = (x, y)

            elif moving:
                sx = moving[0]
                sy = moving[1]

                if x != sx or y != sy:
                    dx = x - sx
                    dy = y - sy
                    wy, wx = win.getbegyx()
                    h, w = win.getmaxyx()

                    nx = wx + dx
                    if nx < 0: nx = 0
                    elif nx + w >= curses.COLS: nx = curses.COLS - w

                    ny = wy + dy
                    if ny < 0: ny = 0
                    elif ny + h >= curses.LINES: ny = curses.LINES - h

                    screen.clear()
                    screen.refresh()
                    win.mvwin(ny, nx)
                    moving = (x, y)

                if btn & curses.BUTTON1_RELEASED:
                    moving = None


curses.wrapper(main)
curses.flushinp()

if debug is not None:
    print(f'debug: {debug}')

