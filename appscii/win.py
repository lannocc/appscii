from .backend import core


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.core = core.Window(app.core, x, y, w, h)
        self.app.windows.append(self)

    def refresh(self):
        self.core.refresh()

    def print(self, txt='', end=True):
        self.core.print(txt, end)

    #def scroll(self, lines):
    #    self.core.scroll(lines)

