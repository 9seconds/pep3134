# -*- coding: utf-8 -*-


import sys


if sys.version_info[0] == 2:
    from .py2 import raise_, raise_from
else:
    from .py3 import raise_, raise_from