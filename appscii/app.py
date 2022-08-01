from .backend import core

from threading import Thread, Event, current_thread


class Application:
    def __init__(self):
        self.go = False
        self.quit = Event()
        self.error = None

        self.core = core.Application(self)
        self.windows = [ ]
        self.mouse = (False, False, False) # mouse buttons (left, mid, right)
        self.moving = None
        self.sizing = None

    def exit(self):
        if self.core:
            self.core.exit()
            self.core = None

        if self.error:
            error = self.error
            self.error = None
            raise error

    def init(self):
        pass

    def run(self):
        self.go = True
        try:
            self.init()

            self.inputs = Thread(target=self.wrap(self.core.inputs),
                name='inputs', daemon=True)
            self.inputs.start()

            self.on_run()

        except Quit:
            pass

        finally:
            self.stop()
            self.exit()

    def stop(self, error=None):
        if error:
            if self.error:
                try: raise self.error
                except BaseException as e:
                    try: raise error
                    except BaseException as e:
                        self.error = e

            else:
                self.error = error

        self.go = False
        self.quit.set()

    def wrap(self, fn):
        def wrapped():
            try: fn()
            except BaseException as e:
                try: raise ThreadException() from e
                except Exception as e: self.stop(e)

        return wrapped

    def sleep(self, secs):
        if self.quit.wait(timeout=secs):
            raise Quit()

    @property
    def w(self):
        return self.core.w

    @property
    def h(self):
        return self.core.h

    def on_run(self):
        self.inputs.join()

    def on_key(self, key):
        if key == 27: # escape
            self.stop()

    def on_mouse(self, x, y, left, mid, right, scroll):
        if self.moving:
            win, mx, my = self.moving
            if not left:
                self.moving = None

            if x != mx or y != my:
                win.move_by(x - mx, y - my)
                if self.moving:
                    self.moving = (win, x, y)

        elif self.sizing:
            win, sxt, syt = self.sizing
            if not left:
                self.sizing = None

            if (sxt and x != sxt[0]) or (syt and y != syt[0]):
                mdx = 0
                mdy = 0
                sdx = 0
                sdy = 0

                if sxt:
                    if sxt[1]:
                        mdx = x - sxt[0]
                        sdx = -mdx
                    else:
                        sdx = x - sxt[0]

                if syt:
                    if syt[1]:
                        mdy = y - syt[0]
                        sdy = -mdy
                    else:
                        sdy = y - syt[0]

                if mdx or mdy:
                    win.move_by(mdx, mdy)

                win.size_by(sdx, sdy)

                if self.sizing:
                    self.sizing = (win,
                        (x, sxt[1]) if sxt else None,
                        (y, syt[1]) if syt else None)

        elif left and not self.mouse[0]: # left button pushed
            for win in self.windows:
                if x >= win.x and x < win.x + win.w \
                        and y >= win.y and y < win.y + win.h:
                    sx = (x, True) if x == win.x else \
                         (x, False) if x == win.x + win.w -1 else \
                         None
                    sy = (y, True) if y == win.y else \
                         (y, False) if y == win.y + win.h -1 else \
                         None

                    if sx or sy:
                        self.sizing = (win, sx, sy)

                    else:
                        self.moving = (win, x, y)

                    break

        elif scroll:
            for win in self.windows:
                if x >= win.x and x < win.x + win.w \
                        and y >= win.y and y < win.y + win.h:
                    if scroll < 0: win.text.down()
                    else: win.text.up()
                    break

        self.mouse = (left, mid, right)

        # FIXME this is just for testing (assumes we have at least one window):
        #self.windows[0].text.print(f'{x},{y}: {left},{mid},{right},{scroll}')


class Quit(Exception):
    pass


class ThreadException(Exception):
    def __init__(self):
        t = current_thread()
        super().__init__('from thread ' \
            + f'"{t.name}"' if t.name else f'{t.ident}')

