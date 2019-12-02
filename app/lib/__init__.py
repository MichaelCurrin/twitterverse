# -*- coding: utf-8 -*-
"""
Initialisation file for lib directory.

Logging approach is based on this tutorial:
    https://docs.python.org/2/howto/logging-cookbook.html
"""
from __future__ import absolute_import
from __future__ import print_function
import logging
import pytz
import datetime

from .config import AppConf


conf = AppConf()
logPath = conf.get('Logging', 'path')
debug = conf.getboolean('Logging', 'debug')

logger = logging.getLogger("lib")


def timeit(func):
    """
    Decorator to time a function duration, printing its start and end.

    You can use `time.time()` and the difference can be multiplied by 1000
    to give delta in milliseconds. But that only looks neat for small values.
    The datetime object provides output as '0:00:00.000' which is more widely
    usable and comparable.

    This can make the print output messy - use times or durations in the log
    file if that would be better.

    From:
        https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
    """
    def timed(*args, **kw):
        print('[START] {} '.format(func.__name__))

        ts = datetime.datetime.now()
        result = func(*args, **kw)
        te = datetime.datetime.now()
        print('[END] {} (took {})'.format(func.__name__, te - ts))

        return result

    return timed


def set_tz(dt):
    """
    Ensure a datetime object has a timezone set.

    Either set timezone of naive datetime object to UTC/GMT time or leave the
    object as is.

    This can be applied to created or updated times for tweet or profile
    objects returned from the Twitter API. When inspecting times from the
    Twitter API directly, they come as UTC+0000 regardless of where the tweet
    was made or what Twitter settings are. Therefore it is safe to assume this
    is the correct timezone to add for a Twitter datetime which is naive.

    :param datetime.datetime dt: datetime object.

    :return: A new datetime object which is timezone aware.
    """
    if not dt.tzinfo:
        return dt.replace(tzinfo=pytz.UTC)

    return dt


def setupLogger():
    """
    Setup the logger object with level, output location and formatting.

    Only updates the logger if there are no handlers already, in order to
    prevent modules each adding the same handler, which results in
    duplicate log output.
    See Guillaume Cisco's answer here:
        https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module

    :return None.
    """
    global logger

    if not logger.handlers:
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s"
                                      " - %(message)s")

        # Create handler for configured log file location.
        fileHandler = logging.FileHandler(logPath)
        fileHandler.setFormatter(formatter)

        # Create handler to print out higher level event in addition to sending
        # to the log file with the file handler.
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.CRITICAL)
        consoleHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)


setupLogger()
