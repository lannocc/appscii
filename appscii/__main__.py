from . import *


def run():
    app = Application()
    try:
        win = Window(app, 30, 5, 42, 9)
        win.text.word_wrap()
        win.text.top()
        win.text.print('ESC to quit.')
        win.text.print('Click drag and scroll to test mouse.')
        win.text.print()
        win.text.print("Here's something.", enter=False)
        win.text.print(' And this continues the previous print and also wraps.')
        for i in range(1, 11):
            win.text.print()
            win.text.print(i, enter=False)
            win.text.print('. This is a line of text that goes and continues' \
                + ' and keeps going some more just to see how it all works.')

        def on_run():
            while app.go:
                app.sleep(1)
                win.text.center()
                app.sleep(1)
                win.text.right()
                app.sleep(1)
                win.text.left()
        app.on_run = on_run

        #raise RuntimeError('__main__ test')
        app.run()

    finally:
        app.exit()


if __name__ == '__main__':
    run()

