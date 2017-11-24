# -*- coding: utf-8 -*-
"""
Campaign queries application file.
"""
from lib import database as db


def printAvailableCampaigns():
    """
    Iterate through Campaigns in db and print out name and Tweet count
    for each.
    """
    print "     Campaign                  |  Tweets | Query"
    print "-------------------------------+---------+-------------------------"
    campaignResult = db.Campaign.select()
    for i, campaign in enumerate(campaignResult):
        print u"{index:3d}. {campaign:25s} | {tweetCnt:7,d}"" | {query:s}"\
            .format(
                index=i + 1,
                campaign=campaign.name,
                tweetCnt=campaign.tweets.count(),
                query=campaign.searchQuery
            )
    print


def printCampaignsAndTweets():
    """
    Iterate through Campaigns in db and print out name and Tweets.
    """
    for i, campaign in enumerate(db.Campaign.select()):
        tweets = list(campaign.tweets)
        print u"{index:d}. {name:s} ({tweetCnt:7,d} tweets)".format(
            index=i + 1,
            name=campaign.name,
            tweetCnt=len(tweets)
        )
        for t in tweets:
            print u" - @{screenName:20} {createdAt} {message}".format(
                screenName=t.profile.screenName,
                createdAt=t.createdAt,
                message=t.message.replace('\n', '').replace('\r', '')
            )
        print


if __name__ == '__main__':
    print "Available campaigns"
    print "==================="
    printAvailableCampaigns()
    print
    print "Tweets"
    print "======"
    printCampaignsAndTweets()
