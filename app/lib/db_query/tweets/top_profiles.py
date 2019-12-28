"""
Top profiles application file.

Functions are made available for imports but this script can also be run
directly.

Usage:
    $ python -m lib.query.tweets.top_profiles --help
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse

from lib import database as db


def printTopProfiles(limit=1):
    """
    Prints the most followed user or users in the Profile table.

    :param limit: Default 1. Upper bound for count of profiles to return,
        as an integer. Set as 0 to return all.

    :return: None
    """
    res = db.Profile.select().orderBy('followers_count DESC')

    if res.count():
        for prof in res[:limit]:
            prof.prettyPrint()
    else:
        print('Zero profiles found in Profile table.')


def main():
    """
    Function for executing command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Pretty print the top Profile"
                                     " records, ordered by most followed.")
    parser.add_argument(
        'limit',
        type=int,
        help="Max count of profiles to select. Set as 0 to get all."
    )

    args = parser.parse_args()

    printTopProfiles(args.limit)


if __name__ == '__main__':
    main()
