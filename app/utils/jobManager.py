# -*- coding: utf-8 -*-
"""
Job manager application file.

Usage:
    # Enter inactive mode.
    $ python utils/jobManager.py

    # Use functions of module in python console. In particular, do an
    # insert for a country name.
    $ python
    >>> from utils import jobManager as jm
    >>> jm.insertCountry('United Kingdom')
    >>> jm.insertTownsOfCountry('South Africa')
    >>> jm.getRecords()
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
    template = '{0:>7} | {1:20} | {2:^10} | {3:^10} | {4:^10} | {5:^7}'
    print template.format('Job ID', 'Place Name', 'Completed', 'Attempted', 'Created',
                          'Enabled')

    for x in db.PlaceJob.select():
        data = (
            x.id,
            x.place.name,
            str(x.lastCompleted.date()) if x.lastCompleted else '-' * 10,
            str(x.lastAttempted.date()) if x.lastAttempted else '-' * 10,
            str(x.created.date()),
            'Y' if x.enabled else 'N',
        )
        print template.format(*data)
    print


def clear():
    """
    Remove all records from PlaceJob table.
    """
    db.PlaceJob.clearTable()
    print 'Table cleared'


def enableAll():
    """
    Set all records in PlaceJob table to enabled.
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=False):
        p.set(enabled=True)
        count += 1
    print '{0} records enabled'.format(count)


def disableAll():
    """
    Set all records in PlaceJob table to disabled.
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=True):
        p.set(enabled=False)
        count += 1
    print '{0} records disabled'.format(count)


def insertCountry(name, forceEnable=False):
    """
    Add country to trend job list.

    Expect country name and add it to the Place Job table, if it exists in
    the Country table.

    If the record exists, skip it. But if was disabled, enable it.
    """
    results = db.Country.selectBy(name=name)
    assert results.count(), 'Country `{0}` was not found.'.format(name)

    country = results.getOne()
    output = (country.woeid, country.name, country.countryCode)

    try:
        j = db.PlaceJob(placeID=country.id)
        print '{0:10} | {1:15} | {2:2} - added'.format(*output)
    except DuplicateEntryError:
        j = db.PlaceJob.byPlaceID(country.id)

        if not forceEnable:
            print '{0:10} | {1:15} | {2:2} - found'.format(*output)
        else:
            if j.enabled:
                print '{0:10} | {1:15} | {2:2} - found and already enabled '\
                    .format(*output)
            else:
                # Force it to be enabled.
                j.set(enabled=True)
                print '{0:10} | {1:15} | {2:2} - was disabled but now enabled'\
                     .format(*output)


def insertTownsOfCountry(name, forceEnable=False):
    """
    Add towns of a country to trend job list.

    Expect country name and add its child towns to the Place Job table, if
    the country exists in the Country table and if it has child towns.
    """
    results = db.Country.selectBy(name=name)
    assert results.count(), 'Country `{0}` was not found.'.format(name)

    country = results.getOne()

    for town in country.hasTowns:
        # Add country code for town.
        output = (town.woeid, town.name, country.countryCode)
        try:
            db.PlaceJob(placeID=town.id)
            print '{0:10} | {1:15} - added'.format(*output)
        except DuplicateEntryError:
            j = db.PlaceJob.byPlaceID(town.id)

            if not forceEnable:
                print '{0:10} | {1:15} | {2:2} - found'.format(*output)
            else:
                if j.enabled:
                    print '{0:10} | {1:15} | {2:2} - found and already'\
                        ' enabled '.format(*output)
                else:
                    # Force it to be enabled.
                    j.set(enabled=True)
                    print '{0:10} | {1:15} | {2:2} - was disabled but now'\
                        ' enabled'.format(*output)


def insertDefaults(forceEnable=False):
    """
    Add default data to PlaceJob table.

    Lookup configured data in trendJobs file and insert records for
    countries and for towns of certain countries.
    """
    print 'Countries'
    print '---------'
    for c in COUNTRIES:
        insertCountry(c, forceEnable)
    print
    print 'Towns'
    print '-----'
    for t in TOWN_PARENTS:
        insertTownsOfCountry(t, forceEnable)
    print


def main():
    """
    Start command-line interactive mode.

    Options are printed on startup or if input is empty.
    If input not valid for the menu options, standard errors are raised
    with appropriate messages.
    """
    import sys
    options = [
        ('quit', sys.exit),
        ('get counts', getCounts),
        ('get records', getRecords),
        ('enable all', enableAll),
        ('disable all', disableAll),
        ('clear table', clear),
        ('insert configured defaults', insertDefaults),
    ]

    print 'Job Manager interactive mode.'
    print
    print 'You are now viewing and editing PlaceJob table.'
    print

    assert db.PlaceJob.tableExists(), 'PlaceJob table must be created still.'

    while True:
        print 'OPTIONS'
        for i, option in enumerate(options):
            print '{0}) {1}'.format(i, option[0])
        print
        print 'Enter a number. Leave input blank to call up options again.'
        print

        while True:
            choice = raw_input('jobManager /> ')
            if choice:
                try:
                    index = int(choice)
                    command = options[index][1]
                    command()
                except StandardError as e:
                    print '{0}. {1}'.format(type(e).__name__, str(e))
            else:
                print
                break


if __name__ == '__main__':
    main()
