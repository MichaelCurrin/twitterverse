# -*- coding: utf-8 -*-
"""
Search Tweet messages application file.

Search for local db Tweet records using search text and date range parameters.

Usage:
    $ python -m lib.query.search.message --help
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import datetime
from collections import Counter

from sqlobject.sqlbuilder import AND

from lib import database as db


def searchMessages(searchText=None, fromDate=None, toDate=None):
    """
    Given an input phrase, search for Tweets in the local db and return Tweets
    which contain the phrase in their text and are with the date range.

    :param searchText: String as text to search in the Tweet messages.
        Defaults to None to get all Tweets.
    :param fromDate: optional datetime.date object. If included, filter Tweets
        which were on or after this date. Must be used with `toDate`.
    :param toDate: optional datetime.date object. If included, filter Tweets
        which were before or on this date. Must be used with `fromDate`.

    :return query: select results object for the Tweets matching the filter
        parameters, ordered by the Tweet default sorting.
    """
    if searchText:
        query = db.Tweet.select(db.Tweet.q.message.contains(searchText))
    else:
        query = db.Tweet.select()

    if fromDate and toDate:
        # SQL sees a given date as a timestamp at midnight, therefore move
        # it ahead 24 hours and check up to that date, excluding the new day.
        toDate = toDate + datetime.timedelta(days=1)
        query = query.filter(AND(db.Tweet.q.createdAt >= fromDate,
                                 db.Tweet.q.createdAt < toDate))

    return query


def tweetsByProfile(tweets):
    """
    Group received Tweet objects by screen name, with a count against each
    value.
    """
    return Counter(t.profile.screenName for t in tweets)


def tweetsByDate(tweets):
    """
    Group received Tweet objects by date (derived from timestamp),
    with a count against each value.
    """
    return Counter(str(t.createdAt.date()) for t in tweets)


def tweetsByCategory(tweets):
    """
    Group received Tweet objects by Profile category, with a count against each
    value.
    """
    categories = Counter()
    for tweet in tweets:
        tweetCategories = list(tweet.profile.categories)

        if tweetCategories:
            for category in tweetCategories:
                categories.update([category.name])
        else:
            categories.update(['(NOT SET)'])

    return categories


def main():
    """
    Process command-line arguments.
    """
    parser = argparse.ArgumentParser(description="""Search for Tweets in the
                                     local db using optional filters""")

    parser.add_argument(
        '--search',
        metavar='TEXT',
        dest='search_text',
        help="""Text as word or phrase. Search the messages of Tweets
            for this search text. Omit this argument to get all Tweets."""
    )

    parser.add_argument(
        '--output',
        choices=['tweet', 'profile', 'category', 'date'],
        default='tweet',
        help="""Choose the output format for the filtered data. If not
            supplied. Defaults to pretty-printed tweets, ordered by time."""
    )

    dateGroup = parser.add_argument_group("Date range")
    dateGroup.add_argument(
        '--from',
        dest='from_date',
        metavar='N',
        type=int,
        help="""Number of days back from today as start date, inclusive.
            This argument is required when setting a date range, while
            --to can be omitted to use its default."""
    )
    dateGroup.add_argument(
        '--to',
        dest='to_date',
        metavar='N',
        type=int,
        default=0,
        help="""Number of days back from today as end date, inclusive.
            Defaults to 0."""
    )

    args = parser.parse_args()

    if args.from_date:
        fromDate = datetime.date.today() \
                    - datetime.timedelta(days=args.from_date)
        toDate = datetime.date.today() \
                    - datetime.timedelta(days=args.to_date)
    else:
        fromDate = toDate = None

    tweets = searchMessages(args.search_text, fromDate, toDate)

    if args.output == 'profile':
        print(tweetsByProfile(tweets))
    elif args.output == 'category':
        print(tweetsByCategory(tweets))
    elif args.output == 'date':
        print(tweetsByDate(tweets))
    else:
        for t in tweets:
            t.prettyPrint()


if __name__ == '__main__':
    main()
