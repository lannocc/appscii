

class FlowText:
    def __init__(self, w, h, notify=None, words=False, align=-1):
        assert w >= 0 and h >= 0
        self.w = w
        self.h = h
        self.notify = notify
        self.words = words
        self.align = align

        self.prints = [ ]
        self.enter = True

        self.lines = [ ]
        self.scroll = -1
        self.flow = (0, 0)

    def resize(self, w, h):
        assert w >= 0 and h >= 0
        if w == self.w and h == self.h: return
        self.h = h
        if w != self.w:
            self.w = w
            self.reflow(True)
        else:
            if self.notify: self.notify(self)

    def word_wrap(self, words=None):
        if words is None:
            self.words = not self.words
            self.reflow(True)

        elif words != self.words:
            self.words = words
            self.reflow(True)

    def left(self):
        if self.align == -1: return
        self.align = -1
        if self.notify: self.notify(self)

    def center(self):
        if self.align == 0: return
        self.align = 0
        if self.notify: self.notify(self)

    def right(self):
        if self.align == 1: return
        self.align = 1
        if self.notify: self.notify(self)

    def top(self):
        if self.scroll == 0: return
        self.scroll = 0
        if self.notify: self.notify(self)

    def bottom(self):
        if self.scroll < 0: return
        self.scroll = -1
        if self.notify: self.notify(self)

    def up(self, lines=1):
        assert lines > 0
        if self.scroll == 0: return
        diff = len(self.lines) - self.h
        if diff > 0:
            self.scroll -= lines
            if self.scroll > diff:
                self.scroll = diff
            elif self.scroll < 0:
                self.scroll = 0
        else:
            self.scroll = 0
        if self.notify: self.notify(self)

    def down(self, lines=1):
        assert lines > 0
        if self.scroll < 0: return
        diff = len(self.lines) - self.h
        if diff > 0:
            self.scroll += lines
            if self.scroll > diff:
                self.scroll = diff
        else:
            self.scroll = -1
        if self.notify: self.notify(self)

    def print(self, txt='', enter=True):
        if not isinstance(txt, str):
            txt = f'{txt}'

        prints = [ ]

        while '\n' in txt:
            idx = txt.index('\n')
            prints.append(txt[:idx])
            txt = txt[idx+1:]

        prints.append(txt)

        if self.enter:
            self.prints.extend(prints)

        else:
            self.prints[-1] += prints[0]
            self.prints.extend(prints[1:])

        self.enter = enter
        self.reflow()

    def reflow(self, reset=False):
        if reset:
            self.flow = (0, 0)

        if self.w < 1 or self.h < 1:
            return

        if self.flow[0] and self.flow[1]:
            self.lines = self.lines[:self.flow[1]]

        elif self.lines:
            self.lines = [ ]

        for entry in self.prints[self.flow[0]:]:
            while len(entry) > self.w:
                chunk = entry[:self.w]

                if self.words and entry[self.w] != ' ' and chunk[-1] != ' ' \
                        and ' ' in chunk:
                    idx = chunk.rindex(' ')
                    chunk = entry[:idx]
                    entry = entry[idx+1:]

                else:
                    entry = entry[self.w:]

                self.lines.append(chunk)

            self.lines.append(entry)

        if self.enter:
            self.flow = (len(self.prints), len(self.lines))

        else:
            self.flow = (len(self.prints) - 1, len(self.lines) - 1)

        if self.notify:
            self.notify(self)

    def view(self):
        if self.w < 1 or self.h < 1:
            return None

        if self.scroll < 0:
            showing = self.lines[-self.h:]

        else:
            showing = self.lines[self.scroll:self.scroll+self.h]

        while len(showing) < self.h:
            showing.append('')

        if self.align < 0: # left
            return [ line + ' ' * (self.w - len(line)) for line in showing ]

        elif self.align > 0: # right
            return [ ' ' * (self.w - len(line)) + line for line in showing ]

        else: # center
            view = [ ]
            lpad = True

            for line in showing:
                diff = self.w - len(line)
                if diff:
                    left = ' ' * (diff // 2)
                    right = left
                    if diff % 2:
                        if lpad: left += ' '
                        else: right += ' '
                        lpad = not lpad

                    view.append(left + line + right)

                else:
                    view.append(line)

            return view

