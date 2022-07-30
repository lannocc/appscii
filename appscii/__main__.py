from . import *


def run():
    app = Application()
    try:
        win = Window(app, 30, 5, 42, 9)
        win.print('ESC to quit.')
        win.print('Click drag and scroll test mouse.')

        #raise RuntimeError('oopsie')

        app.run()

    finally:
        app.exit()


if __name__ == '__main__':
    run()

