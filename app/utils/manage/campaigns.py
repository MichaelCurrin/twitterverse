#!/usr/bin/env python
"""
Campaign manager utility.

Manage values in the Campaign table, setting names and queries. Campaigns
cannot be assigned to Tweets here so must be assigned when adding the
Tweet to the db such as when using the Search and Store Utility.
"""
import argparse
import os
import sys

from sqlobject.dberrors import DuplicateEntryError

# Allow imports to be done when executing this file directly.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
    ),
)

from lib import database as db
from lib.twitter_api.search import getSearchQueryHelp
from lib.db_query.tweets.campaigns import (
    printAvailableCampaigns,
    printCampaignsAndTweets,
)


def main():
    """
    Handle command-line arguments to print or edit data.
    """
    parser = argparse.ArgumentParser(description="Campaign manager utility.")

    viewGrp = parser.add_argument_group("View", "Print data to stdout")
    viewGrp.add_argument(
        "-a",
        "--available",
        action="store_true",
        help="""Output available Campaigns in db, with Tweet counts and
            search query for each.""",
    )
    viewGrp.add_argument(
        "-t",
        "--tweets",
        action="store_true",
        help="Output local Tweets grouped by Campaign.",
    )
    viewGrp.add_argument(
        "-s",
        "--search-help",
        action="store_true",
        help="""Print guide for writing search queries, with examples of
            syntax safe for the command-line. See Twitter's search
            documentation for full rules.""",
    )

    updateGrp = parser.add_argument_group(
        "Update", "Edit pairs of Campaign names and search queries"
    )
    updateGrp.add_argument(
        "-c",
        "--campaign",
        help="""Name of Campaign to create or update. Multiple words, a
            hashtag or quotes must be enclosed in single quotes. This
            argument must be used together with --query argument.""",
    )
    updateGrp.add_argument(
        "-q",
        "--query",
        help="""Single string as a search query (see --search-query help).
            to associate with the campaign name, so it can be used later on
            the Twitter Search API. Sets the search query value on the
            new or existing campaign record as selected by --campaign.
            Overwrites search query without warning. To set as null, use
            `--query null` or `--query None`.""",
    )

    args = parser.parse_args()

    if args.available:
        printAvailableCampaigns()
    if args.tweets:
        printCampaignsAndTweets()
    if args.search_help:
        # TODO Move this to a more global command under help or Twitter syntax
        # guides.
        print(getSearchQueryHelp())

    if args.campaign or args.query:
        assert args.campaign and args.query, (
            "--campaign and --query must" " be used together."
        )

        name = args.campaign

        if args.query.lower() in ("none", "null"):
            query = None
        else:
            query = args.query

        printData = dict(name=name, query=query if query is not None else "NULL")
        try:
            db.Campaign(name=name, searchQuery=query)
            print("Created Campaign: {name} | {query}".format(**printData))
        except DuplicateEntryError:
            db.Campaign.byName(name).set(searchQuery=query)
            print("Updated Campaign: {name} | {query}".format(**printData))


if __name__ == "__main__":
    main()
