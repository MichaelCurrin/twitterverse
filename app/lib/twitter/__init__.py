# -*- coding: utf-8 -*-
"""
Initialisation file for twitter library module.

The components of this module relate directly to the Twitter API and not
to the local database.

See also:
    https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
"""
import datetime
from email.utils import mktime_tz, parsedate_tz


def convertTwitterTime(datetimeStr):
    """
    Convert a datetime as string from Twitter API to a datetime object.

    @param datetimeStr: datetime value as a string from the Twitter API.
        e.g. 'Thu Mar 19 12:37:15 +0000 2015'

    @return: datetime object in UTC time. Printing this out will reflect
        in the system's timezone.
        e.g. entering time 12:00 for +0000 timezone will show as 14:00 if
        printing in a system set to +0200 timezone, whether doing str(obj) or
        str(obj.hour).
    """
    timeTuple = parsedate_tz(datetimeStr)
    timestamp = mktime_tz(timeTuple)

    return datetime.datetime.fromtimestamp(timestamp)
