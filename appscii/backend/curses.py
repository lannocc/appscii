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
        curses.set_escdelay(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    def exit(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.flushinp()
        curses.endwin()

    def refresh(self):
        self.screen.refresh()

    def inputs(self):
        #from time import sleep
        while self.shell.go:
            #sleep(1)
            #raise RuntimeError('my bad')
            key = self.screen.getch()

            if key == curses.KEY_MOUSE:
                _, x, y, _, btn = curses.getmouse()
                self.shell.on_mouse(x, y,
                    1 if btn & curses.BUTTON1_PRESSED else \
                    2 if btn & curses.BUTTON1_RELEASED else \
                    3 if btn & curses.BUTTON1_CLICKED else \
                    4 if btn & curses.BUTTON1_DOUBLE_CLICKED else \
                    0,
                    1 if btn & curses.BUTTON2_PRESSED else \
                    2 if btn & curses.BUTTON2_RELEASED else \
                    3 if btn & curses.BUTTON2_CLICKED else \
                    4 if btn & curses.BUTTON2_DOUBLE_CLICKED else \
                    0,
                    1 if btn & curses.BUTTON3_PRESSED else \
                    2 if btn & curses.BUTTON3_RELEASED else \
                    3 if btn & curses.BUTTON3_CLICKED else \
                    4 if btn & curses.BUTTON3_DOUBLE_CLICKED else \
                    0,
                    1 if btn & curses.BUTTON4_PRESSED else \
                    -1 if btn & 2097152 else \
                    0
                )

            else:
                self.shell.on_key(key)


class Window:
    def __init__(self, app, x, y, w, h):
        win = curses.newwin(h, w, y, x)
        win.keypad(True)
        win.box()
        self.border = win

        win = win.derwin(h - 2, w - 2, 1, 1)
        win.keypad(True)
        win.scrollok(True)
        self.content = win

        self.newline = ''

    def print(self, txt, end):
        self.content.addstr(f'{self.newline}{txt}')
        self.newline = '\n' if end else ''

    def refresh(self):
        self.border.refresh()
        self.content.refresh()

    #def scroll(self, lines):
    #    self.content.scroll(lines)

