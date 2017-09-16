# -*- coding: utf-8 -*-
"""
Top profiles application file.

Usage:
    $ python -m lib.query.tweets.topProfiles [LIMIT]
"""
import sys

from lib import database as db


def printTopProfiles(limit=1):
    """
    Prints the most followed user or users in the Profile table.

    @param limit: Default 1. Upper bound for count of profiles to return,
        as an integer.
    """

    res = db.Profile.select().orderBy('followers_count DESC')

    if res.count():
        for prof in res[:limit]:
            prof.prettyPrint()
    else:
        print 'Zero profiles found in Profile table.'


def main(args):
    limit = int(args[0]) if args else 1
    printTopProfiles(limit)


if __name__ == '__main__':
    main(sys.argv[1:])