from . import *


def run():
    app = Application()
    try:
        win = Window(app, 30, 5, 42, 9)
        win.print('ESC to quit.')
        win.print('Click drag and scroll test mouse.')
        win.print("Here's something.", end=False)
        win.print(' And this continues the previous print and also wraps.')
        #win.print('And here is something else!')
        #win.print('And here is something else!')
        #win.print('And here is something else!')
        #win.print('And here is something else!')
        #win.print('And here is something else!')
        #win.print('Final thing.')

        #raise RuntimeError('oopsie')

        app.run()

    finally:
        app.exit()


if __name__ == '__main__':
    run()

