#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Main application file.

This can eventually become a CherryPy server, but for now use this file to prototype a minimum working version a Twitterverse trends service.

Filter
    http://sqlobject.org/SelectResults.html#filter-expression
Builder expressions
    http://sqlobject.org/SQLBuilder.html
Like
    https://stackoverflow.com/questions/1003506/executing-sql-like-in-sqlobject

Date range
    https://groups.google.com/forum/#!topic/turbogears/_cwaU86NDfU
"""
import datetime

import sqlobject.sqlbuilder as builder

from lib import database as db
from lib.setupConf import conf
import lib.twitterAuth


auth = lib.twitterAuth.generateToken()
api = lib.twitterAuth.getAPIConnection(auth)


def searchCountry(searchStr='', startswith=False):
    """
    LIKE, startswith and endswith seem to be case insensitive at least when using SQLite as db.
    """
    if startswith:
        condition = db.Country.q.name.startswith(searchStr)
    else:
        condition = builder.LIKE(db.Country.q.name, '%{}%'.format(searchStr))

    res = db.Country.select().filter(condition)

    return res


def searchTowns(searchStr='', startswith=False):
    """
    LIKE, startswith and endswith seem to be case insensitive at least when using SQLite as db.
    """
    if startswith:
        condition = db.Town.q.name.startswith(searchStr)
    else:
        condition = builder.LIKE(db.Town.q.name, '%{}%'.format(searchStr))

    res = db.Town.select().filter(condition)

    return res


def _test():
    global api

    cityWoeid = conf.getint('tests', 'cityWoeid')
    # Ignore 'created_at' and 'as_of' and just use 'trends'. There is a list of one item so we can have to take the item.
    if False:
        cityTrends = api.trends_place(cityWoeid)[0]['trends']
    ##print api.trends_place(cityWoeid)[0]['created_at']
    ## 2017-07-14T22:03:14Z
    ## GMT+0000
    
    '''
    print 'TOWNS SEARCH'
    searchStr = 'ca'
    res = searchTowns(searchStr)
    print
    print str(res)
    print
    for town in res:
        print u'{:10d} - {}'.format(town.woeid, town.name)
    print
    print '-------'

    print 'COUNTRY SEARCH'
    searchStr = 'ica'
    res = searchCountry(searchStr)
    print
    print str(res)
    print
    for country in res:
        print u'{} - {}'.format(country.woeid, country.name)
        for town in country.hasTowns:
            print u' * {:10d} - {}'.format(town.woeid, town.name)
        print
    
    print 'GET TRENDS FOR LOCATION FROM TWEEPY'
    for x in cityTrends:
        topic = x['name']
        volume = x['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(cityWoeid)
        print u'Created - Trend: {0} | {1} | {2}.'.format(cityWoeid, topic, volume)
    '''

    print 'GET HIGHEST TRENDS FOR LOCATION, FOR DATE RANGE'
    # End date will start at midnight so have to add a day to include whole day. And we use < to exclude start of the day.
    endDate = datetime.date.today() + datetime.timedelta(days=1)
    startDate = endDate - datetime.timedelta(days=1)
    print startDate
    print endDate
    # use timezone aware column for timestamp?
    # timezone aware datetime?

    # use datetime.datetime for past 24 hours instead of today?

    # for `byWoeid`, have to use Place name, not Town table, otherwise get error for ambiguous id column.
    city = db.Place.byWoeid(cityWoeid)
    assert city is not None, 'Expected city to be returned for {}.'.format(cityWoeid)
    cityID = city.id

    # Or use `select`. Note that `selectBy` gave same error as other method above on Town.
    # Though in raw SQL this ends up being on Place anyway so no benefit is achieved.
    # cityRes = db.Town.select(db.Town.q.woeid == cityWoeid)
    # city = cityRes.getOne() if cityRes else None
    # assert city is not None, 'Expected city to be returned for {}.'.format(cityWoeid)
    # cityID = city.id

    res = db.Trend.select(
        builder.AND(db.Trend.q.placeID == cityID,
                    db.Trend.q.timestamp >= startDate,
                    db.Trend.q.timestamp < endDate,
                    )
        ).orderBy('volume desc').limit(5)
    print res
    for x in res:
        print x


if __name__ == '__main__':
    _test()
