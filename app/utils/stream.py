#!/usr/bin/env python
"""
Stream utility.

Test streaming API using command-line arguments list of input terms. Tweets
are printed but not stored.

See the docs directory for the AND / OR rules of stream searches.
"""
from __future__ import absolute_import
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
        print('Usage: {} [PHRASE, PHRASE, ...]'.format(__file__))
        print()
        print("Each phrase may have spaces and should be separated by")
        print(" commas. They will then be ANDed together.")
        print()
        print('For example, with these arguments:')
        print('    abc def, MNO QRS,xyz')
        print('Then a stream search will be done for:')
        print('   ("abc" and "def") or ("MNO" and "QRS") or "xyz"')
        print()
    else:
        argsStr = ' '.join(args)
        track = argsStr.split(',')
        track = [x.strip() for x in track]

        streaming.startStream(track)


if __name__ == '__main__':
    main(sys.argv[1:])
