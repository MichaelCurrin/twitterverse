# -*- coding: utf-8 -*-
"""
Initialisation file for twitter directory.
"""
import datetime
from email.utils import mktime_tz, parsedate_tz


def convertTwitterTime(datetimeStr):
    """
    Convert a datetime as string from Twitter API to datetime object.

    @param datetimeStr: datetime as a string from the Twitter API.
        e.g. 'Thu Mar 19 12:37:15 +0000 2015'

    @return: datetime object in UTC time. Printing this out will reflect
        in the sytem's timezone.
        e.g. entering 12:00 for +0000 will show as 14:00 if printing in a
        system set to +0200 timezone. Whether doing str(obj) or str(obj.hour).
    """
    timeTuple = parsedate_tz(datetimeStr)
    timestamp = mktime_tz(timeTuple)

    return datetime.datetime.fromtimestamp(timestamp)
