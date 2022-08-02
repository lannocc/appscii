from .common import Window
from .matrix import CharMap

import curses


class Application:
    def __init__(self, shell):
        self.shell = shell

        self.screen = curses.initscr()
        curses.flushinp()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        try: curses.set_escdelay(222)
        except AttributeError: pass
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.mouseinterval(0)

        self.matrix = CharMap(self.w, self.h)
        self.mbtns = [False, False, False] # mouse buttons (left, mid, right)

    def exit(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.flushinp()
        curses.endwin()

    @property
    def w(self):
        return curses.COLS

    @property
    def h(self):
        return curses.LINES

    def inputs(self):
        while self.shell.go:
            key = self.screen.getch()

            if key == curses.KEY_MOUSE:
                _, x, y, _, btn = curses.getmouse()
                mbtns = self.mbtns

                if btn & curses.BUTTON1_PRESSED:
                    mbtns[0] = True
                elif btn & curses.BUTTON1_RELEASED:
                    mbtns[0] = False

                if btn & curses.BUTTON2_PRESSED:
                    mbtns[1] = True
                elif btn & curses.BUTTON2_RELEASED:
                    mbtns[1] = False

                if btn & curses.BUTTON3_PRESSED:
                    mbtns[2] = True
                elif btn & curses.BUTTON3_RELEASED:
                    mbtns[2] = False

                if btn & curses.BUTTON1_CLICKED \
                        or btn & curses.BUTTON1_DOUBLE_CLICKED:
                    self.shell.on_mouse(x, y, True, mbtns[1], mbtns[2], 0)
                    self.shell.on_mouse(x, y, False, mbtns[1], mbtns[2], 0)

                    if btn & curses.BUTTON1_DOUBLE_CLICKED:
                        self.shell.on_mouse(x, y, True, mbtns[1], mbtns[2], 0)
                        self.shell.on_mouse(x, y, False, mbtns[1], mbtns[2], 0)

                elif btn & curses.BUTTON2_CLICKED \
                        or btn & curses.BUTTON2_DOUBLE_CLICKED:
                    self.shell.on_mouse(x, y, mbtns[0], True, mbtns[2], 0)
                    self.shell.on_mouse(x, y, mbtns[0], False, mbtns[2], 0)

                    if btn & curses.BUTTON2_DOUBLE_CLICKED:
                        self.shell.on_mouse(x, y, mbtns[0], True, mbtns[2], 0)
                        self.shell.on_mouse(x, y, mbtns[0], False, mbtns[2], 0)

                elif btn & curses.BUTTON3_CLICKED \
                        or btn & curses.BUTTON3_DOUBLE_CLICKED:
                    self.shell.on_mouse(x, y, mbtns[0], mbtns[1], True, 0)
                    self.shell.on_mouse(x, y, mbtns[0], mbtns[1], False, 0)

                    if btn & curses.BUTTON3_DOUBLE_CLICKED:
                        self.shell.on_mouse(x, y, mbtns[0], mbtns[1], True, 0)
                        self.shell.on_mouse(x, y, mbtns[0], mbtns[1], False, 0)

                elif btn & curses.BUTTON4_PRESSED:
                    self.shell.on_mouse(x, y, mbtns[0], mbtns[1], mbtns[2], 1)

                elif btn & 2097152:
                    self.shell.on_mouse(x, y, mbtns[0], mbtns[1], mbtns[2], -1)

                else:
                    self.shell.on_mouse(x, y, mbtns[0], mbtns[1], mbtns[2], 0)

            else:
                #raise RuntimeError('just a test')
                self.shell.on_key(key)

    def refresh(self):
        try:
            for y in range(self.matrix.h):
                chars = self.matrix.chars[y]
                changes = self.matrix.changes[y]

                for x in range(self.matrix.w):
                    if changes[x]:
                        c = chars[x]
                        self.screen.addstr(y, x, '.' if c is None else c)
                        changes[x] = False

        except curses.error as e:
            # we can ignore error on bottom-right character
            if not (x == self.w - 1 and y == self.h - 1):
                raise ValueError(f'at {x},{y} (x,y)') from e

