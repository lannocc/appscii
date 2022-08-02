from .backend import core
from .helper import FlowText


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.core = core.Window(app.core, x, y, w, h)
        self.text = FlowText(w - 2, h - 2, self.on_flow)
        self.app._attach_(self)

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

    def _focus_(self):
        self.active = True
        self.core.frame(True)

    def _unfocus_(self):
        self.active = False
        self.core.frame(False)

    def collides(self, x, y):
        return x >= self.x and x < self.x + self.w \
            and y >= self.y and y < self.y + self.h

    def move_to(self, x, y):
        self.core.set_pos(x, y)
        self.app.redraw()

    def move_by(self, dx, dy):
        x = self.x + dx
        if x < 0: x = 0
        elif x + self.w > self.app.w: x = self.app.w - self.w

        y = self.y + dy
        if y < 0: y = 0
        elif y + self.h > self.app.h: y = self.app.h - self.h

        self.move_to(x, y)

    def size_to(self, w, h):
        self.core.set_size(w, h)
        self.text.resize(w - 2, h - 2)
        self.core.frame(self.active)
        self.app.redraw()

    def size_by(self, dw, dh):
        w = self.w + dw
        if w < 2: w = 2
        elif self.x + w > self.app.w: w = self.app.w - self.x

        h = self.h + dh
        if h < 2: h = 2
        elif self.y + h > self.app.h: h = self.app.h - self.y

        self.size_to(w, h)

    def on_flow(self, flow):
        assert flow == self.text
        view = flow.view()
        if view is None: return
        self.core.write_all(1, 1, view)
        self.app.redraw()

