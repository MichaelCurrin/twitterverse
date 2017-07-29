# -*- coding: utf-8 -*-
"""
Trends application file.

Usage:
    $ python -m lib.trends
"""
from lib import database as db
from lib.twitter import auth


# Global object to be used as api connection. During execution of the insert
# function, this can be setup once with default app then reused later,
# to avoid time calling Twitter API. It can be left as null if not needed.
appApi = None


def insertTrendsForWoeid(woeid, userApi=None, delete=False):
    """
    Retrieve Trend data for places from the Twitter API and insert into the
    database.

    Receives a WOEID value for a Place, gets up to 50 trend records for the
    Place and stores each of the values in the Trend table.

    From trend API request response, we ignore the location part which we know
    alread and the time part since we just use current time.

    @param woeid: Integer for WOEID value of a Place.
    @param useApi: tweepy API connection object. Set this with a
        user-authorised connection to skip the default behaviour of generating
        and using an app-authorised connection.
    @param delete: Boolean, default False. If set to True, delete item after
        it is inserted into db. This is useful for testing.
    """
    global appApi

    print 'Inserting trend data for', woeid

    assert isinstance(woeid, int), ('Expected WOEID as type `int` but got '
                                    'type `{}`.'.format(type(woeid).__name__))

    if userApi:
        # Use user token.
        api = userApi
    else:
        # Use app token.
        if not appApi:
            # Set it if necessary and then reuse it next time.
            appApi = auth.getAPIConnection()
        api = appApi
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
