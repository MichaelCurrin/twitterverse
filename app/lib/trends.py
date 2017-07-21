# -*- coding: utf-8 -*-
"""
Retrieve Trend data for places from the Twitter API and insert into the database.
"""
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import database as db
from lib import twitterAuth

# This connection is done once and made available globally.
globalApi = twitterAuth.getAPIConnection()


def insertTrendsForWoeid(woeid, userApi=None, delete=False):
    """
    Receives a WOEID value for a Place, gets up to 50 trend records for the
    Place and stores each of the values in the Trend table.

    From trend API request response, ignore the location which we know and 
    times which we don't need if we just use current time.

    @param woeid: Integer WOEID for a Place.
    @param useApi: tweepy API connection object. Setting this here with a user-authorised object will mean the default app-authorised object at the global level will be ignored.
    @param delete: Boolean, default False. If set to True, delete item after
        it is inserted into db. This is useful for testing.
    """
    print 'Inserting trend data for', woeid
    
    assert isinstance(woeid, int), 'Expected WOEID as type `int` but got type `{}`.'.format(type(woeid).__name__)

    if userApi:
        api = userApi
    else:
        api = globalApi
    response = api.trends_place(woeid)[0]
    trends = response['trends']

    for x in trends:
        topic = x['name']
        volume = x['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(woeid)
        print u'Added trend: {0:4d} | {1:25} - {2:7,d} K | {3:10} - {4}.'\
                .format(t.id, t.topic, t.volume/1000 if t.volume else 0, 
                        t.place.woeid, t.place.name),
        if delete:
            db.Trend.delete(t.id)
            print u'Removed from db.'
        else:
            print
