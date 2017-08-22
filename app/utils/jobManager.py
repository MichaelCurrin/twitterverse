# -*- coding: utf-8 -*-
"""
Usage: $ python utils/jobManager.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir)))

from sqlobject.dberrors import DuplicateEntryError

from lib import database as db


def getItems():
    print 'PlaceJob items'
    print '=============='
    totalCount = db.PlaceJob.select().count()
    enabledCount = db.PlaceJob.selectBy(enabled=True).count()
    print 'enabled: {}'.format(enabledCount)
    print 'disabled: {}'.format(totalCount - enabledCount)
    print

    for x in db.PlaceJob.selectBy(enabled=True):
        print '{} {} {}'.format(x.placeID, x.place.name, x.created)


# Focus on mostly English speaking countries.
countries = ['United States', 'South Africa', 'Ireland', 'United Kingdom',
             'Canada', 'Australia', 'New Zealand', 'France', 'Italy',
             'Germany', 'Spain']

# Get all towns within these countries.
getTownsFor = ['South Africa', 'Ireland']

for c in countries:
    o = db.Country.selectBy(name=c).getOne()
    print o.id, o.countryCode, o.name,
    try:
        db.PlaceJob(placeID=o.id)
        print '- inserted'
    except DuplicateEntryError:
        print '- skipped'

getItems()
