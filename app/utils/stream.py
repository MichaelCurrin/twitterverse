#!/usr/bin/env python
"""
Stream utility.

Test streaming API using command-line arguments list of input terms.
Such as words, phrases, hashtags or handles. Tweets are streamed live
and printed but not stored.

See this project's docs for the AND / OR rules of stream searches.
"""
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from lib.twitter_api import streaming


def main(args):
    """
    Main command-line entrypoint.
    """
    if not args or set(args) & {"-h", "--help"}:
        print("Usage: ./stream.py [PHRASE, PHRASE, ...]")
        print()
        print("Each phrase may have spaces and should be separated by")
        print(
            " a comma. They will then be ANDed together to match Twitter's API syntax."
        )
        print()
        print("For example, with these arguments:")
        print("    abc def, MNO QRS,xyz")
        print(
            "The search will print as ['abc def', 'MNO QRS', 'xyz'] which gets passed to a tweepy method."
        )
        print("Then a stream search will effectively be done for:")
        print('   ("abc" and "def") or ("MNO" and "QRS") or "xyz"')
        print()
        print(
            "Make sure to quote hashtags and quoted phrases, either with quotes on each section or the entire input."
        )
        print("""    '#abc , "foo bar", baz'""")
        print("Or like this")
        print("""    '#abc', '"foo bar"', 'baz'""")
    else:
        argsStr = " ".join(args)
        track = argsStr.split(",")
        track = [x.strip() for x in track]

        streaming.startStream(track)


if __name__ == "__main__":
    main(sys.argv[1:])
