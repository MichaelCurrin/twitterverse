# -*- coding: utf-8 -*-
"""
Handle Twitter API rate limit error.

The newer version of tweepy accepts the following the api object.
- wait_on_rate_limit: Wait until next rate limit window is reached to continue
    making queries. Default is True, so errors are prevented when iterating
    over a cursor.
- wait_on_rate_limit_notify: When waiting instead of raising an error,
    show a warning message. See the tweepy binder.py script.
        log.warning("Rate limit reached. Sleeping for: %d" % sleep_time)

This rates script is an archive of code which was done based on tutorial in the
documentation, but is longer needed but could be needed for an
implementation to handle rate limiting in a different way if a hook is needed
e.g. to log the warning to a different location or do another action
instead of waiting. Using asyncio would be a good choice here.
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
    connection object is setup as `wait_on_rate_limit=False`,
    which was a flag added to a later version of tweepy.

    See tweepy docs and https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy

    TODO: Sleeping for 15 minutes is not efficient, as when you
    exceed the limit for the 15 minute window, you could be a few seconds
    from reaching the next window. Rather get the reset time and wait until
    current time is that. See tweepy's binder.py script which does this.

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
