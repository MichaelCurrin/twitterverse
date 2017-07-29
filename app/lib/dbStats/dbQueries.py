# -*- coding: utf-8 -*-
"""
Get data from the database.

Usage:
    $ python -m lib.dbStats.dbQueries
"""
from lib import database as db


def getTrendsFromLocation(woeid=23424977):
    """
    Select trend data already in the database for a given location.

    For test purposes, WOEID defaults to value for United States.
    """
    results = db.Trend.select(db.Place.q.woeid == woeid)
    wordList = [trend.topic for trend in results]

    return wordList


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