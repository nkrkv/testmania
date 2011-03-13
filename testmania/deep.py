# -*- coding: utf-8; -*-

import pprint

from UserDict import UserDict
from UserList import UserList


def assert_deep_equal(actual, expected, msg=None, ignore_extra_keys=False):
    """Test for equality two deeply nested data structures of simple 
    types like dicts or lists.

    Provides readable message if they don't match with path containing 
    found difference.

    .. testcode::

        from testmania import assert_deep_equal
        
        actual = {
           'foo': 1,
           'bar': [
                {'baz': 'qux'},
                {'bam': 'qix', 'tee': 'uup'},
           ],
           'wee': 3,
        }
        
        expected = {
           'foo': 1,
           'bar': [
                {'baz': 'qux'},
                {'bam': 'qix', 'tee': 'uop'},
           ],
           'wee': 3,
        }

        assert_deep_equal(actual, expected)

    raises

    .. testoutput::

        Traceback (most recent call last):
            ...
        AssertionError: 
        -------------------------------- Expected -----------------------------------
        {'bar': [{'baz': 'qux'}, {'bam': 'qix', 'tee': 'uop'}], 'foo': 1, 'wee': 3}
        --------------------------------- Actual ------------------------------------
        {'bar': [{'baz': 'qux'}, {'bam': 'qix', 'tee': 'uup'}], 'foo': 1, 'wee': 3}

        at /bar.1.tee, expected 'uop', got 'uup'

    Objects to compare may be arbitrary nested structures of lists, dicts,
    :py:class:`~UserDict.UserDict`, :py:class:`~UserList.UserList` or inherited
    of thereof such as :py:class:`~collections.defaultdict` or custom user data types.

    If `ignore_extra_keys=True`, dicts in `actual` are allowed to be a superset of
    corresponding dicts in `expected` at any level, e.g. to have extra keys. This is
    handy in cases when it is important to test whether at least necessary items
    are present in a data structure.
    """
    try:
        _assert_deep_equal(actual, expected, [], ignore_extra_keys=ignore_extra_keys)
    except AssertionError, e:
        if not msg:
            msg = "\n-------------------------------- Expected -----------------------------------\n"
            msg += _format(expected)
            msg += "\n--------------------------------- Actual ------------------------------------\n"
            msg += _format(actual)
            msg += "\n\n" + str(e)
        raise AssertionError(msg)


def _format(obj):
    # simplify to make sure it is pretty printed
    return pprint.pformat(_simplify(obj))


def _simplify(x):
    """Recursively replace inherited dicts/lists with simple dicts/lists"""
    if isinstance(x, (list, UserList)):
        result = [_simplify(i) for i in x]
    elif isinstance(x, tuple):
        result = tuple([_simplify(i) for i in x])
    elif isinstance(x, (dict, UserDict)):
        result = {}
        for key, value in x.iteritems():
            if isinstance(value, dict):
                result[key] = _simplify(value)
            else:
                result[key] = value
    else:
        result = x
    return result


def _assert_deep_equal(actual, expected, path, ignore_extra_keys):
    path_str = '/' + '.'.join(map(str, path))
    if isinstance(actual, (dict, UserDict)) and isinstance(expected, (dict, UserDict)):
        actual_keys = set(actual.keys())
        expected_keys = set(expected.keys())
        actual_key_extra = actual_keys - expected_keys
        if actual_key_extra and not ignore_extra_keys:
            msg = "at %s, actual got unexpected keys %s" % (path_str, list(actual_key_extra))
            raise AssertionError(msg)

        expected_key_extra = expected_keys - actual_keys
        if expected_key_extra:
            msg = "at %s, expected keys %s are absent in actual" % (path_str, list(expected_key_extra))
            raise AssertionError(msg)

        for key in expected_keys:
            _assert_deep_equal(actual[key], expected[key], path + [key], ignore_extra_keys)

    elif isinstance(actual, (list, UserList)) and isinstance(expected, (list, UserList)) or \
            isinstance(actual, tuple) and isinstance(expected, tuple):
        actual_len = len(actual)
        expected_len = len(expected)
        if actual_len != expected_len:
            raise AssertionError(
                "at % s, expected length is %s, actual length is %s" %
                (path_str, expected_len, actual_len))
        for i in xrange(actual_len):
            _assert_deep_equal(actual[i], expected[i], path + [i], ignore_extra_keys)
    else:
        if actual != expected:
            raise AssertionError(
                "at % s, expected %r, got %r" %
                (path_str, expected, actual))
