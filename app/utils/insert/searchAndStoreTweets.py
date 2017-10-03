#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

"""
import os
import sys
#import time

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import tweets
from lib.twitter import auth, search


#def test():
api = auth.getAppOnlyConnection()

# Match terms which may start with # or @ or neither. Quoting a phrase
# is useful for exact match of a phrase, but then it has to be at start of
# query string, which is a known bug on Twitter API.
festivalList = ['"MamaCity Improv Fest"', 'MCIF', 'MamaCityImprovFest',
                'MamaCityIF']
festivalQuery = ' OR '.join(festivalList)

searchQuery = festivalQuery
#searchQuery = 'Trump'
totalCount = 100

searchRes = search.fetchTweetsPaging(api, searchQuery=searchQuery,
                                     itemLimit=totalCount)

if False:
    for t in searchRes:
        print t.id #, t.author.screen_name

if True:
    for t in searchRes:
        # Add/update tweet author.
        profileRec = tweets.insertOrUpdateProfile(t.author)
        # Add/update the tweet.
        tweetData = tweets.insertOrUpdateTweet(t, profileRec.id)

#if __name__ == '__main__':
#    test()