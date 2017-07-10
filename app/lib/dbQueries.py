# -*- coding: utf-8 -*-
"""
Get data from the database.
    
Usage (from app dir):
    # Check all stats.
    1. $ python lib/dbQueries.py

    # Check row counts across db schema.
    1. $ python -c 'from lib import dbQueries; dbQueries.getCounts();'
"""
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))

import models
from models.connection import conn


def getCounts():
    """
    Output a table of table names and row counts separated by a pipe.
    The column widths are adjusted to accomodate the widest strings.
    """
    summaryData = []
    nameWidth = 1
    countWidth = 1

    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        count = tableClass.select().count()
        summaryData.append((tableName, count))

        if len(tableName) > nameWidth:
            nameWidth = len(tableName)
        if len(str(count)) > countWidth:
            countWidth = len(str(count))

    template = '{0:%ss} | {1:%sd}' % (nameWidth, countWidth)

    print 'Tables and Records\n'
    for row in summaryData:
        print template.format(*row)
    print
    print


def getPreview(maxResults=10):
    print 'Results preview\n'.format(maxResults)
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        results = tableClass.select()
        limitedResults = results.limit(maxResults)
        heading = '{0} ({1})'.format(tableName, results.count())
        print heading
        print '-'*len(heading)
        for r in limitedResults:
            print r
        print
    print
    print


def exportNetworkData():
    """
    Create output showing Place objects to parent Places. Export as CSV file can be used as input for the Google Fusion tables network graph.

    This could be improved using `csv` library instead.
    """
    data = [('Location', 'Parent')]
    for x in models.Continent.select().orderBy('name'):
        data.append((x.name, x.supername.name))
    for x in models.Country.select().orderBy('name'):
        data.append((x.name, x.continent.name))
    for x in models.Town.select().orderBy('name'):
        data.append((x.name, x.country.name))

    filename = os.path.abspath('var/networkGraphData.csv')
    print filename
    with open(filename, 'w') as writer:
        for row in data:
            r = u'"{0}", "{1}"\n'.format(*row)
            # Convert to ASCII for writer. Or, make writer unicode acceptable.
            r = r.encode('ascii', 'ignore')
            print r,
            writer.write(r)

def getTrendsFromLocation(woeid=23424977):
    """
    Select trend data already in the database for a given location.

    For test purposes, WOEID defaults to value for United States.
    """
    results = models.Trend.select().filter(models.Place.q.woeid==woeid)
    wordList = [trend.topic for trend in results]

    return wordList


if __name__ == '__main__':
    getCounts()
    getPreview()
    #exportNetworkData()

'''

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