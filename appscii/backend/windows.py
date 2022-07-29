import win32con
import win32file
from win32console import *
import msvcrt


class Application:
    def __init__(self):
        #AllocConsole()
        #self.stdout = GetStdHandle(STD_OUTPUT_HANDLE)
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

    def run(self):
        size, _ = self.buffer.GetConsoleCursorInfo()
        self.buffer.SetConsoleCursorInfo(size, False)

    def done(self):
        #FreeConsole()
        self.buffer.Close()

    def refresh(self):
        pass

    def getch(self):
        return ord(msvcrt.getch())


class Window:
    def __init__(self, app, x, y, w, h):
        self.app = app
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def print(self, txt, end):
        #self.app.buffer.WriteConsole(txt + '\n' if end else '')
        self.app.buffer.WriteConsoleOutputCharacter(txt,
            PyCOORDType(self.x + 1, self.y + 1))

    def refresh(self):
        self.app.buffer.WriteConsoleOutputCharacter('\u250c',
            PyCOORDType(self.x, self.y))
        self.app.buffer.WriteConsoleOutputCharacter('\u2500' * (self.w - 2),
            PyCOORDType(self.x + 1, self.y))
        self.app.buffer.WriteConsoleOutputCharacter('\u2510',
            PyCOORDType(self.x + self.w - 1, self.y))

        for y in range(self.y + 1, self.y + self.h):
            self.app.buffer.WriteConsoleOutputCharacter('\u2502',
                PyCOORDType(self.x, y))
            self.app.buffer.WriteConsoleOutputCharacter('\u2502',
                PyCOORDType(self.x + self.w - 1, y))

        self.app.buffer.WriteConsoleOutputCharacter('\u2514',
            PyCOORDType(self.x, self.y + self.h - 1))
        self.app.buffer.WriteConsoleOutputCharacter('\u2500' * (self.w - 2),
            PyCOORDType(self.x + 1, self.y + self.h - 1))
        self.app.buffer.WriteConsoleOutputCharacter('\u2518',
            PyCOORDType(self.x + self.w - 1, self.y + self.h - 1))

