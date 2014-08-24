# -*- coding: utf-8 -*-


import sys

from .utils import prepare_raise, construct_exc_class


@prepare_raise
def raise_(error, traceback):
    prev_exc = sys.exc_info()[1]
    proxy_class = construct_exc_class(type(error))

    err = proxy_class(error)
    err.__cause__ = None
    err.__context__ = prev_exc
    err.__suppress_context__ = False

    if traceback:
        raise err.with_traceback(traceback), None, traceback
    else:
        raise err


def raise_from(exc, cause):
    context = sys.exc_info()[1]

    incorrect_cause = not (
        (isinstance(cause, type) and issubclass(cause, Exception)) or
        cause is None
        or isinstance(cause, BaseException)
    )
    if incorrect_cause:
        raise TypeError("exception causes must derive from BaseException")

    try:
        raise_(cause)
    except:
        cause = sys.exc_info()[1]
    try:
        raise_(exc)
    except:
        exc = sys.exc_info()[1]

    exc.__context__ = context
    exc.__suppress_context__ = True
    exc.__cause__ = cause

    raise exc
