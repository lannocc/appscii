from .backend import core

from threading import Thread, current_thread


class Application:
    def __init__(self):
        self.go = False
        self.error = None

        self.core = core.Application(self)
        self.windows = [ ]
        self.mouse = (False, False, False) # mouse buttons (left, mid, right)
        self.moving = None

    def exit(self):
        self.core.exit()
        if self.error:
            raise self.error

    def run(self):
        self.go = True

        self.inputs = Thread(target=self.wrap(self.core.inputs),
            name='inputs', daemon=True)
        self.inputs.start()

        self.on_run()

    def stop(self, error=None):
        if error:
            if self.error:
                try: raise self.error
                except Exception as e:
                    try: raise error
                    except Exception as e:
                        self.error = e

            else:
                self.error = error

        self.go = False

    def wrap(self, fn):
        def wrapped():
            try: fn()
            except Exception as e:
                try: raise ThreadException() from e
                except Exception as e: self.stop(e)

        return wrapped

    @property
    def w(self):
        return self.core.w

    @property
    def h(self):
        return self.core.h

    def on_run(self):
        #raise RuntimeError('yikes')

        #from time import sleep
        #sleep(1)
        #self.windows[0].move_to(42, 9)

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

        elif left and not self.mouse[0]: # left button pushed
            for win in self.windows:
                if x >= win.x and x < win.x + win.w \
                        and y >= win.y and y < win.y + win.h:
                    #win.on_mouse(x, y, left, mid, right, scroll)

                    self.moving = (win, x, y)
                    break

        self.mouse = (left, mid, right)

        # FIXME this is just for testing (assumes we have at least one window):
        self.windows[0].print(f'{x},{y}: {left},{mid},{right},{scroll}')


class ThreadException(Exception):
    def __init__(self):
        t = current_thread()
        super().__init__('from thread ' \
            + f'"{t.name}"' if t.name else f'{t.ident}')

