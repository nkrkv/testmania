# -*- coding: utf-8; -*-

import pprint

from UserDict import UserDict
from UserList import UserList


def assert_deep_equal(obj1, obj2, message=None, partial_dict_match=False):
    """Test for equality two deeply nested data structures of simple 
    types like dicts or lists.

    Provides readable message if they don't match with path containing 
    found difference.

    .. testsetup:: *
    
        from testmania.deep import assert_deep_equal

    .. doctest::

        >>> obj1 = {
        ...    'foo': 1,
        ...    'bar': [
        ...         {'baz': 'qux'},
        ...         {'bam': 'qix', 'tee': 'uup'},
        ...    ],
        ...    'wee': 3,
        ... }

        >>> obj2 = {
        ...    'foo': 1,
        ...    'bar': [
        ...         {'baz': 'qux'},
        ...         {'bam': 'qix', 'tee': 'uop'},
        ...    ],
        ...    'wee': 3,
        ... }

        >>> assert_deep_equal(obj1, obj2)
        Traceback (most recent call last):
            ...
        AssertionError: 
        ---------- Left ----------
        {'bar': [{'baz': 'qux'}, {'bam': 'qix', 'tee': 'uup'}], 'foo': 1, 'wee': 3}
        ---------- Right ---------
        {'bar': [{'baz': 'qux'}, {'bam': 'qix', 'tee': 'uop'}], 'foo': 1, 'wee': 3}
        <BLANKLINE>
        at /bar.1.tee, left has value 'uup', right has value 'uop'

    Objects to compare may be arbitrary nested structures of lists, dicts,
    :py:class:`~UserDict.UserDict`, :py:class:`~UserList.UserList` or inherited
    of thereof such as :py:class:`~collections.defaultdict` or custom user data types.

    If `partial_dict_match=True`, dicts in `obj1` are allowed to be a superset of
    corresponding dicts in `obj2` at any level, e.g. to have extra keys. This is
    handy in cases when it is important to test whether at least necessary items
    are present in a data structure.
    """
    try:
        _assert_deep_equal(obj1, obj2, [], partial_dict_match=partial_dict_match)
    except AssertionError, e:
        if not message:
            message = "\n---------- Left ----------\n"
            message += _format(obj1)
            message += "\n---------- Right ---------\n"
            message += _format(obj2)
            message += "\n\n" + str(e)
        raise AssertionError(message)


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


def _assert_deep_equal(obj1, obj2, path, partial_dict_match):
    path_str = '/' + '.'.join(map(str, path))
    if isinstance(obj1, (dict, UserDict)) and isinstance(obj2, (dict, UserDict)):
        obj1_keys = set(obj1.keys())
        obj2_keys = set(obj2.keys())
        obj1_key_extra = obj1_keys - obj2_keys
        if obj1_key_extra and not partial_dict_match:
            msg = "at %s, left has extra keys %s" % (path_str, list(obj1_key_extra))
            raise AssertionError(msg)

        obj2_key_extra = obj2_keys - obj1_keys
        if obj2_key_extra:
            msg = "at %s, right has extra keys %s" % (path_str, list(obj2_key_extra))
            raise AssertionError(msg)

        for key in obj2_keys:
            _assert_deep_equal(obj1[key], obj2[key], path + [key], partial_dict_match)

    elif isinstance(obj1, (list, UserList)) and isinstance(obj2, (list, UserList)) or \
            isinstance(obj1, tuple) and isinstance(obj2, tuple):
        obj1_len = len(obj1)
        obj2_len = len(obj2)
        if obj1_len != obj2_len:
            raise AssertionError(
                "at % s, left has length %s, right has length %s" %
                (path_str, obj1_len, obj2_len))
        for i in xrange(obj1_len):
            _assert_deep_equal(obj1[i], obj2[i], path + [i], partial_dict_match)
    else:
        if obj1 != obj2:
            raise AssertionError(
                "at % s, left has value %r, right has value %r" %
                (path_str, obj1, obj2))
