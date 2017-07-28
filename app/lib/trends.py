# -*- coding: utf-8 -*-
"""
Retrieve Trend data for places from the Twitter API and insert into the database.
"""
from sqlobject.sqlbuilder import LIKE, Select

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import database as db
from lib import twitterAuth

# This connection is done once and made available globally.
##globalApi = twitterAuth.getAPIConnection()
# Useful for inserting not when getting search for main or for import...

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


def search(searchStr='', orderByVol=False):
    """
    Search existing trends in the db for topics matching the input string.

    Searches are case insensitive.

    @param searchStr: word or phrase as a string for text to search in the
        topic column of Trend table. Leave as default empty string to
        not filter results. Multi-word searches are not possible except as
        phrases.
    """
    orderBy = 'MaxVol DESC' if orderByVol else 'Trend.topic ASC'
    query = """
        SELECT Trend.topic, MAX(Trend.volume) AS MaxVol
        FROM Trend
        WHERE Trend.topic LIKE '%{0}%'
        GROUP BY Trend.topic
        ORDER BY {1}
    """.format(searchStr, orderBy)
   
    res = db.conn.queryAll(query)

    # note that volume can be added up, but any null values will not be counted.
    print 'Max Volume | Topic'
    for item in res:
        # Making u'' causes errors for some reason for "Динамо"
        print '{0:10,d} | {1}'.format(item[1] if item[1] else -1, item[0])

if __name__ == '__main__':
    search('', orderByVol=True)

# Next step - volume. count distinct places. consider distinct over dates.
# use new attributes in model.
# Date range? timestamp as date col but then consider vol. Range limit?
