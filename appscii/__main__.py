from . import *


def run():
    app = Application()
    try:
        win1 = Window(app, 30, 5, 42, 9)
        win1.text.word_wrap()
        win1.text.top()
        win1.text.print('ESC to quit.')
        win1.text.print('Click drag and scroll to test mouse.')
        win1.text.print()
        win1.text.print("Here's something. ", enter=False)
        win1.text.print('And this continues the previous print and also wraps.')
        for i in range(1, 11):
            win1.text.print()
            win1.text.print(i, enter=False)
            win1.text.print('. This is a line of text that goes and continues' \
                + ' and keeps going some more just to see how it all works.')

        win2 = Window(app, 3, 3, 22, 3)
        win2.text.print('something else')

        def on_run():
            while app.go:
                app.sleep(1)
                win1.text.center()
                app.sleep(1)
                win1.text.right()
                app.sleep(1)
                win1.text.left()
        app.on_run = on_run

        #raise RuntimeError('__main__ test')
        app.run()

    finally:
        app.exit()


if __name__ == '__main__':
    run()

