# -*- coding: utf-8; -*-

from testmania.pep8 import assert_in, assert_equal, assert_raises
from testmania.expect import Expectation


class TestExpectation(object):
    def test_ok(self):
        actual = {
            'foo': 'bar',
            'baz': 'qux',
        }

        expected = {
            'foo': 'bar',
            'baz': Expectation(assert_in, ['qux', 'mew', 'pur'])
        }

        assert_equal(actual, expected)

    def test_fail(self):
        actual = {
            'foo': 'bar',
            'baz': 'bee',
        }

        expected = {
            'foo': 'bar',
            'baz': Expectation(assert_in, ['qux', 'mew', 'pur'])
        }

        with assert_raises(AssertionError) as e:
            assert_equal(actual, expected)

        assert_in("<Failed expectation: 'bee' not found in ['qux', 'mew', 'pur']>", str(e.exception))
