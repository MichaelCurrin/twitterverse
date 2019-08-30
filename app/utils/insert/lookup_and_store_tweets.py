#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Lookup and Store Tweets utility.

Lookup tweets on Twitter by the GUID and then stores the profile and tweet
data in the local db.

TODO: Use the system category and campaign as set in app.conf file.
"""
import argparse
import os
import sys

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))
from lib import tweets
from lib.twitter_api import authentication


def main():
    """
    Command-line interface for Lookup and Store Tweets utility.
    """
    parser = argparse.ArgumentParser(
        description="""Lookup and Store Tweets utility. Fetches a tweet from
            the Twitter API given its GUID. Stores or updates the author
            Profile and Tweet in the db."""
        )
    parser.add_argument(
        'tweetGUIDs',
        metavar='TWEET_GUID',
        nargs='+',
        help="""List of one or more Tweet GUIDs to lookup, separated by spaces.
            The Tweet 'GUID' in the local db is equivalent to the Tweet 'ID'
            on the Twitter API.""")
    parser.add_argument(
        '-u', '--update-all-fields',
        action='store_true',
        help="""If supplied, update all fields when updating an existing
            local Tweet record. Otherwise, the default behavior is to
            only update the favorite and retweet counts of the record."""
    )
    args = parser.parse_args()

    APIConn = authentication.getAppOnlyConnection()
    tweets.lookupTweetGuids(
        APIConn,
        args.tweetGUIDs,
        onlyUpdateEngagements=not(args.update_all_fields)
    )


if __name__ == '__main__':
    main()
