# -*- coding: utf-8 -*-
"""
Top tweets application file.
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
    """
    Function for executing command-line arguments.
    """
    if not args or set(args) & set(('-h', '--help')):
        print """\
Print the top N tweets in the Tweet table, ordered by most retweeted.

Usage:
$ python -m lib.query.tweets.topTweets [LIMIT N] [-h|--help]

Options and arguments:
--help : Show this help message and exit.
LIMIT  : Count of tweets to get. Set as 0 to get all.
"""
    else:
        limit = int(args[0]) if args else 1
        printTopTweets(limit)


if __name__ == '__main__':
    main(sys.argv[1:])
