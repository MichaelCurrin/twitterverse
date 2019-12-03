#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract module Search utility.

Command-line interface to search for tweets on the Twitter API and append the
results to a CSV. No data is added to the DB in this script. The output CSV
file has configurable a name and it will be created if necessary. It is
dedicated to data around search results if necessary. Any custom campaign
defined by the user will added included as a Campaign metadata column in the
CSV.

This script is intended to create many records in a CSV file without writing to
the DB yet, then at a later point a few native SQL statements can be used to
efficiently to do bulk inserts or updates into the db. See also the search
utility in utils/insert directory, which does the extract (fetch from the API)
and load (insert into DB) in one script. Though, that is about 8x slower, by
using the ORM rather than native SQL.

Another advantage of separating the extract to CSV and load into db steps is
that it is a lot easier to debug and repeatedly reproduce the SQL generated in
that loading process, since the SQL is based on rows in a persisted CSV. Using
the ORM approach, any fetched values in memory would be lost when an error is
raised.
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import sys
import os

from sqlobject import SQLObjectNotFound
import six

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db
from lib.extract.search import fetchAndWrite
from lib.twitter_api.search import getSearchQueryHelp
from lib.db_query.tweets.campaigns import printAvailableCampaigns


def view(args):
    """
    Handle the view subcommand.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments. Arguments are intended to be used alone, but
        could be combined.

    :return: None
    """
    if args.available:
        printAvailableCampaigns()
    if args.search_help:
        print(getSearchQueryHelp())


def fetch(args):
    """
    Handle the fetch subcommand.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments.

    :return: None
    """
    if not (args.query or args.campaign):
        return None

    if args.query:
        campaignName = None
        query = six.text_type(args.query, 'utf-8')
    else:
        campaignName = args.campaign
        try:
            customCampaignRec = db.Campaign.byName(campaignName)
        except SQLObjectNotFound as e:
            raise type(e)("Use the campaign manager to create the Campaign"
                          " as name and search query. Name not found: {0}"
                          .format(campaignName))
        query = customCampaignRec.searchQuery
        assert query, "Use the Campaign Manager to set a search query"\
                      " for the campaign: {0}".format(args.campaign)

    print(u"Search query: {0}".format(query))

    fetchAndWrite(
        query,
        campaignName,
        pageCount=args.pages,
    )


def main():
    """
    Handle command-line arguments to do a tweet search and store to a CSV.
    """
    parser = argparse.ArgumentParser(
        description="""Search utility to fetch data and write out to a
        staging CSV. Search with either an ad hoc query, or the name of a
        stored Campaign which has a search query set.
        To create or edit a Campaign, use the Campaign Manager utility.
        """
    )

    subParser = parser.add_subparsers(help="Available subcommands. Use --help"
                                           " after one for more info.")

    viewSubparser = subParser.add_parser(
        "view",
        help="Print exisiting data to stdout."
    )
    viewSubparser.add_argument(
        '-a', '--available',
        action='store_true',
        help="Output available Campaigns in db, with Tweet counts and"
             " search query for each in the db (excludes CSV staging"
             " data not yet added to the db)."
    )
    viewSubparser.add_argument(
        '-s', '--search-help',
        action='store_true',
        help="""Print guide for writing search queries, with examples of
            syntax safe for the command-line. See Twitter's search
            documentation for full rules."""
    )
    viewSubparser.set_defaults(func=view)

    fetchSubparser = subParser.add_parser(
        "fetch",
        help="Select a search query to get Tweets from Twitter Search API."
             " The output is short and clean. For more detailed output on"
             " requests as they are made view the logs in a separate terminal."
             " See the `make help` for appropriate log command."
    )
    fetchSubparser.add_argument(
        '-c', '--campaign',
        help="""Name of existing campaign in the db. If supplied and the
            Campaign record has a query string, fetch Tweets from the Twitter
            Search API and store. The Campaign name is stored in the CSV
            so it can be assigned when loading the data into the db.
            This argument may not be used with the --query argument.
        """
    )
    fetchSubparser.add_argument(
        '-q', '--query',
        help="""Word or phrase to search on the Twitter API as an ad hoc
            query which is not associated with a Campaign. This argument
            may not be used with the --campaign argument."""
    )
    fetchSubparser.add_argument(
        '-p', '--pages',
        metavar='N',
        type=int,
        default=1,
        help="Default: 1. Count of pages of tweets to get for the search"
             " query where each page will contain up to 100 tweets. A search"
             " is done when either N pages are fetched or the API returns"
             " no more pages (all data has been fetched). Set a high number"
             " if youwant to get as much as possible e.g. setting 10000"
             " for pages would return up to 1 million tweets."
    )
    fetchSubparser.set_defaults(func=fetch)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
