# -*- coding: utf-8 -*-
"""
http://docs.tweepy.org/en/v3.5.0/code_snippet.html
"""
import time

import tweepy

from lib.twitterAuth import api


def limitHandled(cursor):
    """
    Since cursors raise RateLimitErrors in their next() method, handling 
    them can be done by wrapping the cursor in an iterator.
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as e:
            print 'Sleeping 15 min. {0}'.format(str(e))
            time.sleep(15 * 60)

sn = 'realDonalTrump'
#api.user_timeline(screen_name=sn)

# use ipython to explore actions on this.
