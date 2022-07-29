import curses


class Application:
    def __init__(self):
        self.screen = curses.initscr()

    def run(self):
        curses.flushinp()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.set_escdelay(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    def done(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.flushinp()
        curses.endwin()

    def refresh(self):
        self.screen.refresh()

    def getch(self):
        return self.screen.getch()


class Window:
    def __init__(self, x, y, w, h):
        win = curses.newwin(h, w, y, x)
        win.keypad(True)
        win.box()
        self.border = win

        win = win.derwin(h - 2, w - 2, 1, 1)
        win.keypad(True)
        win.scrollok(True)
        self.content = win

    def print(self, txt, end):
        self.content.addstr(txt + '\n' if end else '')

    def refresh(self):
        self.border.refresh()
        self.content.refresh()

    #def scroll(self, lines):
    #    self.content.scroll(lines)

