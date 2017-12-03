#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Tweets utility.

Get Tweet and Profile data from the Twitter API, after filtering Profiles
by Category. The Category could be an industry name, or it could be a
compiled favourites list of Profiles which the application user wants to
routinely fetch Tweets for.

A configured campaign name is allocated to Tweets, in addition to any possible
existing campaign names on Tweets which are updated. No custom campaign
is necessary as there is no search related campaign. If a Category
was used to store up a Profile's tweets, the Tweets can always be selected
from the db later by filtering on Tweets of Profiles in a given Category.
"""
import argparse
import os
import sys

from sqlobject import SQLObjectNotFound
from sqlobject.sqlbuilder import IN, AND

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import database as db
from lib.tweets import insertOrUpdateTweetBatch
from lib.query.tweets.categories import printAvailableCategories

# We fetch Tweets in this script by getting recent activity of Profiles,
# rather than through a search or fetching by Tweet GUID. Therefore assign
# this Campaign name to Tweets.
CAMPAIGN_NAME = u"_PROFILE_TIMELINE"


def main():
    """
    Command-line interface to fetch Tweet data for Profile Categories.
    """
    parser = argparse.ArgumentParser(
        description="""Fetch Tweets utility. Filter Profiles in the db using
            a Category input, update them with new data and insert or update
            the most recent Tweets for each. Tweets are assigned to the
            '{0}' Campaign.""".format(CAMPAIGN_NAME))

    view = parser.add_argument_group("View", "Print data to stdout")
    view.add_argument(
        '-a', '--available',
        action='store_true',
        help="Output available Categories in db, with Profile counts for each."
    )

    update = parser.add_argument_group("Update", "Create or update Tweet"
                                                 " records.")
    update.add_argument(
        '-c', '--categories',
        metavar='CATEGORY',
        nargs='+',
        help="""List of one or more existing Categories in the db. Filter
            Profiles to only these Categories then fetch and store data."""
    )
    update.add_argument(
        '-t', '--tweets-per-profile',
        type=int,
        metavar='N',
        default=200,
        help="""Default 200. Count of Tweets to fetch and store for each
            profile. A value up to 200 takes a fixed time to query one
            page of Tweets for a Profile, while higher values require
            querying more pages and therefore will take longer per
            Profile and lead to a higher chance of hitting rate limits.
            A higher value also requires additional time to create or update
            records."""
    )
    update.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="""If supplied, pretty print Tweet data fetched from the
            Twitter API. Otherwise only a count of Tweets is printed
            upon completion.""")
    update.add_argument(
        '-n', '--no-write',
        action='store_true',
        help="If supplied, do not write data to the db."
    )

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

        try:
            campaignRec = db.Campaign.byName(CAMPAIGN_NAME)
        except SQLObjectNotFound:
            campaignRec = db.Campaign(name=CAMPAIGN_NAME, searchQuery=None)

        if profCount:
            insertOrUpdateTweetBatch(
                profResults,
                args.tweets_per_profile,
                verbose=args.verbose,
                writeToDB=not(args.no_write),
                campaignRec=campaignRec
            )
    else:
        printAvailableCategories()


if __name__ == '__main__':
    main()
