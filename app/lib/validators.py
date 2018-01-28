# -*- coding: utf-8 -*-
"""
Validators lib application file.
"""
from formencode.validators import UnicodeString


class TweetMessage(UnicodeString):
    """
    Twitter has changed the max at the end of 2017 from 140 to 280 characters
    and this is mirrored here such that an Invalid error is raised for
    exceeding the lengh. Note that Twitter applies the limit at creation
    time on the *truncated* form of a tweet i.e. replace full URLs with
    shortened 't.co' URLs, which only count as a small, fixed number of
    characters.

    A tweet's URLs are expanded by default in the browser. This can be
    recreated in the API using the 'extended' value for tweet_mode,
    however this should be avoided as this means the tweet length exceeds
    280 characters. Also the entire original URL is still not shown. If
    this is required, then the model should be modified to store a tweet's
    URL attribute.
    """

    max = 280

    def _validate_other(self, value, state):
        """
        Override the parent method so that validation is done on the unicode
        value. This overcomes a bug in SQLObject where the length of a
        string is incorrectly evaluated based on the str equivalent of a
        unicode string.

        @return: None
        """
        if type(value) == str:
            value = value.decode('utf-8')
        super(TweetMessage, self)._validate_other(value, state)
