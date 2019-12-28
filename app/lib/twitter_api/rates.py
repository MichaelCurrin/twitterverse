"""
Handle Twitter API rate limit error.

The newer version of tweepy accepts the following in tweepy.API object.
- wait_on_rate_limit: If the api until next rate limit window is reached
    to continue. Default is False.
- wait_on_rate_limit_notify: Default is False. If the api prints a notification
     when the rate limit is hit. See the tweepy binder.py script.

See authentication.py for setting those on the tweepy.API object, so that the
catching of errors with limitHandled below is not needed.

This script is based on tutorial in the documentation. It needs
to be improved but shows where a hook could be used instead of the standard
waiting. e.g. to log the warning to a different location, or process
data. See asyncio library's sleep and return of control, as alternative to
time.sleep.
"""
from __future__ import absolute_import
from __future__ import print_function
import time

import tweepy


def limitHandled(cursor):
    """
    Function to handle Twitter API rate limiting when cursoring through items
    (note that this does not work with Streaming API.)

    Since cursors raise RateLimitErrors in their next() method, handling
    them can be done by wrapping the cursor in an iterator, such that
    an error is never raised outside the cursor. Alternatively, if not
    using a cursor, set wait_on_rate_limit to True on the tweepy.API object.

    See tweepy docs and https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy

    TODO: Sleeping for 15 minutes is not efficient, as when you
    exceed the limit for the 15 minute window, you could be a few seconds
    from reaching the next window. Rather get the reset time and wait until
    current time is that. See tweepy's binder.py script which does this.

    :param: cursor: tweepy Cursor items list.
        Example Usage:
        >>> for x in limitHandled(tweepy.Cursor(api.followers).items()):
        ...     print(x)

    :return: cursor.next() in a generator expression.
    """
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError as e:
            print(u'Sleeping 15 min. {0}'.format(str(e)))
            time.sleep(15 * 60)
