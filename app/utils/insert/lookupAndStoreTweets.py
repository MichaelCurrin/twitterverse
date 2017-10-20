#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Lookup and Store Tweets utility.
"""
import argparse
import os
import sys

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import tweets
from lib.twitter import auth


def main():
    """
    Command-line interface to lookup tweet GUIDs and store them in the db.
    """
    parser = argparse.ArgumentParser(description="Lookup and Store Tweets"
                                                 " utility.")

    parser.add_argument('tweetGuids',
                        nargs='+',
                        help="List of one or more tweet GUIDS to lookup and"
                             " store in the db, separated by spaces. "
                             " Profiles are also stored so that tweets can be"
                             " linked to them.")
    args = parser.parse_args()

    APIConn = auth.getAppOnlyConnection()
    tweets.lookupTweetGuids(APIConn, args.tweetGuids)


if __name__ == '__main__':
    main()
