# -*- coding: utf-8 -*-
"""
Top tweets application file.

Usage:
    $ python -m lib.query.tweets.topTweets [LIMIT]
"""
import sys

from lib import database as db


def printTopTweets(limit=1):
    """
    Prints the most retweeted tweet or tweets in the Tweet table.

    @param limit: Default 1. Upper bound for count of tweets to return,
        as an integer.
    """

    res = db.Tweet.select().orderBy('retweet_count DESC')

    if res.count():
        for tweet in res[:limit]:
            tweet.prettyPrint()
    else:
        print 'Zero tweets found in Tweet table.'


def main(args):
    limit = int(args[0]) if args else 1
    printTopTweets(limit)


if __name__ == '__main__':
    main(sys.argv[1:])
