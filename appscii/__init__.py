from .__version__ import __version__
from . import system
if system.windows:
    raise NotImplementedError('windows support coming soon')
else:
    from .backend import curses as backend


class Application:
    def __init__(self):
        self.core = backend.Application()
        self.windows = [ ]

    def run(self):
        self.core.run()

        while True:
            self.refresh_all()

            key = self.getch()
            if key == 27: # escape
                break

            self.main()

    def main(self):
        pass # subclasses may override

    def done(self):
        self.core.done()

    def refresh(self):
        self.core.refresh()

    def refresh_all(self):
        self.refresh()
        for win in self.windows:
            win.refresh()

    def getch(self):
        return self.core.getch()


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.core = backend.Window(x, y, w, h)
        self.app.windows.append(self)

    def refresh(self):
        self.core.refresh()

    def print(self, txt='', end=True):
        self.core.print(txt, end)

    #def scroll(self, lines):
    #    self.core.scroll(lines)

