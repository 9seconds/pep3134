# -*- coding: utf-8 -*-


import sys

from .utils import prepare_raise


def reraise():
    raise_(*sys.exc_info())


@prepare_raise
def raise_(error, traceback):
    if error.__traceback__ is not traceback:
        raise error.with_traceback(traceback)
    raise error


def raise_from(error, cause):
    raise error from cause
