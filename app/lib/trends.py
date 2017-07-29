# -*- coding: utf-8 -*-
"""
Retrieve Trend data for places from the Twitter API and insert into the
database.

To execute this file directly but still enable imports from app dir:
    $ cd app
    $ python -m lib.trends
"""
from lib import database as db
from lib import twitterAuth


# Global object to be used as api connection. During execution of the insert
# function, this can be setup once with default app then reused later,
# to avoid time calling Twitter API. It can be left as null if not needed.
appApi = None


def insertTrendsForWoeid(woeid, userApi=None, delete=False):
    """
    Receives a WOEID value for a Place, gets up to 50 trend records for the
    Place and stores each of the values in the Trend table.

    From trend API request response, ignore the location which we know and
    times which we don't need if we just use current time.

    @param woeid: Integer WOEID for a Place.
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
            appApi = twitterAuth.getAPIConnection()
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
# Where do search functions belong?
