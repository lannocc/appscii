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
        curses.set_escdelay(99)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

        self.mbtns = [False, False, False] # mouse buttons (left, mid, right)

    def exit(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.flushinp()
        curses.endwin()

    def inputs(self):
        while self.shell.go:
            #raise RuntimeError('my bad')
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
                self.shell.on_key(key)

    @property
    def w(self):
        return curses.COLS

    @property
    def h(self):
        return curses.LINES


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        assert w >= 2 and h >= 2
        assert x >= 0 and x + w <= self.app.w
        assert y >= 0 and y + h <= self.app.h

        win = curses.newwin(h, w, y, x)
        win.keypad(True)
        win.box()
        self.border = win

        win = win.derwin(h - 2, w - 2, 1, 1)
        win.keypad(True)
        win.scrollok(True)
        self.content = win

        self.app.screen.refresh()
        self.border.refresh()

        self.newline = ''

    def print(self, txt='', end=True):
        self.content.addstr(f'{self.newline}{txt}')
        self.newline = '\n' if end else ''
        self.content.refresh()

    @property
    def x(self):
        return self.border.getbegyx()[1]

    @property
    def y(self):
        return self.border.getbegyx()[0]

    @property
    def w(self):
        return self.border.getmaxyx()[1]

    @property
    def h(self):
        return self.border.getmaxyx()[0]

    def set_pos(self, x, y):
        assert x >= 0 and x + self.w <= self.app.w
        assert y >= 0 and y + self.h <= self.app.h

        self.app.screen.clear()
        self.app.screen.refresh()
        self.border.mvwin(y, x)
        self.content.mvwin(y + 1, x + 1)
        self.border.refresh()

