Testmania |version| documnetation
=================================

Testmania is a library that complements standard :py:mod:`unittest` module 
with few convenient assert functions. Such as for comparing deeply nested simple data
structures or xmls.

All assert methods are presented as global functions, not tied to the 
:py:class:`~unittest.TestCase` class. Also testmania exposes all built-in 
``TestCase.assert*`` methods as global 
functions in ``pep8_naming_fashion``. So that you haven't to use multiple
inheritance or mixins if you want to mix different asserts in your tests.

Testmania has no external dependencies except for 
`unittest2 <http://pypi.python.org/pypi/unittest2/>`_ if you're using
Python version lower than 2.7. However `nose <http://pypi.python.org/pypi/nose/>`_ 
is used to test testmania itself and it is not installed by default.

Installation is trivial::

    pip install testmania

Find the project on github: https://github.com/nailxx/testmania

Contents:

.. toctree::
   :maxdepth: 2

   pep8
   assertions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

