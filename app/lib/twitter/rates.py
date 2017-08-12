# -*- coding: utf-8 -*-
"""
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
    them can be done by wrapping the cursor in an iterator.

    This is ONLY needed if api object is setup to keep default
    `wait_on_rate_limit_notify=False` which was a feature added to a later
    version of tweepy.

    See tweepy docs and https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy

    @param: cursor: tweepy Cursor items list.
        Usage:
            for x in limitHandled(tweepy.Cursor(api.followers).items()):
                print x

    @return: None
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as e:
            print u'Sleeping 15 min. {0}'.format(str(e))
            time.sleep(15 * 60)
