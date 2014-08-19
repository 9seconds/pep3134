# -*- coding: utf-8 -*-


import inspect
import functools



def prepare_raise(func):
    @functools.wraps(func)
    def decorator(tp, value=None, traceback=None):
        if value is not None and isinstance(tp, Exception):
            raise TypeError("instance exception may not have a separate value")

        if value is None:
            if isinstance(tp, Exception):
                error = tp
            else:
                error = tp()
        else:
            error = tp(value)
        func(error, traceback)

    return decorator


def exec_in_frame_context(code, frame_number=1):
    frame = inspect.stack()[1][0]
    locals = frame.f_locals
    globals = frame.f_globals
    exec("""exec code in locals, globals""")