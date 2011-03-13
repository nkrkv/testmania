# -*- coding: utf-8; -*-

"""
Module exposes ``TestCase.assert*`` methods as plain functions with corresponding
names in ``pep8_naming_fashion``.

>>> from testmania.pep8 import assert_almost_equal    
>>> assert_almost_equal(0.7, 0.701, places=2)

All assertions of Python 2.7+ :py:mod:`unittest` are exposed even if you're on
Python 2.6 or lower. In that case they are taken from 
`unittest2 <http://pypi.python.org/pypi/unittest2/>`_ backport.

For full list of functions and their docs refer official documentation.

"""

import sys
import re


__all__ = []


if sys.version_info[0:2] >= (2, 7):
    # Python 2.7+
    import unittest
else:
    import unittest2 as unittest


#
# Borrowed from nose:
#
# Expose assert* from unittest.TestCase
# - give them pep8 style names
#
caps = re.compile('([A-Z])')

def pep8(name):
    return caps.sub(lambda m: '_' + m.groups()[0].lower(), name)

class Dummy(unittest.TestCase):
    def nop():
        pass
_t = Dummy('nop')

for at in [ at for at in dir(_t)
            if at.startswith('assert') and not '_' in at ]:
    pepd = pep8(at)
    vars()[pepd] = getattr(_t, at)
    __all__.append(pepd)

del Dummy
del _t
del pep8
