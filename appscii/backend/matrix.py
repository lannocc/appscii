

class CharMap:
    def __init__(self, w, h, fill=' '):
        assert w >= 0
        assert h >= 0
        assert fill is None or (isinstance(fill, str) and len(fill) == 1)

        self.w = w
        self.h = h

        self.chars = [ [ fill for x in range(w) ] for y in range(h) ]
        self.changes = [ [ True for x in range(w) ] for y in range(h) ]

    def set_size(self, w, h, fill=' '):
        if w == self.w and h == self.h: return
        assert w >= 0 and h >= 0

        if h > self.h:
            self.chars.extend(
                [ [ fill for x in range(w) ] for y in range(self.h, h) ])
            self.changes.extend(
                [ [ True for x in range(w) ] for y in range(self.h, h) ])

        elif h < self.h:
            self.chars = self.chars[:h]
            self.changes = self.changes[:h]

        if w > self.w:
            for row in self.chars[:min(self.h, h)]:
                row.extend([ fill for x in range(self.w, w) ])
            for row in self.changes[:min(self.h, h)]:
                row.extend([ True for x in range(self.w, w) ])

        elif w < self.w:
            for row in self.chars[:min(self.h, h)]:
                del row[w:]
            for row in self.changes[:min(self.h, h)]:
                del row[w:]

        self.w = w
        self.h = h

    def set(self, c, x, y):
        assert c is None or (isinstance(c, str) and len(c) == 1)
        assert x >= 0 and x < self.w
        assert y >= 0 and y < self.h
        if self.chars[y][x] == c: return

        self.chars[y][x] = c
        self.changes[y][x] = True

    def fill(self, c, x, y, w, h):
        assert c is None or (isinstance(c, str) and len(c) == 1)
        assert x >= 0 and x + w <= self.w
        assert y >= 0 and y + h <= self.h

        for cy in range(y, y + h):
            chars = self.chars[cy]
            changes = self.changes[cy]

            for cx in range(x, x + w):
                if chars[cx] != c:
                    chars[cx] = c
                    changes[cx] = True

    def merge(self, matrix, x=0, y=0):
        assert x >= 0 and x + matrix.w <= self.w
        assert y >= 0 and y + matrix.h <= self.h

        # FIXME: consider only changed items of matrix then clear changes?

        for cy in range(y, y + matrix.h):
            chars = self.chars[cy]
            changes = self.changes[cy]
            mchars = matrix.chars[cy - y]

            for cx in range(x, x + matrix.w):
                mchar = mchars[cx - x]

                if mchar is not None and chars[cx] != mchar:
                    chars[cx] = mchar
                    changes[cx] = True

    def debug_chars(self):
        return '\n'.join([
            ''.join([ c for c in line ])
            for line in self.chars
        ])

    def debug_changes(self):
        return '\n'.join([
            ''.join([ '#' if c else '.' for c in line ])
            for line in self.changes
        ])

