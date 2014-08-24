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
    except IOError:
        ctype, cexc, ctb = sys.exc_info()

        assert isinstance(cexc, IOError)
        assert issubclass(ctype, IOError)
        assert cexc.__context__ is None
        assert cexc.__suppress_context__ == False
        assert cexc.__traceback__ is ctb


def test_assert_with_proper_callback():
    try:
        raise TypeError
    except TypeError:
        traceback = sys.exc_info()[2]

        try:
            raise_(IOError, None, traceback)
            assert False
        except IOError:
            ctype, cexc1, ctb1 = sys.exc_info()

            assert ctb1 is not traceback
            assert isinstance(cexc1, IOError)
            assert issubclass(ctype, IOError)
            assert isinstance(cexc1.__context__, TypeError)
            assert cexc1.__suppress_context__ == False

            assert get_tb(traceback)[0] == get_tb(ctb1)[-1]

            try:
                raise_(IOError, None, None)
                assert False
            except IOError:
                ctype, cexc2, ctb2 = sys.exc_info()

                assert ctb2 is not ctb1
                assert ctb1 is not traceback
                assert get_tb(traceback)[0] != get_tb(ctb2)[-1]
                assert cexc2.__traceback__ is ctb2
                assert cexc2.__traceback__ is not ctb1

@pytest.mark.parametrize("input_, expect_", (
    ((KeyError, None, None), "KeyError()"),
    ((KeyError, "OK", None), "KeyError('OK',)"),
    ((KeyError("OK"), None), "KeyError('OK',)")
))
def test_repr(input_, expect_):
    try:
        raise_(*input_)
        assert False
    except KeyError as exc:
        assert repr(exc) == expect_


def test_raise_fault():
    with pytest.raises(TypeError):
        raise_(IOError("OK"), "NOK", None)


def test_raise_custom():
    class CustomException(Exception):

        def parameter(self):
            return 1

    try:
        raise_(CustomException())
        assert False
    except CustomException:
        type_, value_, tb_ = sys.exc_info()

        assert issubclass(type_, CustomException)
        assert isinstance(value_, CustomException)
        assert value_.parameter() == 1


@pytest.mark.parametrize("input_, cause_", (
    (IOError("Hello"), KeyError("OKAY")),
    (IOError("Hello"), KeyError),
    (IOError, KeyError("OKAY")),
    (IOError, KeyError),
    (IOError, None)
))
def test_raise_from(input_, cause_):
    with pytest.raises(IOError):
        raise_from(input_, cause_)


@pytest.mark.parametrize("input_, cause_", (
    (IOError("Hello"), "str"),
    (IOError("Hello"), set)
))
def test_raise_from_fail(input_, cause_):
    with pytest.raises(TypeError):
        raise_from(input_, cause_)


def test_raise_from_proxy_exc():
    try:
        raise_(TypeError, "OK")
        assert False
    except TypeError:
        cause, cause_tb = sys.exc_info()[1:]

    try:
        raise_from(IOError, cause)
    except IOError:
        exc, exc_tb = sys.exc_info()[1:]

    assert exc.__suppress_context__
    assert exc.__context__ is None
    assert exc.__cause__ is cause
    assert exc.__traceback__ is exc_tb
    assert exc.__cause__.__traceback__ is cause_tb


def test_raise_from_ordinary_exc():
    try:
        raise TypeError("OK")
    except TypeError:
        cause, cause_tb = sys.exc_info()[1:]

    try:
        raise_from(IOError, cause)
        assert False
    except IOError:
        exc, exc_tb = sys.exc_info()[1:]

    if sys.version_info[0] == 2:
        assert exc.__cause__ is not cause
        assert hasattr(exc.__cause__, "__pep3134__")
    else:
        assert exc.__cause__ is cause
    assert exc.__suppress_context__
    assert exc.__context__ is None
    assert exc.__traceback__ is exc_tb
    assert exc.__cause__.__traceback__ is cause_tb


def test_raise_from_none():
    try:
        raise_from(IOError, None)
        assert False
    except IOError:
        exc, exc_tb = sys.exc_info()[1:]

    assert exc.__suppress_context__
    assert exc.__context__ is None
    assert exc.__cause__ is None


def test_reraise():
    try:
        raise_from(IOError, KeyError)
        assert False
    except IOError:
        try:
            reraise()
        except IOError:
            reraised, reraised_tb = sys.exc_info()[1:]

        assert not reraised.__suppress_context__
        assert reraised.__cause__ is None
