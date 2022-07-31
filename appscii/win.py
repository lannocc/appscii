from .backend import core


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.core = core.Window(app.core, x, y, w, h)
        self.app.windows.append(self)

    def print(self, txt='', end=True):
        self.core.print(txt, end)

    @property
    def x(self):
        return self.core.x

    @property
    def y(self):
        return self.core.y

    @property
    def w(self):
        return self.core.w

    @property
    def h(self):
        return self.core.h

    def move_to(self, x, y):
        self.core.set_pos(x, y)

    def move_by(self, dx, dy):
        x = self.x + dx
        if x < 0: x = 0
        elif x + self.w > self.app.w: x = self.app.w - self.w

        y = self.y + dy
        if y < 0: y = 0
        elif y + self.h > self.app.h: y = self.app.h - self.h

        self.move_to(x, y)

    #def on_mouse(self, x, y, left, mid, right, scroll):
    #    # FIXME this is just for testing:
    #    self.print(f'{x},{y}: {left},{mid},{right},{scroll}')

