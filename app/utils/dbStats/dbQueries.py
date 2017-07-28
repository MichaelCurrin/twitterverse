# -*- coding: utf-8 -*-
"""
Get data from the database.
"""
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                                      os.pardir))
# Make dirs in app dir importable.
if appDir not in sys.path:
    sys.path.insert(0, appDir)

from collections import Counter

import models
#from models.connection import conn

# Also see places.py
# Consider which of these should be stats, searches, healthchecks and reused
# on API.


def getTrendsFromLocation(woeid=23424977):
    """
    Select trend data already in the database for a given location.

    For test purposes, WOEID defaults to value for United States.
    """
    results = models.Trend.select(models.Place.q.woeid == woeid)
    wordList = [trend.topic for trend in results]

    return wordList


def showTownCountByCountry(byName=True):
    """
    Print a list of all countries and number of towns in each.
    """
    countries = models.Country.select().orderBy('name')

    if byName:
        # Report by country name.
        print 'Country              | Towns'
        print '=====================|======'
        for x in countries:
            print '{0:20} | {1:4,d} {2}'.format(x.name, len(x.hasTowns),
                                                (len(x.hasTowns)/10)*'*')
        print
    else:
        # Report by most towns.
        print 'Country              | Towns'
        print '=====================|======'
        countrySet = Counter()
        for x in countries:
            countrySet.update({x.name: len(x.hasTowns)})
        for y in countrySet.most_common():
            print '{0:20} | {1:4,d} {2}'.format(y[0], y[1], (y[1]/10)*'*')


print getTrendsFromLocation()

showTownCountByCountry()

#def main(args):
#    if not args or set(args) & set(('-h', '--help')):
#        helpMsg = ('Usage: \n'
#            '    python {} [--counts] [--preview] [--town] [--mapping] [--help]')
#        print helpMsg.format(__file__)
#    else:
#        if '--counts' in args:
#            showTableCounts()
#        if '--preview' in args:
#            showTablePreview()
#        if '--town' in args:
#            showTownCountByCountry()
#        if '--mapping' in args:
#            showPlacesMapping()

#
#if __name__ == '__main__':
#    main(sys.argv[1:])

'''
Other stats on places.

# Get topic.
models.Trend.select(models.Trend.q.topic=='#CanadaDay')

# All towns in country ID order
for x in list(db.Town.select().orderBy(db.Town.q.countryID) ):
    print x

# All towns in town name order
for x in list(db.Town.select().orderBy('name') ):
    print x

Show country names and town names
# assuming all countries are set
for x in list(db.Town.select().orderBy(db.Town.q.countryID) ):
    print x.country.name, x.name

# Count of towns per country.
for x in db.Country.select().orderBy("name"):
    print x.name, len(x.hasTowns)

# Towns without countries.
for x in db.Town.select().filter(db.Town.q.country==None):
    print x

'''