import os
import sys


def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def cprint_at(row, col, text='', color=None, on_color=None, attrs=None, end='\n'):
    print_at(row, col, colored(text, color, on_color, attrs), end=end)


'''
keymode_settings_orig = None

def key_enable():
    fd = sys.stdin.fileno()
    keymode_settings_orig = termios.tcgetattr(fd)

    settings = keymode_settings_orig & ~termios.ICANON & ~termios.ECHO

    termios.tcsetattr(fd, termios.TCSAFLUSH, settings)

def key_disable():
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSAFLUSH, keymode_settings_orig)

#def key_hit():
#    if os.name == 'nt':
#        return msvcrt.kbhit()

def key_get():
    pass
'''



#
# The following code originally taken from:
#   https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window/10455937#10455937
#


if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

    else: # assume ANSI compatible
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

    else: # assume ANSI compatible
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()



#
# The following code originally taken from:
#   https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user/21659588#21659588
#

def _read_char():
    try:
        import termios

    except ImportError:
        # Non-POSIX; assume Windows
        import msvcrt
        return msvcrt.getch

    # POSIX
    import tty

    def getch():
        fd = sys.stdin.fileno()
        settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)

        return char

    return getch

'''read_char() is our actual function for export, which has resolved the proper implementation'''
read_char = _read_char()




#
# The following code originally taken from:
#   https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python
#

def print_at(row, col, text='', end='\n'):
    # use ANSI escape for positioning
    print('\033[{};{}H{}'.format(row, col, text), end=end)


if os.name == 'nt':
    # Windows console does not support ANSI sequences

    from ctypes import *
     
    STD_OUTPUT_HANDLE = -11
     
    class COORD(Structure):
        pass
     
    COORD._fields_ = [("X", c_short), ("Y", c_short)]
     
    def win_print_at(row, col, text, end='\n'):
        h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        windll.kernel32.SetConsoleCursorPosition(h, COORD(col, row))

        if end:
            text += end

        c = text.encode("windows-1252")
        windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)

    print_at = win_print_at

    



#
# The following code originally taken from:
#   https://gist.github.com/jtriley/1108174
#

import shlex
import struct
import platform
import subprocess
 

def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print("default")
        tuple_xy = (80, 25)      # default value
    return tuple_xy
 
 
def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass
 

def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass
 
 
def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
 



#
# The following code originally from termcolor pypi package:
# (MIT License)
#   Copyright (c) 2008-2011 Volvox Development Team
#   Author: Konstantin Lepa <konstantin.lepa@gmail.com>
#


ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )


COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 38))
            ))
        )


RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text


def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
    """Print colorize text.

    It accepts arguments of print function.
    """

    print((colored(text, color, on_color, attrs)), **kwargs)


