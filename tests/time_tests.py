# -*- coding: utf-8; -*-

import datetime

from testmania.pep8 import assert_raises
from testmania.time import assert_just_now


class TestTimeDeltas(object):
    def test_ok(self):
        assert_just_now(datetime.datetime.now())

    def test_future(self):
        with assert_raises(AssertionError):
            assert_just_now(datetime.datetime.now() + datetime.timedelta(hours=2))

    def test_past(self):
        with assert_raises(AssertionError):
            assert_just_now(datetime.datetime.now() - datetime.timedelta(hours=2))
