# -*- coding: utf-8 -*-


import sys

from .utils import prepare_raise, construct_exc_class


# noinspection PyUnusedLocal
@prepare_raise
def raise_(type_, value=None, traceback=None):  # pylint: disable=W0613
    prev_exc, prev_tb = sys.exc_info()[1:]
    proxy_class = construct_exc_class(type(type_))

    err = proxy_class(type_)
    err.__cause__ = None
    err.__suppress_context__ = False

    if getattr(prev_exc, "__proxy_exception__", False):
        prev_exc = prev_exc.with_traceback(prev_tb)
    err.__context__ = prev_exc

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

    if not getattr(cause, "__proxy_exception__", False):
        # noinspection PyBroadException
        try:
            raise_(cause)
        except:  # noqa pylint: disable=W0702
            cause = sys.exc_info()[1]
    cause = cause.with_traceback(None)

    # noinspection PyBroadException
    try:
        raise_(exc)
    except:  # noqa pylint: disable=W0702
        exc = sys.exc_info()[1]

    exc.__context__ = context
    exc.__suppress_context__ = True
    exc.__cause__ = cause

    raise exc
