from .common import Window
from .matrix import CharMap

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

        self.matrix = CharMap(self.w, self.h)
        self.mpos = (0, 0) # mouse position

    def exit(self):
        size, _ = self.buffer.GetConsoleCursorInfo()
        self.buffer.SetConsoleCursorInfo(size, True)

        self.buffer.Close()

    @property
    def w(self):
        return self.buffer.GetConsoleScreenBufferInfo()["Size"].X

    @property
    def h(self):
        return self.buffer.GetConsoleScreenBufferInfo()["Size"].Y

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

    def clear(self):
        self.buffer.FillConsoleOutputCharacter(' ', self.w * self.h,
            PyCOORDType(0, 0))

    def write(self, x, y, txt):
        self.buffer.WriteConsoleOutputCharacter(txt, PyCOORDType(x, y))

    def refresh(self):
        for y in range(self.matrix.h):
            chars = self.matrix.chars[y]
            changes = self.matrix.changes[y]

            for x in range(self.matrix.w):
                if changes[x]:
                    c = chars[x]
                    self.buffer.WriteConsoleOutputCharacter(
                        '.' if c is None else c, PyCOORDType(x, y))
                    changes[x] = False

