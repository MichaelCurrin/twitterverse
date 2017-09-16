#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Tweets utility.

Get tweet data from the Twitter API and add to the database.
"""
import os
import sys

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))
from lib import database as db
from lib.tweets import insertOrUpdateTweetBatch


def main(args):
    """
    Run fetching of tweets with command-line input.

    Get ALL profiles in the Profile table and get the most tweets for
    each. Insert into Tweet table or update existing records.
    """
    if not args or set(args) & set(('-h', '--help')):
        print """\
Usage:
$ ./fetchTweets [tweetsPerProfile] [-h|--help]

Options and arguments:
--help          : show this help message and exit.
tweetsPerProfile: Set integer value as count of tweets to get for each profile.
                  The most tweets that can be fetched without paging is 200.
                  Then additional queries will be done.
"""
    else:
        assert args[0].isdigit(), 'Expected tweets per profile argument'\
                                  ' as a numeric string.'
        tweetsPerProfile = int(args[0])

        profResults = db.Profile.select()

        insertOrUpdateTweetBatch(profResults, tweetsPerProfile)


if __name__ == '__main__':
    main(sys.argv[1:])
