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
"""
#import sqlobject
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
    '''

    print 'GET TRENDS FOR LOCATION FROM TWEEPY'
    global api
    cityWoeid = conf.getint('tests', 'cityWoeid')
    # Ignore 'created_at' and 'as_of' and just use 'trends'. There is a list of one item so we can have to take the item.
    cityTrends = api.trends_place(cityWoeid)[0]['trends']

    for x in cityTrends:
        topic = x['name']
        volume = x['tweet_volume']
        t = db.Trend(topic=topic, volume=volume).setPlace(cityWoeid)
        print u'Created - Trend: {0} | {1} | {2}.'.format(cityWoeid, topic, volume)


if __name__ == '__main__':
    _test()
