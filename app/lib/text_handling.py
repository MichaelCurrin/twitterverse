# -*- coding: utf-8 -*-
"""
Common string handling functions.

Usage:
    $ python -m lib.text_handling
"""
import string


def flattenText(text, replacement=u" "):
    r"""
    Remove line breaks in a string.

    Flatten a string from multi-line to a single line, using a specified
    string to replace line breaks.

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


def stripSymbols(inputStr, keepHash=False, keepAt=False, keepWhiteSpace=False):
    """
    Remove symbols from a string, but optionally keep any which are specified.

    Accepts str and unicode input so this function has broader application,
    but rejects other data types. The output type is forced to match the
    type of the input. (Note: it appears that both types may contain a unicode
    character, but only an ASCII str can contain ASCII characters.)

    Removal of unicode characters:
        https://stackoverflow.com/questions/15321138/removing-unicode-u2026-like-characters-in-a-string-in-python2-7

    :param str inputStr: Word or sentence.
    :param keepHash: Set as True to keep the '#' symbol.
    :param keepAt: Set as True to keep the '@' symbol.
    :param keepWhiteSpace: Set at True to keep the whitespace characters.

    :return outputList: A list of cleaned strings without punctuation or
        special unicode characters. Keeps the characters indicated by arguments.
    """
    assert isinstance(inputStr, basestring), (
        'Expected input as unicode or ascii string, but got type `{0}`.'
        .format(type(inputStr).__name__)
    )

    # Force the input to be unicode.
    if type(inputStr) == unicode:
        outputStr = inputStr
    else:
        outputStr = inputStr.decode('unicode_escape')

    # Remove unicode symbols.
    outputStr = outputStr.encode('ascii', 'ignore')

    # Replace whitespace characters.
    if not keepWhiteSpace:
        for c in string.whitespace:
            if c in outputStr:
                outputStr = outputStr.replace(c, ' ')

    # Remove standard punctuation.
    charToRemove = string.punctuation
    if keepHash:
        charToRemove = charToRemove.replace('#', '')
    if keepAt:
        charToRemove = charToRemove.replace('@', '')
    for c in charToRemove:
        if c in outputStr:
            outputStr = outputStr.replace(c, '')

    if type(inputStr) == unicode:
        outputStr = outputStr.encode('utf-8')

    outputList = outputStr.split(' ')
    outputList = [s for s in outputList if s]

    return outputList


def main():
    """
    Function to manually verify functionality of the strip symbols logic.
    """
    tests = [
        "I am a #Tweet, but need cleaning! ^-^ Why don't you help me,"
        " my friend @jamie_123?",
        u"I’m a #unicode string with unicode symbol near the start!",
        "I’m an #ascii string, also with unicode symbol near the start!",
        u"Unicode symbol \u2026 (…) in unicode.",
        "Unicode symbol \u2026 (…) in ascii.",
        "I am some ****stars**** and I am some <<<arrows>>>.",
        "I have \t\ttabs.",
        "I am a \nline break.",
        string.punctuation,

        "Join me LIVE with @VP, @SecretaryPerry, @SecretaryZinke and"
        " @EPAScottPruitt. \n#UnleashingAmericanEnergy\nhttps://t.co/hlM7F2BQD9",

        "MAKE AMERICA SAFE AGAIN!\n\n#NoSanctuaryForCriminalsAct \n#KatesLaw"
        " #SaveAmericanLives \n\nhttps://t.co/jbN4hPjqjS",

        # Todo - handle URIs in sentence.
        "This is a link! http://IAmLink.com#yeah",
        u"https://IAmUnicodeLink.com/abc_def"
    ]
    for t in tests:
        print t
        if type(t) != str:
            t = t.encode('ascii', 'ignore')
        print stripSymbols(t, keepHash=True, keepAt=True)
        print '----'


if __name__ == '__main__':
    main()
