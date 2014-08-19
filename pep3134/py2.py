# -*- coding: utf-8 -*-


import sys

from .utils import prepare_raise


@prepare_raise
def raise_(error, traceback):
    error.__suppress_context__ = False
    error.__context__ = sys.exc_info()[1]
    error.__cause__ = None
    error.__traceback__ = traceback

    if traceback:
        raise error, None, traceback
    else:
        raise error


def raise_from(exc, cause):
    error = exc
    if isinstance(exc, type) and issubclass(exc, Exception):
        error = exc()

    error.__context__, error.__traceback__ = sys.exc_info()[1:]
    error.__suppress_context__ = True

    if isinstance(cause, type) and issubclass(cause, Exception):
        error.__cause__ = cause()
    elif cause is None or isinstance(cause, BaseException):
        error.__cause__ = cause
    else:
        raise TypeError("exception causes must derive from BaseException")
    raise error