# -*- coding: utf-8; -*-

"""
`Expectation` is a special object that could be used to simplify
testing of composite values. It resepresents not concrete value,
but an expectation expressed in terms of assertion functions.

It is better to illustrate it with an example. Consider you have
a function that returns set of blog post comments and your test
looks like::

    def test_fetch_comments(self):
        self.comments.post('John', "Oh, that's great")
        comments = self.comments.fetch()
        assert_equal(comments, [{
            'author': 'John',
            'text': "Oh, that's great",
            'visibility': 'public',
        }])

Now you decide to add ``created_at`` field to the comment structure::

    def test_fetch_comments(self):
        self.comments.post('John', "Oh, that's great")
        comments = self.comments.fetch()
        assert_equal(comments, [{
            'author': 'John',
            'text': "Oh, that's great",
            'visibility': 'public',
            'created_at': datetime.datetime.now(),
        }])

But this will fail from time to time since `now` when a comment is posted
and `now` when the comment is tested could differ a bit. It will be nice
to use :meth:`~testmania.time.assert_just_now` to test timestamp but to
leave test structure intact. Here `Expectation` object comes into play:: 

    from testmania import assert_just_now, Expectation as e

    def test_fetch_comments(self):
        self.comments.post('John', "Oh, that's great")
        comments = self.comments.fetch()
        assert_equal(comments, [{
            'author': 'John',
            'text': "Oh, that's great",
            'visibility': 'public',
            'created_at': e(assert_just_now),
        }])

Expectation tests value using an assertion function provided. It passes
if assertion is ok and fails with meaningful message that includes assertion
failure text.
"""

class Expectation(object):
    """
    Defines an object that holds an expectation about a value of the object
    that will be compared to it.

    .. note::

        Due to Python operator precedence rules, `Expectation` could be used only
        to test against types that don't define their own ``__eq__``. As a special
        case testing against :py:class:`~datetime.datetime` is allowed.
    """

    # make datetime-compatible
    timetuple = None

    def __init__(self, assertion, *args, **kwargs):
        """
        :param assertion: assertion function or bound method to use to test expectation;
            choice is not limited to assertions from `testmania` package, it could be any
            function that takes tested value as first positional argument and raises
            ``AssertionError`` on test failure.
        :param args: passed to `assertion` as-is after tested value argument.
        :param kwargs: passed to `assertion` as-is.
        """
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

    def __ne__(self, other):
        return not (self == other)
