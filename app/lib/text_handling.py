# -*- coding: utf-8 -*-
"""
Common string handling functions.

Usage:
    $ python -m lib.text_handling
"""
from __future__ import absolute_import
from __future__ import print_function
import string


def standardize_breaks(text):
    """
    Converting line endings to the Unix style.

    The Windows and the old Mac line breaks have been observed in Twitter
    profiles. These are best replaced with the standard form to make printing
    and text file handling easier. Especially since "\r" in an unquoted field
    causes CSV read errors.
    """
    return text.replace(u"\r\n", u"\n").replace(u"\r", "\n")


def flattenText(text, replacement=u" "):
    r"""
    Remove line endings in a string and replace with target character.

    This handles line endings of Unix, Mac and Windows style.

    :param text: Single unicode string, which could have line endings in
        any format.
    :param replacement: Unicode string to use in place of the line
        breaks. Defaults to a single space. Other recommended values are:
            - u"\t"
            - u"    "
            - u" ; "
            - u"\n"

    :return: the input text with newline characters replaced with the
        replacement string.
    """
    textList = standardize_breaks(text).split("\n")

    return replacement.join(textList)


def stripSymbols(inputStr, keepHash=False, keepAt=False, keepWhiteSpace=False):
    """
    Remove symbols from a string, but optionally keep any which are specified.

    TODO: Don't remove apostrophe in a word but on the outside only as quotes.
    Also handle unicode ’ as single quote.
    TODO: Replace with regex for the characters we do want, instead of having
    to explicitly replace things like punctutation and unicode.

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
        special unicode characters. Keeps the characters indicated by
        arguments.
    """
    assert isinstance(inputStr, str), (
        'Expected input to be string-like, but got type `{0}`.'
        .format(type(inputStr).__name__)
    )

    # Remove unicode symbols.
    # TODO Redo this in PY3 as this might no longer work.
    # outputStr = inputStr.encode('ascii', 'ignore')
    outputStr = inputStr

    # Replace whitespace characters.
    if not keepWhiteSpace:
        for c in string.whitespace:
            if c in outputStr:
                outputStr = outputStr.replace(c, ' ')

    # Remove standard punctuation.
    charToRemove = string.punctuation
    keepsChars = []
    if keepHash:
        keepsChars.append('#')
    if keepAt:
        keepsChars.append('@')
    for keep in keepsChars:
        charToRemove = charToRemove.replace(keep, '')

    for c in charToRemove:
        if c in outputStr:
            outputStr = outputStr.replace(c, '')

    outputList = outputStr.split(' ')
    outputList = [s for s in outputList if s]

    return outputList


def main():
    """
    Function to manually verify functionality of the strip symbols logic.

    TODO: Move all of these to test_text_handling.py though that is low
    priority while this is only used process_tweets.py
    The function can eventually be used in DB reporting on tweet messages.
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
        " @EPAScottPruitt. "
        "\n#UnleashingAmericanEnergy\nhttps://t.co/hlM7F2BQD9",

        "MAKE AMERICA SAFE AGAIN!\n\n#NoSanctuaryForCriminalsAct \n#KatesLaw"
        " #SaveAmericanLives \n\nhttps://t.co/jbN4hPjqjS",

        # Todo - handle URIs in sentence.
        "This is a link! http://IAmLink.com#yeah",
        u"https://IAmUnicodeLink.com/abc_def"
    ]
    for t in tests:
        print(t)
        if type(t) != str:
            t = t.encode('ascii', 'ignore')
        print(stripSymbols(t, keepHash=True, keepAt=True))
        print('----')


if __name__ == '__main__':
    main()
