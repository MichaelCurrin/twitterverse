#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Tweets utility.

Get Tweet and Profile data from the Twitter API based on Categories filter.
"""
import argparse
import os
import sys

from sqlobject.sqlbuilder import IN, AND

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import database as db
from lib.tweets import insertOrUpdateTweetBatch
from lib.query.tweets.categories import printAvailableCategories


def main():
    """Command-line interface to fetch Tweet data."""
    parser = argparse.ArgumentParser(description="""Fetch Tweets utility.
                                     Filter existing Profile records by
                                     Categories, fetch a limited number of
                                     Tweets for each Profile then insert or
                                     update Tweet and Profile records.""")

    parser.add_argument('-c', '--categories',
                        nargs='+',
                        help="""List of one or more existing Categories
                             in the db. Filter Profiles to only these
                             Categories then fetch and store data.
                             If this is omitted, print available Category
                             names in the db with Profile counts, then
                             exit.""")

    tweetGroup = parser.add_argument_group('Tweets')
    tweetGroup.add_argument('-t', '--tweets-per-profile',
                            type=int,
                            metavar='N',
                            default=200,
                            help="""Default 200. Count of Tweets to get for
                                 each profile. Values greater than 200 require
                                 paging and increases the number of queries
                                 needed per Profile.""")
    tweetGroup.add_argument('-v', '--verbose',
                        action='store_true',
                        help="""If supplied, pretty print Tweet data fetched
                             from the Twitter API.""")
    tweetGroup.add_argument('-n', '--no-write',
                            action='store_true',
                            help="If supplied, do not write data to the db.")

    args = parser.parse_args()

    if args.categories:
        inputCategories = [unicode(name) for name in args.categories]

        categoryResult = db.Category.select(
            IN(db.Category.q.name,
               args.categories)
        )
        dbCategoryNames = [c.name for c in list(categoryResult)]

        missing = set(inputCategories) - set(dbCategoryNames)
        assert not missing, u"Input categories not found in db: \n- {0}"\
                            .format('\n- '.join(missing))

        profResults = db.Profile.select(
            AND(db.Profile.j.categories,
                IN(db.Category.q.name,
                   args.categories))
        )
        profCount = profResults.count()
        print "Profiles to fetch Tweets for: {0:,d}".format(profCount)

        if profCount:
            insertOrUpdateTweetBatch(
                profResults,
                args.tweets_per_profile,
                verbose=args.verbose,
                writeToDB=not(args.no_write)
            )
    else:
        printAvailableCategories()


if __name__ == '__main__':
    main()
