# -*- coding: utf-8 -*-
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import database as db

from test import _readJSON


def testTrends():
    """
    Experiment to take Trend values from JSON file insert into the database. This can be done offline while the full version will use connection to tweepy and with tweepy objects instead of JSON.
    """
    # Insert some trends. This will be different in tweepy.
    # Dates? raw is 2017-07-01T13:49:20Z
    tweetData = _readJSON('var/trend_test.json')[0]
    woeid = tweetData['locations'][0]['woeid']
    for rawTrend in tweetData['trends']:
        topic = rawTrend['name']
        volume = rawTrend['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(woeid)
        print 'Created - Trend: {0} | {1} | {2}`.'.format(woeid, topic, volume)
