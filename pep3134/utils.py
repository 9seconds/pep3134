# -*- coding: utf-8 -*-


import sys
import functools


def construct_exc_class(cls):
    class ProxyException(cls):
        __slots__ = ("__original_exception__", "__fixed_traceback__")

        @property
        def __traceback__(self):
            if self.__fixed_traceback__:
                return self.__fixed_traceback__

            current_exc, current_tb = sys.exc_info()[1:]
            if current_exc is self:
                return current_tb

        def __init__(self, instance):
            self.__original_exception__ = instance
            self.__fixed_traceback__ = None

        def __getattribute__(self, item):
            if item == "__class__":
                return type(self.__original_exception__)
            return super(ProxyException, self).__getattribute__(item)

        def __repr__(self):
            return repr(self.__original_exception__)

        def __getattr__(self, item):
            return getattr(self.__original_exception__, item)

        def with_traceback(self, tb):
            self.__fixed_traceback__ = tb

    ProxyException.__name__ = cls.__name__

    return ProxyException


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
