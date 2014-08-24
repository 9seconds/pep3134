# -*- coding: utf-8 -*-


import sys


if sys.version_info[0] == 2:
    from .py2 import raise_, raise_from
else:
    from .py3 import raise_, raise_from


def reraise():
    raise_(*sys.exc_info())


# silence pyflakes
assert reraise
assert raise_
assert raise_from
