# -*- coding: utf-8 -*-


import sys
import traceback

import pytest

from pep3134 import raise_, raise_from, reraise


def get_tb(traceback_):
    return [tuple(entry[:2]) for entry in traceback.extract_tb(traceback_)]


@pytest.mark.parametrize("input_", (
    (IOError, None, None),
    (IOError, "OKAY", None)
))
def test_simple_raise(input_):
    try:
        raise_(IOError)
        assert False
    except:
        ctype, cexc, ctb = sys.exc_info()

        assert isinstance(cexc, IOError)
        assert issubclass(ctype, IOError)
        assert cexc.__context__ is None
        assert cexc.__suppress_context__ == False
        assert cexc.__traceback__ is ctb


def test_assert_with_proper_callback():
    try:
        raise TypeError
    except:
        traceback = sys.exc_info()[2]

    try:
        raise_(IOError, None, traceback)
    except:
        ctype, cexc1, ctb1 = sys.exc_info()

        assert isinstance(cexc1, IOError)
        assert issubclass(ctype, IOError)
        assert isinstance(cexc1.__context__, TypeError)
        assert cexc1.__suppress_context__ == False
        assert cexc1.__traceback__ is ctb1
        assert get_tb(traceback)[0] == get_tb(ctb1)[-1]

    try:
        raise_(IOError, None, None)
    except:
        ctype, cexc2, ctb2 = sys.exc_info()

        assert get_tb(traceback)[0] != get_tb(ctb2)[-1]
        assert cexc2.__traceback__ is ctb2
        assert cexc2.__traceback__ is not ctb1
        if sys.version_info[0] == 2:
            assert cexc1.__traceback__ is None
        else:
            assert cexc1.__traceback__ is ctb1


@pytest.mark.parametrize("input_, expect_", (
    ((IOError, None, None), "IOError()"),
    ((IOError, "OK", None), "IOError('OK',)"),
    ((IOError("OK"), None), "IOError('OK',)")
))
def test_repr(input_, expect_):
    try:
        raise_(*input_)
    except IOError as exc:
        assert repr(exc) == expect_
