import win32con
import win32file
from win32console import *


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

    def exit(self):
        size, _ = self.buffer.GetConsoleCursorInfo()
        self.buffer.SetConsoleCursorInfo(size, True)

        self.buffer.Close()

    def refresh(self):
        pass

    def inputs(self):
        while self.shell.go:
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
                    #self.shell.on_mouse(flags, btn, pos)
                    self.shell.on_mouse(pos.X, pos.Y,
                        True if btn & 1 == 1 else False,
                        True if btn & 4 == 4 else False,
                        True if btn & 2 == 2 else False,
                        -1 if btn & 4287102976 == 4287102976 else \
                        1 if btn & 7864320 == 7864320 else \
                        0
                    )

    def write(self, x, y, txt):
        self.buffer.WriteConsoleOutputCharacter(txt, PyCOORDType(x, y))


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.cur = [0, 0]
        self.buf = [ ]

        self._border_()

    def print(self, txt='', end=True):
        assert self.w > 2 and self.h > 2
        #self._write_(1, 1, txt)

        lines = [ ]
        w = self.w - 2
        x = self.cur[0]

        while len(txt) > w - x or '\n' in txt:
            if '\n' in txt and txt.index('\n') < w - x:
                lines.append(txt[:txt.index('\n')])
                txt = txt[txt.index('\n')+1:]

            else:
                lines.append(txt[:w-x])
                txt = txt[w-x:]

            x = 0

        lines.append(txt)

        if self.cur[0] > 0 and self.buf:
            self.buf[-1] += lines[0]
            self.buf.extend(lines[1:])

        else:
            self.buf.extend(lines)

        if len(self.buf) > self.h - 2:
            self.buf = self.buf[-(self.h-2):]
            for y, txt in enumerate(self.buf):
                self._write_(1, y + 1, txt + ' ' * (w - len(txt)))

        else:
            x = self.cur[0]
            for y, txt in enumerate(lines):
                self._write_(1 + x, 1 + self.cur[1] + y, txt)
                x = 0

        self.cur[0] = 0 if end else len(self.buf[-1])
        self.cur[1] = len(self.buf) - (0 if end else 1)

    def refresh(self):
        pass

    def _border_(self):
        self._write_(0, 0, '\u250c')
        self._write_(1, 0, '\u2500' * (self.w - 2))
        self._write_(self.w - 1, 0, '\u2510')

        for y in range(1, self.h):
            self._write_(0, y, '\u2502')
            self._write_(self.w - 1, y, '\u2502')

        self._write_(0, self.h - 1, '\u2514')
        self._write_(1, self.h - 1, '\u2500' * (self.w - 2))
        self._write_(self.w - 1, self.h - 1, '\u2518')

    def _write_(self, x, y, txt):
        assert x >= 0 and x + len(txt) <= self.w
        assert y >= 0 and y < self.h

        self.app.write(self.x + x, self.y + y, txt)

