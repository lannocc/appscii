from .matrix import CharMap


class Window:
    def __init__(self, app, x, y, w, h):
        assert x >= 0 and x + w <= app.w
        assert y >= 0 and y + h <= app.h
        assert w >= 2
        assert h >= 2

        self.app = app
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.matrix = CharMap(w, h)

    def set_pos(self, x, y):
        assert x >= 0 and x + self.w <= self.app.w
        assert y >= 0 and y + self.h <= self.app.h

        self.x = x
        self.y = y

    def set_size(self, w, h):
        if w == self.w and h == self.h: return
        assert w >= 2
        assert h >= 2

        self.w = w
        self.h = h

        self.matrix.set_size(w, h)

    def frame(self, active=True):
        tl = '\u2554' if active else '\u250c'
        t = '\u2550' if active else '\u2500'
        tr = '\u2557' if active else '\u2510'
        l = '\u2551' if active else '\u2502'
        r = '\u2551' if active else '\u2502'
        bl = '\u255a' if active else '\u2514'
        b = '\u2550' if active else '\u2500'
        br = '\u255d' if active else '\u2518'

        self.matrix.set(tl, 0, 0)
        self.matrix.fill(t, 1, 0, self.w - 2, 1)
        self.matrix.set(tr, self.w - 1, 0)
        self.matrix.fill(l, 0, 1, 1, self.h - 2)
        self.matrix.fill(r, self.w - 1, 1, 1, self.h - 2)
        self.matrix.set(bl, 0, self.h - 1)
        self.matrix.fill(b, 1, self.h - 1, self.w -2, 1)
        self.matrix.set(br, self.w - 1, self.h - 1)

    def write(self, x, y, txt):
        assert x >= 0 and x + len(txt) <= self.w
        assert y >= 0 and y < self.h

        for tx, c in enumerate(txt):
            self.matrix.set(c, x + tx, y)

    def write_all(self, x, y, lines):
        assert x >= 0 and x < self.w
        assert y >= 0 and y < self.h
        assert y + len(lines) < self.h

        for line in lines:
            self.write(x, y, line)
            y += 1

