# -*- coding: utf-8 -*-
"""
Initialisation file for lib directory.

Logging approach is based on this tutorial:
    https://docs.python.org/2/howto/logging-cookbook.html
"""
import pytz
import logging

from .config import AppConf


conf = AppConf()
logPath = conf.get('Logging', 'path')
debug = conf.getboolean('Logging', 'debug')

logger = logging.getLogger("lib")


# TODO: Move to text_handling.py, update references and retest.
def flattenText(text, replacement=u" "):
    r"""
    Flatten a string from multi-line to a single line, using a specified
    string in place of line breaks.

    Rather than just replacing '\n', we also consider the '\r\n' Windows line
    ending, as this has been observed in Twitter profile descriptions even when
    testing on a Linux machine.

    It is not practical to use .split and .join here. Since splitting on
    one kind of characters produces a list, which then has to have its
    elements split on the other kind of character, then the nested list
    would to be made into a flat list and then joined as a single string.

    :param text: Single unicode string, which could have line breaks
        in the '\n' or '\r\n' format.
    :param replacement: Unicode string to use in place of the line
        breaks. Defaults to a single space. Other recommended values are:
            - u"\t"
            - u"    "
            - u" ; "
            - u"\n"

    :return: the input text with newline characters replaced with the
        replacement string.
    """
    text = text.replace(u"\r\n", replacement)

    if replacement != "\n":
        text = text.replace(u"\n", replacement)

    return text


def set_tz(dt):
    """
    Ensure a datetime object has a timezone set.

    Either set timezone of naive datetime object to UTC/GMT time or leave the
    object as is.

    This can be applied to created or updated times for tweet or profile objects
    returned from the Twitter API. When inspecting times from the Twitter API
    directly, they come as UTC+0000 regardless of where the tweet was made or
    what Twitter settings are. Therefore it is safe to assume this is the
    correct timezone to add for a Twitter datetime which is naive.

    :param datetime.datetime dt: datetime object.

    :return: Timezone-aware datetime object.
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
