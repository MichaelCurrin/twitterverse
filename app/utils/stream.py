#!/usr/bin/env python
"""
Stream utility.

Test streaming API using command-line arguments list of input terms. Tweets
are printed but not stored.

See the docs directory for the AND / OR rules of stream searches.

Transform items split to work with tweepy. Spaces on either side
of commas are optional and have no effect.
e.g.
    $ python -m lib.twitter_api.streaming abc def,ABC DEF, xyz
    => ['abc def', 'MNO QRS', 'xyz']
    => which translates to
        match ('abc' and 'def' in one tweet in any order)
        or match ('MNO' and 'QRS' in one tweet in any order)
        or match ('xyz')
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)
))
from lib.twitter_api import streaming


def main(args):
    """
    Main command-line entrypoint.
    """
    if not args or set(args) & {'-h', '--help'}:
        print('Usage: python -m lib.twitter_api.streaming [WORD, WORD, ...]')
        print('e.g. abc def, MNO QRS,xyz')
        print('      --> track: ("abc" and "def") or ("MNO" and "QRS")'
              ' or "xyz"')
        print()
    else:
        argsStr = ' '.join(args)
        track = argsStr.split(',')
        track = [x.strip() for x in track]

        streaming.startStream(track)


if __name__ == '__main__':
    main(sys.argv[1:])
