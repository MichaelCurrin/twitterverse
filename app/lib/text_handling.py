# -*- coding: utf-8 -*-
"""
Common string handling functions.

Usage:
    $ python -m lib.textHandling
"""
from string import punctuation, whitespace


def stripSymbols(inputStr, keepHash=False, keepAt=False, keepWhiteSpace=False):
    """
    Remove symbols from a string but optionally keep some characters.

    Accepts str and unicode input so this function has broader application,
    but rejects other data types. The output type is forced to match the
    type of the input. (Note: it appears that both types may contain a unicode
    character, but only an ASCII str can contain ASCII characters.)

    Removal of unicode characters:
        https://stackoverflow.com/questions/15321138/removing-unicode-u2026-like-characters-in-a-string-in-python2-7

    :param str inputStr: Word or sentence.
    :param keepHash: default False. Set as True to keep the '#' symbol.
    :param keepAt: default False. Set as True to keep the '@' symbol.
    :param keepWhiteSpace: default False. Set at True to keep the whitespace
        characters.

    :return outputList: A list of cleaned strings without punctuation or
        special unicode characters. Keep the characters indicated by arguments.
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
    wsToRemove = whitespace
    if not keepWhiteSpace:
        for ws in wsToRemove:
            if ws in outputStr:
                outputStr = outputStr.replace(ws, ' ')

    # Remove standard punctuation.
    charToRemove = punctuation
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

    return outputList


def main():
    """
    Function to test functionality of the file.
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
        punctuation,
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
