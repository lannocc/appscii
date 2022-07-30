import win32con
import win32file
from win32console import *
#import msvcrt


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
            #key = ord(msvcrt.getch())

            #if key == 3: # ctrl-c
            #    raise KeyboardInterrupt()

            #self.shell.on_key(key)

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


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def print(self, txt, end):
        self._write_(self.x + 1, self.y + 1, txt)

    def refresh(self):
        self._write_(self.x, self.y, '\u250c')
        self._write_(self.x + 1, self.y, '\u2500' * (self.w - 2))
        self._write_(self.x + self.w - 1, self.y, '\u2510')

        for y in range(self.y + 1, self.y + self.h):
            self._write_(self.x, y, '\u2502')
            self._write_(self.x + self.w - 1, y, '\u2502')

        self._write_(self.x, self.y + self.h - 1, '\u2514')
        self._write_(self.x + 1, self.y + self.h - 1, '\u2500' * (self.w - 2))
        self._write_(self.x + self.w - 1, self.y + self.h - 1, '\u2518')

    def _write_(self, x, y, txt):
        self.app.buffer.WriteConsoleOutputCharacter(txt, PyCOORDType(x, y))

