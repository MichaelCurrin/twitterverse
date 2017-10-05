#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Search and Store Tweets utility.

Search for tweets in the Twitter API for given input terms, then store
the tweet and the tweet's author data locally, updating or adding objects
as required.

Send search terms as arguments to the command-line tool to search for
them. See the usage instructions. The persist value is set based on
an answer here: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
"""
import argparse
import os
import sys

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import tweets
from lib.twitter import auth, search


# Setup global API connection object, which needs to be set using a function
# on auth.
API_CONN = None


def searchAndStore(searchQuery, totalCount=200, persist=True):
    """
    Search Twitter API for tweets matching input search terms.

    Only matches on tweets for users which had their language set to English
    or undefined.

    @param searchQuery: search query as a string containing terms.
    @param totalCount: total count of tweets to attempt to get for the
        search query, as an integer. Defaults to 200, which is the max count
        of tweets received on a single page from the Twitter API.
    @param persist. Default True. If set to False, does not store data
        in the database and only prints to stdout.

    @return processedCount: count of tweets processed, as an integer.
        This will be a number up to the totalCount flag, but may less if
        fewer tweets are available in the 7-day window, or some tweets
        which were received were ignored because of language restriction
        we apply.
    """
    assert API_CONN, ("Authenticate with Twitter API before doing"
                      " a search for tweets.")

    searchRes = search.fetchTweetsPaging(API_CONN, searchQuery=searchQuery,
                                         itemLimit=totalCount)
    processedCount = 0
    for t in searchRes:
        if persist:
            # Add/update tweet author.
            profileRec = tweets.insertOrUpdateProfile(t.author)
            # Add/update the tweet.
            tweetData = tweets.insertOrUpdateTweet(t, profileRec.id)
        else:
            text = t.full_text.replace('\n', ' ').replace('\r', ' ')
            print u'@{0}: {1}'.format(t.author.screen_name, text)
        processedCount += 1

    return processedCount


def main():
    """
    Handle command-line arguments to search for tweets and then store data for
    Tweet and Profile objects.
    """
    global API_CONN

    parser = argparse.ArgumentParser(
        description="Utility to search for tweets, then store tweet"
                    " and store profile data locally.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Set value for terms list.
    searchQueryHelp = """\
Search tweet messages on Twitter API which match a query
string of one or more terms. See rules on the Twitter
API's search documentation.

Any double quotes or hashtags must be escaped on
the command-line, as covered below.

Examples:
 * message contains all terms, in any order.
    - wordA
    - wordA wordB wordC wordD
 * message contains at least one of the terms.
    - wordA OR wordB
    - @handleA OR wordB OR wordC
 * message contains hashtag terms.
    - \\#abc
    - '#def OR xyz OR #ghi'
 * message contains exact phrases. Note that
    quoted phrases must appear before other terms.
    - \\"My Quote\\"
    - '"My Quote" OR "Another quote" OR wordC'"""
    parser.add_argument('terms', metavar='TERM', nargs='+',
                        help=searchQueryHelp)

    # Set value count. Allows -c N or -c=N syntax.
    parser.add_argument('-c', '--count', metavar='N', type=int, default=200,
                        help="Default 200. Max count of tweets to get for the"
                             " search query.")

    # Set persist boolean value.
    parser.add_argument('--persist', dest='persist', action='store_true',
                        help="Store tweets and profiles in database."
                             " Defaults to on.")
    parser.add_argument('--no-persist', dest='persist', action='store_false',
                        help="Print tweet and profile data without storing.")
    parser.set_defaults(persist=True)

    args = parser.parse_args()

    # Combine trimmed list of strings into single string.
    searchQuery = u' '.join(args.terms)
    print u'Search query: {0}'.format(searchQuery)

    # Use app auth for up to 450 search requests per window, rather than 180.
    API_CONN = auth.getAppOnlyConnection()

    processedCount = searchAndStore(args.terms, totalCount=args.count,
                                    persist=args.persist)
    print 'Processed tweets: {0}'.format(processedCount)


if __name__ == '__main__':
    main()
