from .backend import core

from threading import Thread, current_thread


class Application:
    def __init__(self):
        self.go = False
        self.error = None

        self.core = core.Application(self)
        self.windows = [ ]

    def exit(self):
        self.core.exit()
        if self.error:
            raise self.error

    def run(self):
        self.go = True

        self.inputs = Thread(target=self.wrap(self.core.inputs),
            name='inputs', daemon=True)
        self.inputs.start()

        self.refresh_all()

        self.on_run()

    def stop(self, error=None):
        if error:
            if self.error:
                try:
                    raise self.error
                except Exception as e:
                    try:
                        raise error
                    except Exception as e:
                        self.error = e

            else:
                self.error = error

        self.go = False

    def wrap(self, fn):
        def wrapped():
            try:
                fn()

            except Exception as e:
                try: raise ThreadException() from e
                except Exception as e: self.stop(e)

        return wrapped

    def refresh(self):
        self.core.refresh()

    def refresh_all(self):
        self.refresh()
        for win in self.windows:
            win.refresh()

    def on_run(self):
        #raise RuntimeError('yikes')
        self.inputs.join()

    def on_key(self, key):
        if key == 27: # escape
            self.stop()

    def on_mouse(self, x, y, left, mid, right, scroll):
        # this is just for testing:
        self.windows[0].print(f'{x},{y}: {left},{mid},{right},{scroll}')
        self.windows[0].refresh()
        #self.refresh_all()
        pass


class ThreadException(Exception):
    def __init__(self):
        t = current_thread()
        super().__init__('from thread ' \
            + f'"{t.name}"' if t.name else f'{t.ident}')

