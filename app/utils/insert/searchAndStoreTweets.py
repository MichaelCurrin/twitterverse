#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Search and Store Tweets utility.

Search for tweets in the Twitter API for given input terms, then store
the tweet and the tweet's author data locally, updating or adding objects
as required. The input may be command-line text for easy ad hoc queries,
or the name of an existing Campaign in the db so that its search query string
can be looked up.

Add the default label as Campaign for processed Tweets to signal that the Tweet
was processed by this script. If looking up Tweets using the search query from
a Campaign specified in arguments, then also allocate the processed Tweets
to that Campaign.

Add the default label as Category for Profiles which are processed due to
processing their Tweets.

The persist value is set based on an answer here:
    https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

TODO: Consolidate use of writeToDB and persist in this repo.
"""
import argparse
import os
import sys

from sqlobject import SQLObjectNotFound

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import database as db, flattenText, tweets
from lib.twitter import auth, search
from lib.query.tweets.campaigns import printAvailableCampaigns,\
                                       printCampaignsAndTweets

# Name to assign to Tweets and Profiles created or updated with this utility.
BASE_LABEL = u"_SEARCH_QUERY"
# Setup global API connection object, which needs to be set using a function
# on auth.
API_CONN = None


def searchAndStore(searchQuery, totalCount=200, persist=True,
                   campaignRecs=None):
    """
    Search the Twitter Search API for tweets matching input search terms.

    By default, the tweets are created or updated as Tweet records in the local
    db and then campaign names if supplied as Campaign Records.

    Only matches on tweets for users which had their language set to English
    or undefined.

    @param searchQuery: query text to search on the Twitter API.
    @param totalCount: total count of tweets to attempt to get for the
        search query, as an integer. Defaults to 200, which is the max count
        of tweets received on a single page from the Twitter API.
    @param persist. Default True. If set to False, does not store data
        in the database and only prints to stdout.
    @param campaignRecs: Optional list of campaign records to assign to the
        fetched Tweets. Defaults to None, to not assign any.

    @return processedTweets: count of tweets fetched, unaffected by
        with the data is persisted. This count will be a number up to the
        totalCount argument, but may less if fewer tweets are available in
        the 7-day window, or some tweets which were received were ignored
        because of language restriction applied.
    @return profileRecs: List of local Profile records inserted or updated.
        Defaults to empty list.
    @return tweetRecs: List of local Tweet records inserted or updated.
        Defaults to empty list.
    """
    assert API_CONN, ("Authenticate with Twitter API before doing"
                      " a search for tweets.")

    searchResults = search.fetchTweetsPaging(
        API_CONN,
        searchQuery=searchQuery,
        itemLimit=totalCount
    )
    # TODO: Check the type of full_text and if it needs to be cast
    # to unicode before printing and if the db UnicodeCol handles
    # it correctly.
    processedTweets = 0
    profileRecs = []
    tweetRecs = []
    for fetchedTweet in searchResults:
        if persist:
            profileRec = tweets.insertOrUpdateProfile(fetchedTweet.author)
            profileRecs.append(profileRec)
            data, tweetRec = tweets.insertOrUpdateTweet(fetchedTweet,
                                                        profileRec.id)
            tweetRecs.append(tweetRec)
        else:
            print u"{index:3d} @{screenName}: {message}".format(
                index=processedTweets + 1,
                screenName=fetchedTweet.author.screen_name,
                message=flattenText(fetchedTweet.full_text)
            )
        processedTweets += 1
    print

    return processedTweets, profileRecs, tweetRecs


def main():
    """
    Handle command-line arguments to search for tweets, store data for
    Tweet and Profile objects and then assign Campaigns to Tweets.
    """
    global API_CONN

    parser = argparse.ArgumentParser(
        description="""\
Utility to search for tweets and then the store tweet and profile data locally.

