# -*- coding: utf-8; -*-

class Expectation(object):
    def __init__(self, assertion, *args, **kwargs):
        self.assertion = assertion
        self.args = args
        self.kwargs = kwargs
        self._fail_msg = None

    def __repr__(self):
        if self._fail_msg:
            return '<Failed expectation: %s>' % self._fail_msg
        return '<Expectation %s %s %s>' % (
            self.assertion.__name__, 
            ' '.join(map(repr, self.args)),
            ' '.join('%s=%r' % item for item in self.kwargs.iteritems())
        )

    def __eq__(self, other):
        try:
            self.assertion(other, *self.args, **self.kwargs)
        except AssertionError, e:
            self._fail_msg = str(e)
            return False
        else:
            return True
