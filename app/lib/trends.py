# -*- coding: utf-8 -*-
from lib import database as db

from test import _readJSON


def _testTrends():
    # Insert some trends. This will be different in tweepy.
    # Dates? raw is 2017-07-01T13:49:20Z
    tweetData = _readJSON('var/trend_test.json')[0]
    woeid = tweetData['locations'][0]['woeid']
    for rawTrend in tweetData['trends']:
        topic = rawTrend['name']
        volume = rawTrend['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(woeid)
        print 'Created - Trend: {0} | {1} | {2}`.'.format(woeid, topic, volume)
