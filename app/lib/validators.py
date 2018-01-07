# -*- coding: utf-8 -*-
"""
Validators lib application file.
"""
from formencode.validators import UnicodeString


class TweetMessage(UnicodeString):
    """
    Validate Tweet message.

    Twitter has changed the max at the end of 2017 from 140 to 280 characters.
    """

    max = 280

    def _validate_other(self, value, state):
        """
        Override the parent method so that validation is done on the unicode
        value, since the str value would be longer for unicode characters.

        @return: None
        """
        if type(value) == str:
            value = value.decode('utf-8')
        super(TweetMessage, self)._validate_other(value, state)