Search with either an ad hoc query, or the name of a stored Campaign which
has a search query set. To create or edit a Campaign, use the Campaign Manager
utility.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    view = parser.add_argument_group("View", "Print data to stdout")
    view.add_argument(
        '-a', '--available',
        action='store_true',
        help="""Output available Campaigns in db, with Tweet counts and
             search query for each."""
    )
    view.add_argument(
        '-t', '--tweets',
        action='store_true',
        help="Output local Tweets grouped by Campaign."
    )
    view.add_argument(
        '-s', '--search-help',
        action='store_true',
        help="""Print guide for writing search queries, with examples of
            syntax safe for the command-line. See Twitter's search
            documentation for full rules."""
        )

    fetch = parser.add_argument_group("Fetch", "Select a search query to"
                                      " get Tweets from Twitter Search API.")
    fetch.add_argument(
        '-c', '--campaign',
        help="""Name of existing campaign in the db. If supplied and the
            Campaign record has a query string, fetch Tweets from the Twitter
            Search API and store, assigning the Campaign name and
            {baseLabel} as campaigns on all processed Tweets.
            This argument may not be used with the --query argument.
        """.format(baseLabel=BASE_LABEL)
    )
    fetch.add_argument(
        '-q', '--query',
        help="""Word or phrase to search on the Twitter API as an ad hoc
            query which is not associated with a Campaign. This argument
            may not be used with the --campaign argument."""
    )
    fetch.add_argument(
        '-C', '--count',
        metavar='N',
        type=int,
        default=200,
        help="Default 200. Max count of tweets to get for the search query.")
    fetch.add_argument(
        '--persist',
        dest='persist',
        action='store_true',
        help="(DEFAULT) Store fetched tweets and profiles in the database.")
    fetch.add_argument(
        '--no-persist',
        dest='persist',
        action='store_false',
        help="Print fetched tweet and profile datas without storing.")
    fetch.set_defaults(persist=True)

    args = parser.parse_args()

    if args.available:
        printAvailableCampaigns()
    if args.tweets:
        printCampaignsAndTweets()
    if args.search_help:
        print search.getSearchQueryHelp()

    if args.query or args.campaign:
        try:
            generalCampaignRec = db.Campaign.byName(BASE_LABEL)
        except SQLObjectNotFound:
            # The campaign manager is not needed externally for creathing
            # this one, since the searchQuery is best set to NULL for
            # this specific campaign and therefore can be automatic.
            generalCampaignRec = db.Campaign(name=BASE_LABEL, searchQuery=None)

        if args.query:
            customCampaignRec = None
            query = unicode(args.query)
        else:
            campaignName = args.campaign
            try:
                customCampaignRec = db.Campaign.byName(campaignName)
            except SQLObjectNotFound as e:
                raise type(e)("Use the campaign manager to create the Campaign"
                              " as name and search query. Name not found: {0}"
                              .format(campaignName))
            query = customCampaignRec.searchQuery
            assert query, "Use the Campaign Mananger to set a search query"\
                          " for the campaign: {0}".format(args.campaign)

        print u'Search query: {0}'.format(query)

        # Use app auth  herefor up to 450 search requests per window, rather
        # than 180.
        API_CONN = auth.getAppOnlyConnection()

        processedCount, profileRecs, tweetRecs = searchAndStore(
            query,
            totalCount=args.count,
            persist=args.persist
        )
        print "Processed tweets: {0:,d}".format(processedCount)

        if profileRecs:
            tweets.assignProfileCategory(
                categoryName=BASE_LABEL,
                profileRecs=profileRecs)

        if tweetRecs:
            tweets.assignTweetCampaign(
                campaignRec=generalCampaignRec,
                tweetRecs=tweetRecs
            )
            if customCampaignRec:
                new, existing = tweets.assignTweetCampaign(
                    campaignRec=customCampaignRec,
                    tweetRecs=tweetRecs
                )
                print u"Tweet Campaign links - new: {new} existing:"\
                    " {existing}".format(
                        new=new,
                        existing=existing
                    )


if __name__ == '__main__':
    main()
