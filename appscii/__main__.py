from . import *


def run():
    app = Application()
    try:
        win = Window(app, 30, 5, 42, 9)
        win.print('ESC to quit.')
        #win.print('Hold click and drag me.')
        #win.print('Scroll wheel to scroll me.')
        #for i in range(10):
        #    win.print(f'{i+1}. This is a line of text.')
        #win.scroll(-3)

        app.run()

    finally:
        app.done()


if __name__ == '__main__':
    run()

