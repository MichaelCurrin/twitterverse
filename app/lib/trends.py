# -*- coding: utf-8 -*-
"""

"""
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))


def insertTrendsForWoeid(woeid, api, delete=False):
    """
    Receives a WOEID value for a Place, gets up to 50 trend records for the
    Place and stores each of the values in the Trend table.

    From trend API request response, ignore the location which we know and 
    times which we don't need if we just use current time.

    @param woeid: Integer WOEID for a Place.
    @param delete: Boolean, default False. If set to True, delete item after
        it is inserted into db. This is useful for testing.
    """
    assert isinstance(woeid, int), 'Expected WOEID as type `int` but got type `{}`.'.format(type(woeid).__name__)
    response = api.trends_place(woeid)[0]
    trends = response['trends']
    #print 'trends', woeid
    for x in trends:
        topic = x['name']
        volume = x['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(woeid)
        print u'Added trend: {0:4d} | {1:25} - {2:10,d} | {3:10} - {4}.'\
                .format(t.id, t.topic, t.volume if t.volume else 0, 
                        t.place.woeid, t.place.name)
        if delete:
            db.Trend.delete(t.id)
            print u'Removed from db.'
