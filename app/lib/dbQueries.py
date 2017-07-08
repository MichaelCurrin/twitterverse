# -*- coding: utf-8 -*-
"""
Get data from the database.

    # Check row counts across db schema.
    1. $ python -c 'from lib import dbQueries; dbQueries.getCounts();'
"""
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    sys.path.insert(0, os.path.abspath('.'))

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

'''
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