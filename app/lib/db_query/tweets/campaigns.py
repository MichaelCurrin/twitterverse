# -*- coding: utf-8 -*-
"""
Campaign queries application file.

See lib/twitter/search.py for search query syntax.
"""
from __future__ import absolute_import
from __future__ import print_function
from lib import database as db


def printAvailableCampaigns():
    """
    Iterate through Campaigns in db to print out the name and Tweet count
    for each.

    :return: None
    """
    # TODO: Find an alternative to printing this table in case of large
    # campaign names or tweet counts.
    print("     Campaign                  |  Tweets | Query")
    print("-------------------------------+---------+-------------------------")
    campaignResult = db.Campaign.select()
    for i, campaign in enumerate(campaignResult):
        print(u"{index:3d}. {campaign:25s} | {tweetCnt:7,d}"" | {query:s}"\
            .format(
                index=i + 1,
                campaign=campaign.name,
                tweetCnt=campaign.tweets.count(),
                query=(campaign.searchQuery if campaign.searchQuery is not None
                       else u"NULL")
            ))
    print()


def printCampaignsAndTweets():
    """
    Iterate through Campaigns in db to print out the name and list of
    Tweets in each.

    :return: None
    """
    for i, campaign in enumerate(db.Campaign.select()):
        tweets = list(campaign.tweets)
        print(u"{index:d}. {name:15s} {tweetCnt:,d} tweets".format(
            index=i + 1,
            name=campaign.name,
            tweetCnt=len(tweets)
        ))
        for t in tweets:
            print(u"   - @{screenName:20} | {createdAt} | {message}".format(
                screenName=t.profile.screenName,
                createdAt=t.createdAt,
                message=t.getFlatMessage()
            ))
        print()


if __name__ == '__main__':
    print("Available campaigns")
    print("===================")
    printAvailableCampaigns()
    print()
    print("Tweets")
    print("======")
    printCampaignsAndTweets()
