import win32con
import win32file
from win32console import *

from time import sleep


class Application:
    def __init__(self, shell):
        self.shell = shell

        self.console = PyConsoleScreenBufferType(win32file.CreateFile(
            "CONIN$",
            win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ,
            None,
            win32con.OPEN_EXISTING,
            0,
            0
        ))
        self.console.SetConsoleMode(ENABLE_WINDOW_INPUT | ENABLE_MOUSE_INPUT)
        self.buffer = CreateConsoleScreenBuffer()
        self.buffer.SetConsoleActiveScreenBuffer()

        size, _ = self.buffer.GetConsoleCursorInfo()
        self.buffer.SetConsoleCursorInfo(size, False)

        self.mpos = (0, 0) # mouse position

    def exit(self):
        size, _ = self.buffer.GetConsoleCursorInfo()
        self.buffer.SetConsoleCursorInfo(size, True)

        self.buffer.Close()

    def inputs(self):
        while self.shell.go:
            # poll for events before blocking and getting them
            # because the block prevents output from showing up
            while self.console.GetNumberOfConsoleInputEvents() < 1:
                sleep(0.01)

            for input in self.console.ReadConsoleInput(1):
                if input.EventType == KEY_EVENT:
                    if input.KeyDown:
                        if input.Char == '\0':
                            pass # FIXME - virtual key

                        elif input.Char == '\x03': # ctrl-c
                            raise KeyboardInterrupt()

                        else:
                            self.shell.on_key(ord(input.Char))

                elif input.EventType == MOUSE_EVENT:
                    flags = input.EventFlags # 1=push, 2=click, 4=scroll
                    pos = input.MousePosition
                    btn = input.ButtonState
                    scroll = -1 if btn & 4287102976 == 4287102976 else \
                              1 if btn & 7864320 == 7864320 else 0

                    if not scroll: # mouse position not reliable while scrolling
                        self.mpos = (pos.X, pos.Y)

                    self.shell.on_mouse(self.mpos[0], self.mpos[1],
                        True if btn & 1 == 1 else False,
                        True if btn & 4 == 4 else False,
                        True if btn & 2 == 2 else False,
                        scroll
                    )

    def write(self, x, y, txt):
        self.buffer.WriteConsoleOutputCharacter(txt, PyCOORDType(x, y))
        #dummy = PyINPUT_RECORDType(KEY_EVENT)
        #dummy.Char = '\0'
        #self.console.WriteConsoleInput([ dummy ])

    def clear(self):
        self.buffer.FillConsoleOutputCharacter(' ', self.w * self.h,
            PyCOORDType(0, 0))

    @property
    def w(self):
        return self.buffer.GetConsoleScreenBufferInfo()["Size"].X

    @property
    def h(self):
        return self.buffer.GetConsoleScreenBufferInfo()["Size"].Y


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        assert w >= 2 and h >= 2
        assert x >= 0 and x + w <= self.app.w
        assert y >= 0 and y + h <= self.app.h

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.view = [ ]
        self._border_()

    def write(self, x, y, txt):
        assert x >= 0 and x + len(txt) <= self.w
        assert y >= 0 and y < self.h

        self.app.write(self.x + x, self.y + y, txt)

        while y >= len(self.view):
            self.view.append('')

        line = self.view[y]
        if len(line) < x:
            self.view[y] = line + ' ' * (x - len(line)) + txt
        else:
            self.view[y] = line[:x] + txt + line[x+len(txt):]

    def write_all(self, x, y, lines):
        assert x >= 0 and x < self.w
        assert y >= 0 and y < self.h
        assert y + len(lines) < self.h

        for line in lines:
            self.write(x, y, line)
            y += 1

    def set_pos(self, x, y):
        assert x >= 0 and x + self.w <= self.app.w
        assert y >= 0 and y + self.h <= self.app.h
        if x == self.x and y == self.y: return

        self.app.clear()
        self.x = x
        self.y = y
        self._review_()

    def set_size(self, w, h):
        assert w >= 2 and self.x + w <= self.app.w
        assert h >= 2 and self.y + h <= self.app.h
        if w == self.w and h == self.h: return

        self.app.clear()
        self.w = w
        self.h = h
        self._border_()
        self._review_()

    def _border_(self):
        self.write(0, 0, '\u250c')
        self.write(1, 0, '\u2500' * (self.w - 2))
        self.write(self.w - 1, 0, '\u2510')

        for y in range(1, self.h):
            self.write(0, y, '\u2502')
            self.write(self.w - 1, y, '\u2502')

        self.write(0, self.h - 1, '\u2514')
        self.write(1, self.h - 1, '\u2500' * (self.w - 2))
        self.write(self.w - 1, self.h - 1, '\u2518')

    def _review_(self):
        for y in range(self.h):
            if y >= len(self.view): break
            self.app.write(self.x, self.y + y, self.view[y][:self.w])

