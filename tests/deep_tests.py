# -*- coding: utf-8; -*-

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from nose.tools import assert_equal
from testmania.deepassert import assert_deep_equal


class TestDeepAssert(TestCase):
    def test_primitive(self):
        assert_deep_equal(123, 123)
        assert_deep_equal('foo', 'foo')

    def test_primitive_inequal(self):
        with self.assertRaises(AssertionError):
            assert_deep_equal(123, 0)

    def test_dict(self):
        d = {
            'foo': 'bar',
            'baz': 'qux',
        }
        assert_deep_equal(d, d)

    def test_dict_inequal_different_values(self):
        d1 = {
            'foo': 'bar',
            'baz': 'qux',
        }
        
        d2 = {
            'foo': 'hello',
            'baz': 'qux',
        }

        with self.assertRaisesRegexp(AssertionError, "at /foo, left has value 'bar', right has value 'hello'"):
            assert_deep_equal(d1, d2)

    def test_dict_inequal_extra_keys(self):
        d1 = {
            'foo': 'bar',
            'baz': 'qux',
        }
        
        d2 = {
            'foo': 'bar',
        }

        with self.assertRaisesRegexp(AssertionError, u"at /, left has extra keys \['baz'\]"):
            assert_deep_equal(d1, d2)

    def test_dict_inequal_lack_of_key(self):
        d1 = {
            'foo': 'bar',
        }
        
        d2 = {
            'foo': 'bar',
            'baz': 'qux',
        }

        with self.assertRaisesRegexp(AssertionError, u"at /, right has extra keys \['baz'\]"):
            assert_deep_equal(d1, d2)

    def test_partial_dict_match(self):
        d1 = {
            'foo': 'bar',
            'baz': 'qux',
        }
        
        d2 = {
            'foo': 'bar',
        }

        assert_deep_equal(d1, d2, partial_dict_match=True)

    def test_nested(self):
        d = {
            'foo': {
                'bar': 'qux',
                'yup': 'moo'
            },
            'baz': [0, 1, {'aww': 'owl'}, 2],
        }

        assert_deep_equal(d, d)

    def test_nested_inequal(self):
        d1 = {
            'foo': {
                'bar': 'qux',
                'yup': 'moo'
            },
            'baz': [0, 1, {'aww': 'owl'}, 2],
        }

        d2 = {
            'foo': {
                'bar': 'qux',
                'yup': 'moo'
            },
            'baz': [0, 1, {'aww': 'uwl'}, 2],
        }

        with self.assertRaisesRegexp(AssertionError, u"at /baz.2.aww, left has value 'owl', right has value 'uwl'"):
            assert_deep_equal(d1, d2)
