# -*- coding: utf-8 -*-
"""
Job manager application file.

Usage: $ python utils/jobManager.py
       # OR
       $ python
       >>> from utils import jobManager as jm
       >>> jm.insertCountry('United Kingdom')
       >>> jm.getCounts()
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))

from sqlobject.dberrors import DuplicateEntryError

from etc.trendJobs import COUNTRIES, TOWN_PARENTS
from lib import database as db


def getCounts():
    """
    Print stats for the PlaceJob table.
    """
    print 'PlaceJob stats'
    print
    totalCount = db.PlaceJob.select().count()
    enabledCount = db.PlaceJob.selectBy(enabled=True).count()
    print 'enabled: {}'.format(enabledCount)
    print 'disabled: {}'.format(totalCount - enabledCount)
    print


def getRecords():
    """
    Print all records in the PlaceJob table.
    """
    print 'PlaceJob records'
    print
    template = '{0:>7} | {1:20} | {2:^10} | {3:^10} | {4:^10} | {5:^8}'
    print template.format('Job ID', 'Place Name', 'Completed', 'Attempted', 'Created',
                          'Enabled')

    for x in db.PlaceJob.select():
        data = (
            x.id,
            x.place.name,
            str(x.lastCompleted.date()) if x.lastCompleted else '-' * 10,
            str(x.lastAttempted.date()) if x.lastAttempted else '-' * 10,
            str(x.created.date()),
            x.enabled,
        )
        print template.format(*data)
    print



def clear():
    """
    Remove all records from PlaceJob table.
    """
    db.PlaceJob.clearTable()


def insertCountry(name):
    """
    Add country to trend job list.

    Expect country name and add it to the Place Job table, if it exists in
    the Country table.

    If the record exists, skip it. But if was disabled, enable it.
    """
    c = db.Country.selectBy(name=name).getOne()

    output = (c.woeid, c.countryCode, c.name)

    try:
        db.PlaceJob(placeID=c.id)
        print '{0:10} | {1} | {2:15} - added'.format(*output)
    except DuplicateEntryError:
        j = db.PlaceJob.selectBy(placeID=c.id).getOne()
        if j.enabled:
            print '{0:10} | {1} | {2:15} - found and already enbled '\
                .format(*output)
        else:
            j.set(enabled=True)
            print '{0:10} | {1} | {2:15} - found but made enabled'\
                 .format(*output)


def insertTownsOfCountry(name):
    """
    Add towns of a country to trend job list.

    Expect country name and add its child towns to the Place Job table, if
    the country exists in the Country table and if it has child towns.
    """
    c = db.Country.selectBy(name=name).getOne()
    print '{0} {1}'.format(c.countryCode, c.name)

    for t in c.hasTowns:
        output = (t.woeid, t.name)
        try:
            db.PlaceJob(placeID=t.id)
            print ' * {0:10} | {1:15} - added'.format(*output)
        except DuplicateEntryError:
            j = db.PlaceJob.selectBy(placeID=t.id).getOne()
            if j.enabled:
                print '{0:10} | {1:15} - found and already enbled '\
                    .format(*output)
            else:
                j.set(enabled=True)
                print '{0:10} | {1:15} - found but made enabled'\
                     .format(*output)
    print


def defaultInserts():
    print 'Inserting default values'
    print '========================'
    print
    print 'Countries'
    print '---------'
    for c in COUNTRIES:
        insertCountry(c)
    print
    print 'Towns'
    print '-----'
    for t in TOWN_PARENTS:
        insertTownsOfCountry(t)
    print
