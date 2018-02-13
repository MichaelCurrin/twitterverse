# -*- coding: utf-8 -*-
"""
Handle Twitter API rate limit error.

This is an archive of code which is no longer needed but could be needed
for an implementation to handle rate limiting in a different way.
"""
import time

import tweepy


def limitHandled(cursor):
    """
    Function to handle Twitter API rate limiting when cursoring through items
    (note that this does not work Streaming API.)

    Since cursors raise RateLimitErrors in their next() method, handling
    them can be done by wrapping the cursor in an iterator, such that
    an error is never raised outside the cursor.

    Therefore this limitHandled function is is ONLY needed if an API
    connection object is setup as `wait_on_rate_limit_notify=False`,
    which was a flag added to a later version of tweepy.

    See tweepy docs and https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy

    Note also that sleeping for 15 minutes is not efficient, as when you
    exceed the limit for the 15 minute window, you could be a few seconds
    from reaching the next window. It would be better to make a call
    to the endpoint which returns rate limit data, or to just the rate limit
    data returned on the main call (at least in the Twitter API and this
    needs to be checked if its available in tweepy). Then the timestamp
    of the when to wait until can be compared to current time and sleep until
    then.

    @param: cursor: tweepy Cursor items list.
        Example Usage:
        >>> for x in limitHandled(tweepy.Cursor(api.followers).items()):
        ...     print x

    @return: cursor.next() in a generator expression.
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as e:
            print u'Sleeping 15 min. {0}'.format(str(e))
            time.sleep(15 * 60)
