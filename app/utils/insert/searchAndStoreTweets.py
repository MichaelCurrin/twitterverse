#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Search and Store Tweets utility.

Search for tweets in the Twitter API for given search query, then store
the tweet and the tweet author data, adding new objects or updating existing
ones.

The input may be command-line text for easy ad hoc queries, or the name of
an existing Campaign in the db so that its search query string can be
looked up.

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
import datetime
import os
import sys

from sqlobject import SQLObjectNotFound

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db, flattenText, tweets
from lib.config import AppConf
from lib.twitter import auth, search
from lib.query.tweets.campaigns import printAvailableCampaigns, \
                                       printCampaignsAndTweets


conf = AppConf ()
UTILITY_CATEGORY = UTILITY_CAMPAIGN = conf.get('Labels', 'search')

# Create initial global API connection object, which needs to be set using
# a function on auth.
API_CONN = None


def searchAndStore(searchQuery, pageCount=1, persist=True, extended=True):
    """
    Search the Twitter Search API for tweets matching input search terms.

    By default, the tweets are created or updated as Tweet records in the local
    db.

    Only matches on tweets for users which had their language set to English
    or undefined.

    @param searchQuery: Query text to search on the Twitter API.
    @param pageCount: Count pages of tweets to fetch. Each page contains 100
        tweets, which is the Search API's limit.
    @param persist. Default True. If set to False, does not store data
        in the database and only prints to stdout.
    @param extended: If True, get the expanded tweet message instead of the
        truncated form.

    @return processedTweets: count of tweets fetched, unaffected by
        with the data is persisted. This count will be a number up to the
        totalCount argument, but may less if fewer tweets are available in
        the 7-day window.
    @return profileRecs: List of local Profile records inserted or updated.
        Defaults to empty list.
    @return tweetRecs: List of local Tweet records inserted or updated.
        Defaults to empty list.
    """
    assert API_CONN, ("Authenticate with Twitter API before doing"
                      " a search for tweets.")
    searchPages = search.fetchTweetsPaging(
        API_CONN,
        searchQuery=searchQuery,
        pageCount=pageCount,
        extended=extended
    )

    processedTweets = 0
    profileRecs = []
    tweetRecs = []

    for page in searchPages:
        for fetchedTweet in page:
            if persist:
                profileRec = tweets.insertOrUpdateProfile(fetchedTweet.author)
                profileRecs.append(profileRec)
                data, tweetRec = tweets.insertOrUpdateTweet(
                    fetchedTweet,
                    profileRec.id
                )
                tweetRecs.append(tweetRec)
                if (processedTweets + 1) % 100 == 0:
                    print "Processed so far: {}".format(processedTweets + 1)
            else:
                # Assume extended mode, otherwise fall back to standard mode.
                try:
                    text = fetchedTweet.full_text
                except AttributeError:
                    text = fetchedTweet.text

                print u"{index:3d} @{screenName}: {message}".format(
                    index=processedTweets + 1,
                    screenName=fetchedTweet.author.screen_name,
                    message=flattenText(text)
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

    view = parser.add_argument_group(
        "View",
        "Print data to stdout"
    )
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

    fetch = parser.add_argument_group(
        "Fetch",
        "Select a search query to get Tweets from Twitter Search API."
    )
    fetch.add_argument(
        '-c', '--campaign',
        help="""Name of existing campaign in the db. If supplied and the
            Campaign record has a query string, fetch Tweets from the Twitter
            Search API and store. Then assign the given custom Campaign name
            to processed Tweets. This argument may not be used with the
            --query argument.
        """
    )
    fetch.add_argument(
        '-q', '--query',
        help="""Word or phrase to search on the Twitter API as an ad hoc
            query which is not associated with a Campaign. This argument
            may not be used with the --campaign argument."""
    )
    fetch.add_argument(
        '-p', '--pages',
        metavar='N',
        type=int,
        default=1,
        help="Default 1. Count of pages of tweets to get for the search query,"
            " where each page contains up to 100 tweets."
    )
    fetch.add_argument(
        '--persist',
        dest='persist',
        action='store_true',
        help="(DEFAULT) Store fetched tweets and profiles in the database."
    )
    fetch.add_argument(
        '--no-persist',
        dest='persist',
        action='store_false',
        help="Print fetched tweet and profile data without storing."
    )
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
            utilityCampaignRec = db.Campaign.byName(UTILITY_CAMPAIGN)
        except SQLObjectNotFound:
            # The campaign manager is not needed externally for creating
            # this one, since the searchQuery is best set to NULL for
            # this specific campaign and therefore can be automatic.
            utilityCampaignRec = db.Campaign(
                name=UTILITY_CAMPAIGN,
                searchQuery=None
            )

        if args.query:
            customCampaignRec = None
            query = unicode(args.query, 'utf-8')
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

        # Process the category and campaign records above before fetching
        # data from the API.
        print u"Search query: {0}".format(query)

        # Use app auth here for up to 480 search requests per window, rather
        # than 180 when using the user auth.
        API_CONN = auth.getAppOnlyConnection()

        now = datetime.datetime.now()
        processedCount, profileRecs, tweetRecs = searchAndStore(
            query,
            pageCount=args.pages,
            persist=args.persist
        )
        print "Completed tweet processing: {0:,d}".format(processedCount)
        print "took {0}".format(datetime.datetime.now() - now)

        if profileRecs:
            print "Assigning category links... ",
            now = datetime.datetime.now()
            try:
                utilityCategoryRec = db.Category.byName(UTILITY_CATEGORY)
            except SQLObjectNotFound:
                utilityCategoryRec = db.Category(name=UTILITY_CATEGORY)
            tweets.bulkAssignProfileCategory(
                categoryID=utilityCategoryRec.id,
                profileIDs=(profile.id for profile in profileRecs)
            )
            print "DONE"
            print "took {0}".format(datetime.datetime.now() - now)

        if tweetRecs:
            print "Assigning utility's campaign links... ",
            now = datetime.datetime.now()
            tweets.bulkAssignTweetCampaign(
                campaignID=utilityCampaignRec.id,
                tweetIDs=(tweet.id for tweet in tweetRecs)
            )
            print "DONE"
            print "took {0}".format(datetime.datetime.now() - now)

            if customCampaignRec:
                print "Assigning custom campaign links... ",
                now = datetime.datetime.now()
                # Reset generator to first item, after using it above within
                # the bulk assign function.
                tweetIDs = (tweet.id for tweet in tweetRecs)
                tweets.bulkAssignTweetCampaign(
                    campaignID=customCampaignRec.id,
                    tweetIDs=tweetIDs
                )
                print "DONE"
                print "took {0}".format(datetime.datetime.now() - now)


if __name__ == '__main__':
    main()
