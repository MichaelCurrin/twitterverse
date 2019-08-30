# -*- coding: utf-8 -*-
"""
Validators lib application file.

When using the to_python method on a validator or implementing a
validator on a SQLObject column, a formencode Invalid error can be raised
when necessary.

Note on tweet message validation:
    Twitter has changed the max at the end of 2017 from 140 to 280 characters
    When a retweeted tweet is expanded it can exceed the limit, therefore
    a validating on a max length does not work.
"""
from formencode.validators import UnicodeString


class UnicodeValidator(UnicodeString):
    """
    Base for unicode string validation, with added support for evaluating
    length correctly for special unicode characters, like accents and emjojis.

    Override `max` as an integer on the class or on an instance,
    to enforce a maximum character length.
    """
    def _validate_other(self, value, state):
        """
        Override the parent method so that validation is done on the unicode
        value. This overcomes a bug in SQLObject where the length of a
        string is incorrectly evaluated based on the str equivalent of a
        unicode string.

        :return: None
        """
        if type(value) == str:
            value = value.decode('utf-8')
        super(UnicodeValidator, self)._validate_other(value, state)
