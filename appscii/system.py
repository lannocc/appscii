import platform
import os


windows = platform.system == 'Windows' or os.name == 'nt'
linux = platform.system == 'Linux'
macos = platform.system == 'Darwin'

