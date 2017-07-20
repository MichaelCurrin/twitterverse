#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Get Trend data for Places. This is a utility intended to be run as cronjob.

Usage:
    $ ./utils/getTrends.py
"""
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))

from sqlobject import SQLObjectNotFound
import sqlobject.sqlbuilder as builder

from lib import database as db
from lib.setupConf import conf


def queuePlaces():
    """
    Get the WOEIDs of Places to be queued for retrieving Trend data.
    """
    # Get all countries.
    allCountries = db.Country.select()
    countryWoeidList = [c.woeid for c in allCountries]

    # Get towns, for countries which have been marked as towns are required.
    # continentNames = ('Europe', 'North America')
    # continentsFiltered = db.Continent.select(
    #     builder.IN(db.Continent.q.name, continentNames)
    #     )
    # print continentsFiltered.count()
    # for x in continentsFiltered:
    #     print x.name

    # matchedCountries = db.Country.select(builder.IN(db.Country.q.continentID, continentsFiltered))
    # print matchedCountries.count()
    # for x in matchedCountries:
    #     print x.name, len(x.hasTowns)

    # Lookup towns falling in a limited set of countries.
    include = ['South Africa', 'United Kingdom', 'United States']
    filteredCountries = db.Country.select(
        builder.IN(db.Country.q.name, include)
        )
    print filteredCountries
    print filteredCountries.count()
    filteredTowns = db.Town.select(
        builder.IN(db.Town.q.countryID, filteredCountries)
        )
    print filteredTowns
    print filteredTowns.count()


def c():
    countryWoeid = conf.getint('Cron', 'countryWoeid')
    try:
        countryObj = db.Place.byWoeid(countryWoeid)
    except SQLObjectNotFound as e:
        msg = 'Unable to find country WOEID {0} in the database.'\
                .format(countryWoeid)
        print 'ERROR {0}. {1}'.format(type(e).__name__, msg)
        raise type(e)(msg)

    print countryObj

queuePlaces()
