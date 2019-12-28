"""
Top tweets application file.

Functions are made available for imports but this script can also be run
directly.

Usage:
    $ python -m lib.query.tweets.top_tweets --help
"""
import argparse

from lib import database as db


def printTopTweets(limit=1):
    """
    Prints the most retweeted tweet or tweets in the Tweet table.

    :param limit: Default 1. Upper bound for count of tweets to return,
        as an integer. Set as 0 to return all.
    """

    res = db.Tweet.select().orderBy("retweet_count DESC")

    if res.count():
        for tweet in res[:limit]:
            tweet.prettyPrint()
    else:
        print("Zero tweets found in Tweet table.")


def main():
    """
    Function for executing command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Pretty print the top Tweet"
                                     " records, ordered by most retweeted.")
    parser.add_argument(
        'limit',
        type=int,
        help="Max count of profiles to select. Set as 0 to get all."
    )

    args = parser.parse_args()

    printTopTweets(args.limit)


if __name__ == '__main__':
    main()
