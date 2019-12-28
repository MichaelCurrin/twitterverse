#!/usr/bin/env python
"""
Fetch Tweets utility.

Get Tweet and Profile data from the Twitter API, after filtering Profiles
by a given Category list.

The Category could be an industry name, or it could be a
compiled favourites list of Profiles which the application user wants to
routinely fetch Tweets for. Note that this utility cannot be used to lookup
a specific screen name, but rather Categories containing Profile records.

A configured campaign name is allocated to fetched Tweets, in addition to
any possible existing campaign names on Tweets which are updated. No custom
campaign is necessary to allow to the Tweets, since the fetch is done based on
screen names rather than a Twitter API search query. If a Category
was used to store up a Profile's tweets, the Tweets can always be selected
from the db later by filtering on Tweets of Profiles in a given Category.
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import os
import sys

from sqlobject import SQLObjectNotFound
from sqlobject.sqlbuilder import IN, AND

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db
from lib.config import AppConf
from lib.tweets import insertOrUpdateTweetBatch
from lib.db_query.tweets.categories import printAvailableCategories


conf = AppConf()
UTILITY_CAMPAIGN = conf.get('Labels', 'fetchTweets')


def main():
    """
    Command-line interface to fetch Tweet data for Profile Categories.
    """
    parser = argparse.ArgumentParser(
        description="""Fetch Tweets utility. Filter Profiles in the db using
            a Category input, update them with new data and insert or update
            the most recent Tweets for each. Tweets are assigned to the
            '{0}' Campaign.""".format(UTILITY_CAMPAIGN))

    viewGrp = parser.add_argument_group("View", "Print data to stdout")
    viewGrp.add_argument(
        '-a', '--available',
        action='store_true',
        help="Output available Categories in db, with Profile counts for each."
    )

    updateGrp = parser.add_argument_group("Update", "Create or update Tweet"
                                                    " records.")
    updateGrp.add_argument(
        '-c', '--categories',
        metavar='CATEGORY',
        nargs='+',
        help="""List of one or more existing Categories names in the db.
            Profiles are filtered to only those which have been assigned to at
            least one of the supplied CATEGORY values, then their Tweets
            are fetched and stored. Values must be separated by a space and any
            multi-word values or values containing a hash symbol must be
            enclosed in single quotes.
            e.g. -c 'first cat' second 'third cat' '#fourth'
        """
    )
    updateGrp.add_argument(
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
            records.
        """
    )
    updateGrp.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="""If supplied, pretty print Tweet data fetched from the
            Twitter API. Otherwise only a count of Tweets is printed
            upon completion.
        """
    )
    updateGrp.add_argument(
        '-n', '--no-write',
        action='store_true',
        help="If supplied, do not write data to the db."
    )
    updateGrp.add_argument(
        '-u', '--update-all-fields',
        action='store_true',
        help="""If supplied, update all fields when updating an existing
            local Tweet record. Otherwise, the default behavior is to
            only update the favorite and retweet counts of the record.
        """
    )

    args = parser.parse_args()

    if args.available:
        printAvailableCategories()
    elif args.categories:
        inputCategories = args.categories

        categoryResult = db.Category.select(
            IN(db.Category.q.name, inputCategories)
        )
        dbCategoryNames = [c.name for c in list(categoryResult)]
        missing = set(inputCategories) - set(dbCategoryNames)
        assert not missing, "Input categories not found in db: \n- {0}"\
                            .format("\n- ".join(missing))

        # Here the AND is required to include SQLObject j-magic, so that
        # Profiles are filtered by Category.
        profResults = db.Profile.select(
            AND(db.Profile.j.categories,
                IN(db.Category.q.name, inputCategories))
        )
        profCount = profResults.count()
        print("Fetching Tweets for {0:,d} Profiles".format(profCount))

        try:
            campaignRec = db.Campaign.byName(UTILITY_CAMPAIGN)
        except SQLObjectNotFound:
            campaignRec = db.Campaign(
                name=UTILITY_CAMPAIGN,
                searchQuery=None
            )

        if profCount:
            insertOrUpdateTweetBatch(
                profResults,
                args.tweets_per_profile,
                verbose=args.verbose,
                writeToDB=not(args.no_write),
                campaignRec=campaignRec,
                onlyUpdateEngagements=not(args.update_all_fields)
            )
        else:
            raise ValueError("No profiles were found in the categories"
                             " provided: {}".format(inputCategories))


if __name__ == '__main__':
    main()
