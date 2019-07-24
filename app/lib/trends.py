# -*- coding: utf-8 -*-
"""
Trends application file.

Usage:
    $ python -m lib.trends
"""
import datetime

from lib import database as db
from lib.twitter_api import auth


# Global object to be used as api connection. During execution of the insert
# function, this can be setup once with default app then reused later,
# to avoid time calling Twitter API. It can be left as null if not needed.
appApi = None


def insertTrendsForWoeid(woeid, userApi=None, delete=False, verbose=True):
    """
    Retrieve Trend data from the Twitter API for a place and insert into the
    database.

    Expects a WOEID value for a Place, gets up to 50 trend records for the
    Place as limited by the API and stores each of the values in the
    Trend table.

    From the API request response, we ignore the location field (which we know
    already) and the time field (since we just use current time as close
    enough).

    For printing of the added trend, it works normally to print the string
    as u'...{}'.format, even if the value is u'Jonathan Garc\xeda'. This
    was tested in the bash console of Python Anywhere.
    However, when running as a cronjob and outputting to log file, it appears
    to be converted to ASCII and throws an error. Therefore encoding to ASCII
    and replacing the character is done, even though it less readable.

    @param woeid: Integer for WOEID value of a Place.
    @param userApi: tweepy API connection object. Set this with a
        user-authorised connection to skip the default behaviour of generating
        and using an app-authorised connection.
    @param delete: Boolean, default False. If set to True, delete item after
        it is inserted into db. This is useful for testing.
    @param verbose: Print details for each trend added.
    """
    global appApi

    now = datetime.datetime.now().strftime('%x %X')
    print "{time} Inserting trend data for WOEID {woeid}".format(
        time=now,
        woeid=woeid
    )

    assert isinstance(woeid, int), ("Expected WOEID as type `int` but got "
                                    "type `{}`.".format(type(woeid).__name__))

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

        if verbose:
            # Handle printing of unicode characters not in ascii range.
            decodedTopic = t.topic.encode('ascii', 'replace')
            print "Added trend: {tweetID:4d} | {topic:25} - {volume:7,d} K |"\
                " {woeid:10} - {place}.".format(
                    tweetID=t.id,
                    topic=decodedTopic,
                    volume=(t.volume / 1000 if t.volume else 0),
                    woeid=t.place.woeid,
                    place=t.place.name
                )

        if delete:
            db.Trend.delete(t.id)
            if verbose:
                print " - removed from db."

    return len(trends)
