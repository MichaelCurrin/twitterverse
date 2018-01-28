# -*- coding: utf-8 -*-
"""
Initialisation file for lib directory.
"""


def flattenText(text, replacement=u" "):
    r"""
    Flatten a string from multi-line to a single line, using a specified
    string in place of line breaks.

    Rather than just replacing '\n', also consider the '\r\n' Windows line
    ending, as this has been observed in Twitter profile descriptions even when
    testing on a Linux machine.

    It is not practical to use .split and .join here. Since splitting on
    one kind of characters produces a list, which then has to have its
    elements split on the other kind of character, then the nested list
    would to be made into a flat list and then joined as a single string.

    @param text: Single unicode string, which could have line breaks
        in the '\n' or '\r\n' format.
    @param replacement: Unicode string to use in place of the line
        breaks. Defaults to a single space. Other recommended values are:
            - u"\t"
            - u"    "
            - " ;"
            - "\n"

    @return: the input text with newline characters replaced with the
        replacement string.
    """
    return text.replace(u"\r\n", replacement).replace(u"\n", replacement)
