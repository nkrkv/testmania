# -*- coding: utf-8; -*-

from testmania.pep8 import assert_equal, assert_raises, assert_raises_regexp
from testmania.deep import assert_deep_equal


class TestDeepAssert(object):
    def test_primitive(self):
        assert_deep_equal(123, 123)
        assert_deep_equal('foo', 'foo')

    def test_primitive_inequal(self):
        with assert_raises(AssertionError):
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

        with assert_raises_regexp(AssertionError, "at /foo, expected 'hello', got 'bar'"):
            assert_deep_equal(d1, d2)

    def test_dict_inequal_extra_keys(self):
        d1 = {
            'foo': 'bar',
            'baz': 'qux',
        }
        
        d2 = {
            'foo': 'bar',
        }

        with assert_raises_regexp(AssertionError, ur"at /, actual got unexpected keys \['baz'\]"):
            assert_deep_equal(d1, d2)

    def test_dict_inequal_lack_of_key(self):
        d1 = {
            'foo': 'bar',
        }
        
        d2 = {
            'foo': 'bar',
            'baz': 'qux',
        }

        with assert_raises_regexp(AssertionError, ur"at /, expected keys \['baz'\] are absent in actual"):
            assert_deep_equal(d1, d2)

    def test_partial_dict_match(self):
        d1 = {
            'foo': 'bar',
            'baz': 'qux',
        }
        
        d2 = {
            'foo': 'bar',
        }

        assert_deep_equal(d1, d2, ignore_extra_keys=True)

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

        with assert_raises_regexp(AssertionError, u"at /baz.2.aww, expected 'uwl', got 'owl'"):
            assert_deep_equal(d1, d2)
