# -*- coding: utf-8 -*-
"""
Top profiles application file.
"""
import sys

from lib import database as db


def printTopProfiles(limit=1):
    """
    Prints the most followed user or users in the Profile table.

    @param limit: Default 1. Upper bound for count of profiles to return,
        as an integer. Set as 0 to return all.
    """

    res = db.Profile.select().orderBy('followers_count DESC')

    if res.count():
        for prof in res[:limit]:
            prof.prettyPrint()
    else:
        print 'Zero profiles found in Profile table.'


def main(args):
    """
    Function for executing command-line arguments.
    """
    if not args or set(args) & set(('-h', '--help')):
        print """\
Print the top N profiles in the Profile table, ordered by most followed.

Usage:
$ python -m lib.query.tweets.topProfiles [LIMIT N] [-h|--help]

Options and arguments:
--help : Show this help message and exit.
LIMIT  : Count of profiles to get. Set as 0 to get all.
"""
    else:
        limit = int(args[0]) if args else 1
        printTopProfiles(limit)


if __name__ == '__main__':
    main(sys.argv[1:])
