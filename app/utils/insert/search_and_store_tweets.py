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
import os
import sys

from sqlobject import SQLObjectNotFound

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))
import lib
import lib.text_handling
import lib.twitter_api.authentication
import lib.twitter_api.search
import lib.tweets
from lib import database as db
from lib.config import AppConf
from lib.db_query.tweets.campaigns import printAvailableCampaigns, \
                                       printCampaignsAndTweets
from models import Campaign


conf = AppConf()
UTILITY_CATEGORY = UTILITY_CAMPAIGN = conf.get('Labels', 'search')

# Create initial global API connection object, which needs to be set.
API_CONN = None


def search(query, pageCount=1, extended=True):
    """
    Do a Search API query for one or more pages of tweets matching the query.

    After every 100 or slightly fewer tweets, a new request will be done to
    get the next page.

    :param query: Query text to search on the Twitter API.
    :param pageCount: Count pages of tweets to fetch. Each page contains 100
        tweets, which is the Search API's limit.
    :param extended: If True, get the expanded tweet message instead of the
        truncated form.

    :return: Iterable of tweets, across pages if necessary.
    """
    pages = lib.twitter_api.search.fetchTweetsPaging(
        API_CONN,
        searchQuery=query,
        pageCount=pageCount,
        extended=extended
    )
    for page in pages:
        for fetchedTweet in page:
            yield fetchedTweet


def storeTweets(fetchedTweets, persist=True):
    """
    Search the Twitter Search API for tweets matching input search terms.

    Tweets are created or updated and their authors are created or updated
    as Profile records.

    This function does not care about the pages, just individual tweets and
    it logs when every 100 tweets are stored. This will roughly line up with
    pages which can up to 100 tweets on them for Search API.

    :param fetchedTweets: Iterable of tweets from the Twitter API.
    :param persist. Default True. If set to False, does not store data
        in the database and only prints to stdout.

    :return profileRecs: List of local Profile records inserted or updated.
        Defaults to empty list. Note, this will double count a profile which comes
        up multiple times.
    :return tweetRecs: List of local Tweet records inserted or updated.
        Defaults to empty list.
    """
    processedTweets = 0
    profileRecs = []
    tweetRecs = []

    for fetchedTweet in fetchedTweets:
        processedTweets += 1
        if persist:
            profileRec = lib.tweets.insertOrUpdateProfile(fetchedTweet.author)
            profileRecs.append(profileRec)
            data, tweetRec = lib.tweets.insertOrUpdateTweet(
                fetchedTweet,
                profileRec.id
            )
            tweetRecs.append(tweetRec)
            if processedTweets % 100 == 0:
                print "Stored so far: {}".format(processedTweets)
        else:
            # Assume attribute which comes in extended mode, otherwise fall back
            # to the standard mode one.
            try:
                text = fetchedTweet.full_text
            except AttributeError:
                text = fetchedTweet.text

            print u"{index:3d} @{screenName}: {message}".format(
                index=processedTweets,
                screenName=fetchedTweet.author.screen_name,
                message=lib.text_handling.flattenText(text)
            )
    print "Stored at end of search: {}".format(processedTweets)
    print

    return profileRecs, tweetRecs


def assignCategories(profileRecs):
    if profileRecs:
        try:
            utilityCategoryRec = db.Category.byName(UTILITY_CATEGORY)
        except SQLObjectNotFound:
            utilityCategoryRec = db.Category(name=UTILITY_CATEGORY)
        lib.tweets.bulkAssignProfileCategory(
            categoryID=utilityCategoryRec.id,
            profileIDs=(profile.id for profile in profileRecs)
        )


def assignCustomCampaign(customCampaignRec, tweetRecs):
    if customCampaignRec:
        # Reset generator to first item, after using it above within
        # the bulk assign function.
        tweetIDs = (tweet.id for tweet in tweetRecs)
        lib.tweets.bulkAssignTweetCampaign(
            campaignID=customCampaignRec.id,
            tweetIDs=tweetIDs
        )


def assignCampaigns(tweetRecs, utilityCampaignRec, customCampaignRec):
    if tweetRecs:
        # print "Assigning utility's campaign links... ",
        lib.tweets.bulkAssignTweetCampaign(
            campaignID=utilityCampaignRec.id,
            tweetIDs=(tweet.id for tweet in tweetRecs)
        )
        assignCustomCampaign(customCampaignRec, tweetRecs)


@lib.timeit
def searchStoreAndLabel(query, pageCount, persist, utilityCampaignRec,
                        customCampaignRec):
    """
    Fetch and store tweet data then assign labels.

    :param str query: Twitter API search query.
    :param int pageCount: Count of pages of tweets to fetch.
    :param bool persist: If True, persist data, otherwise just print.
        TODO Can this be moved to a variable on class, or global variable
        or env variable so it doesn't have to get passed down to functions?
    :param models.tweets.Campaign utilityCampaignRec:
    :param models.tweets.Campaign customCampaignRec:

    :return: Tuple of processed profile and tweet counts.
    """
    fetchedTweets = search(query, pageCount)

    # TODO Improve this - should values still be returned here. Should
    # we break early on assigning with no persist - how do the other functions
    # operate?
    # Should the logic to print only be moved out to here (and a new function),
    # then skip steps below.
    # Also keep in mind that the verbose option has index for current tweet.
    profileRecs, tweetRecs = storeTweets(fetchedTweets, persist)
    profileCount = len(profileRecs)
    tweetCount = len(tweetRecs)
    if persist:
        print "Profiles: {:,d}".format(profileCount)
        print "Tweets: {:,d}".format(tweetCount)

        assignCategories(profileRecs)
        assignCampaigns(tweetRecs, utilityCampaignRec, customCampaignRec)

    return profileCount, tweetCount


def run(maxPages, persist, campaignName=None, query=None):
    """
    Get labels first before attempting to do searches and then find labels
    are missing.

    :param maxPages: Count.
    :param persist: Flag.
    :param campaignName: Custom campaign name to label tweets with.
    :param query: Search query.

    :return: Tuple of processed profile and tweet counts.
    """
    global API_CONN

    utilityCampaignRec = Campaign.getOrCreate(UTILITY_CAMPAIGN, None)

    if query:
        customCampaignRec = None
        query = unicode(query, 'utf-8')
    else:
        customCampaignRec = Campaign.getOrRaise(campaignName)
        query = customCampaignRec.searchQuery
        assert query, "Use the Campaign Manager to set a search query" \
                      " for the campaign: {0}".format(campaignName)

    # Process the category and campaign records above before fetching
    # data from the API.
    print u"Search query: {0}".format(query)

    # Use app auth here for up to 480 search requests per window, rather
    # than 180 when using the user auth.
    API_CONN = lib.twitter_api.authentication.getAppOnlyConnection()
    profileCount, tweetCount = searchStoreAndLabel(
        query,
        maxPages, persist,
        utilityCampaignRec, customCampaignRec,
    )

    return profileCount, tweetCount


def main():
    """
    Handle command-line arguments to search for tweets, store data for
    Tweet and Profile objects and then assign labels.
    """
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
        help="Default 1. Max count of pages of tweets to get for the search "
             " query, where each page contains up to 100 tweets."
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
        return
    if args.tweets:
        printCampaignsAndTweets()
        return
    if args.search_help:
        print search.getSearchQueryHelp()
        return
    if not (args.query or args.campaign):
        raise ValueError("Either query or campaign args must be set.")

    run(args.pages, args.persist, args.campaign, args.query)


if __name__ == '__main__':
    main()
