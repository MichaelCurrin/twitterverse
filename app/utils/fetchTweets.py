#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Profiles utility.
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
    Run fetching of tweets with tweetsPerProfile as command-line argument.

    Get all profiles in the Profile table and get the most tweets for
    each. Insert into Tweet table or update existing records.
    """

    kwargs = {}
    if args:
        assert args[0].isdigit(), 'Expected tweets per profile argument'\
                                  ' as a number.'
        kwargs['tweetsPerProfile'] = int(args[0])

    profResults = db.Profile.select()

    insertOrUpdateTweetBatch(profResults, **kwargs)


if __name__ == '__main__':
    main(sys.argv[1:])
