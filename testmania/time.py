# -*- coding: utf-8; -*-

import datetime


def assert_just_now(time_value, msg=None, tolerance=1):
    """
    Test whether `time_value` represents almost current moment.
    It's handy to test timestamp values like ``created_at`` or ``updated_at``.

    :param time_value: should be a :py:class:`~datetime.datetime` object.
    :param int|float tolerance: specifies acceptable deviation
        of `time_value` in seconds.
    """
    delta = datetime.datetime.now() - time_value
    if abs(delta) > datetime.timedelta(seconds=tolerance):
        msg = msg or "Expected now, got %s" % time_value
        raise AssertionError(msg)
