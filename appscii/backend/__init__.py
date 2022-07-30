import platform
import os


windows = platform.system == 'Windows' or os.name == 'nt'
linux = platform.system == 'Linux'
macos = platform.system == 'Darwin'


if windows:
    from . import win32 as core

else:
    from . import curses as core

