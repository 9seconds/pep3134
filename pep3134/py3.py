# -*- coding: utf-8 -*-


from .utils import prepare_raise


# noinspection PyUnusedLocal
@prepare_raise
def raise_(type_, value=None, traceback=None):
    if type_.__traceback__ is not traceback:
        raise type_.with_traceback(traceback)
    raise type_


def raise_from(error, cause):
    raise error from cause
