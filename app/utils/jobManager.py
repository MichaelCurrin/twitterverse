# -*- coding: utf-8 -*-
"""
Job manager application file.

This does not run the jobs but simply manages the records in the PlaceJob
table.

Usage:
    $ python utils/jobManager.py --help

    # Use functions of module in python console.
    $ python
    >>> from utils import jobManager as jm

    # Do insert for single name.
    >>> jm.insertCountry('United Kingdom')

    # Insert two towns of same name.
    >>> jm.insertTown('Valencia')
    395272 | Valencia        | VE - added
    776688 | Valencia        | ES - added
"""
import datetime
import os
import sys
# Allow this imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))

from sqlobject.dberrors import DuplicateEntryError
from sqlobject.sqlbuilder import OR

from lib.config import AppConf
from lib import database as db


conf = AppConf()


def getCounts(lookbackHours=25):
    """
    Print stats for the PlaceJob table.

    @lookbackHours: number of hours to look back from current time. If the
        job was run after that time then it is considered recently run.
        Defaults to 25 hours to give margin on a running a job every 24 hours.
    """
    print 'PlaceJob stats'
    print
    lookbackTime = datetime.datetime.now() \
        - datetime.timedelta(hours=lookbackHours)

    total = db.PlaceJob.select()
    enabled = db.PlaceJob.selectBy(enabled=True)
    queued = enabled.filter(OR(db.PlaceJob.q.lastCompleted == None,
                               db.PlaceJob.q.lastCompleted < lookbackTime))

    print 'total: {0}'.format(total.count())
    print ' * enabled: {0}'.format(enabled.count())
    print '   * run in past {0} hours: {1}'.format(
        lookbackHours, enabled.count() - queued.count()
    )
    print '   * queued {0}'.format(queued.count())
    print ' * disabled: {0}'.format(total.count() - enabled.count())
    print


def getRecords():
    """
    Print all records in the PlaceJob table using table's default ordering.

    @return: None
    """
    print 'PlaceJob records'
    print 'Ordered by enabled first then oldest completed and oldest'\
        ' attempted.'
    print
    template = '{0:>7} | {1:20} | {2:^8} | {3:^17} | {4:^17} | {5:^10} | {6:^7}'
    print template.format('Job ID', 'Place Name', 'Status', 'Attempted',
                          'Completed', 'Created', 'Enabled')

    for x in db.PlaceJob.select():
        data = (
            x.id,
            x.place.name,
            x.getStatus(asText=True),
            x.lastAttempted.strftime('%x %X') if x.lastAttempted else '-' * 17,
            x.lastCompleted.strftime('%x %X') if x.lastCompleted else '-' * 17,
            str(x.created.date()),
            'Y' if x.enabled else 'N',
        )
        print template.format(*data)
    print


def enableOne(jobID=None):
    """
    Enable one record in PlaceJob table.

    @return: None
    """
    if not jobID:
        jobID = int(raw_input('jobManager. Enter PlaceJob ID /> '))
    db.PlaceJob.get(jobID).set(enabled=True)
    print 'Enabled job ID {0}'.format(jobID)


def disableOne(jobID=None):
    """
    Disable one record in PlaceJob table.

    @return: None
    """
    if not jobID:
        jobID = int(raw_input('jobManager. Enter PlaceJob ID /> '))
    db.PlaceJob.get(jobID).set(enabled=False)
    print 'Disabled job ID {0}'.format(jobID)


def deleteOne(jobID=None):
    """
    Delete one record in PlaceJob table.

    @return: None
    """
    if not jobID:
        jobID = int(raw_input('jobManager. Enter PlaceJob ID /> '))
    db.PlaceJob.deleteBy(id=jobID)
    print 'Deleted job ID {0}'.format(jobID)


def deleteAll():
    """
    Remove all records from PlaceJob table.

    @return: None
    """
    db.PlaceJob.clearTable()
    print 'Table cleared'


def enableAll():
    """
    Set all records in PlaceJob table to enabled.

    @return: None
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=False):
        p.setEnabled()
        count += 1
    print '{0} records enabled'.format(count)


def disableAll():
    """
    Set all records in PlaceJob table to disabled.

    @return: None
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=True):
        p.setDisabled()
        count += 1
    print '{0} records disabled'.format(count)


def insertPlaceByID(placeID, forceEnable=False):
    """
    Expect a Place ID and add a record in PlaceJob for it.

    @param placeID: ID of place to add job for, an an integer.
    @param forceEnable. Default False. If True and a record exists but as
        disabled, set it as enabled.

    @return: None
    """
    place = db.Place.get(placeID)

    output = (place.woeid, place.name)
    try:
        j = db.PlaceJob(placeID=place.id)
        print '{0:10} | {1:15}- added'.format(*output)
    except DuplicateEntryError:
        j = db.PlaceJob.byPlaceID(place.id)

        if not forceEnable:
            print '{0:10} | {1:15} | - found'.format(*output)
        else:
            if j.enabled:
                print '{0:10} | {1:15} | - found and already enabled '\
                    .format(*output)
            else:
                # Force it to be enabled.
                j.set(enabled=True)
                print '{0:10} | {1:15} | - was disabled but now enabled'\
                     .format(*output)


def insertCountry(name, forceEnable=False):
    """
    Add country by name to trend job list.

    Expect country name and add it to the Place Job table, if it exists in
    the Country table. Existing values are skipped.

    @param name: name of country to insert in PlaceJob table.
    @param forceEnable. Default False. If True and a record exists but as
        disabled, set it as enabled.

    @return: None
    """
    results = db.Country.selectBy(name=name)
    assert results.count(), 'Country `{0}` was not found.'.format(name)

    country = results.getOne()
    output = (country.woeid, country.name, country.countryCode)

    try:
        j = db.PlaceJob(placeID=country.id)
        print '{0:10} | {1:15} | {2:2} | - added'.format(*output)
    except DuplicateEntryError:
        j = db.PlaceJob.byPlaceID(country.id)

        if not forceEnable:
            print '{0:10} | {1:15} | {2:2} | - found'.format(*output)
        else:
            if j.enabled:
                print '{0:10} | {1:15} | {2:2} | - found and already enabled '\
                    .format(*output)
            else:
                # Force it to be enabled.
                j.set(enabled=True)
                print '{0:10} | {1:15} | {2:2} | - was disabled but now'\
                    ' enabled'.format(*output)


def insertTown(name, forceEnable=False):
    """
    Add town by name to trend job list.

    Expect town name and add it to the PlaceJob table, if it exists in
    the Town table. Existing values are skipped.

    @param name: name of town to insert in PlaceJob table.
    @param forceEnable. Default False. If True and a record exists but as
        disabled, set it as enabled.

    @return: None
    """
    results = db.Town.selectBy(name=name)
    count = results.count()
    assert count, 'Town `{0}` was not found.'.format(name)

    # Allow iteration through the same town name in different countries:
    for town in results:
        output = (town.woeid, town.name, town.country.countryCode)

        try:
            j = db.PlaceJob(placeID=town.id)
            print '{0:10} | {1:15} | {2:2} | - added'.format(*output)
        except DuplicateEntryError:
            j = db.PlaceJob.byPlaceID(town.id)

            if not forceEnable:
                print '{0:10} | {1:15} | {2:2} | - found'.format(*output)
            else:
                if j.enabled:
                    print '{0:10} | {1:15} | {2:2} | - found and already'\
                        ' enabled'.format(*output)
                else:
                    # Force it to be enabled.
                    j.set(enabled=True)
                    print '{0:10} | {1:15} | {2:2} | - was disabled but now'\
                        ' enabled'.format(*output)


def insertTownsOfCountry(name, forceEnable=False):
    """
    Add all towns of a named country to trend job list.

    Expect country name and add its child towns to the Place Job table, if
    the country exists in the Country table and if it has child towns.
    Existing values are skipped.

    @param name: Name of country to look up towns for and then add jobs for
        towns.
    @param forceEnable. Default False. If True and a record exists but as
        disabled, set it as enabled.

    @return: None
    """
    results = db.Country.selectBy(name=name)
    assert results.count(), 'Country `{0}` was not found.'.format(name)

    country = results.getOne()

    for town in country.hasTowns:
        # Add country code for town.
        output = (town.woeid, town.name, country.countryCode)
        try:
            db.PlaceJob(placeID=town.id)
            print '{0:10} | {1:15} | - added'.format(*output)
        except DuplicateEntryError:
            j = db.PlaceJob.byPlaceID(town.id)

            if not forceEnable:
                print '{0:10} | {1:15} | {2:2} | - found'.format(*output)
            else:
                if j.enabled:
                    print '{0:10} | {1:15} | {2:2} | - found and already'\
                        ' enabled '.format(*output)
                else:
                    # Force it to be enabled.
                    j.set(enabled=True)
                    print '{0:10} | {1:15} | {2:2} | - was disabled but now'\
                        ' enabled'.format(*output)


def _getConfiguredValues():
    """
    Get configured values for fields in job section of config file and return.

    @return countries: list of configured country name strings.
    @return townsForCountries: list of configured country names where towns
        are needed.
    @return towns: list of configured town names.
    """
    countriesStr = conf.get('PlaceJob', 'countries')
    countries =  [v.strip() for v in countriesStr.split('\n') if v]

    townsForCountriesStr = conf.get('PlaceJob', 'townsForCountries')
    townsForCountries = [v.strip() for v in townsForCountriesStr.split('\n')
                         if v]

    townsStr = conf.get('PlaceJob', 'towns')
    towns =  [v.strip() for v in townsStr.split('\n') if v]

    return countries, townsForCountries, towns


def printConfiguredValues():
    """
    Print configured values in job section of config file.

    @return: None
    """
    countries, townsForCountries, towns = _getConfiguredValues()

    print 'Countries'
    print '---------'
    for c in countries:
        print c
    print

    print 'Towns for Countries'
    print '-------------------'
    for tc in countries:
        print tc
    print

    print 'Towns'
    print '-----'
    for t in towns:
        print t


def insertDefaults(forceEnable=False):
    """
    Add default data to PlaceJob table.

    Lookup configured data in trendJobs file and insert records for
    countries and for towns of certain countries.

    The World is always added before reading from configured values.

    @forceEnable. Default False. If True and a record exists but as disabled,
        set it as enabled.

    @return: None
    """
    countries, townsForCountries, towns = _getConfiguredValues()

    print 'World'
    print '-----'
    for w in db.Supername.select():
        insertPlaceByID(w.id)
    print

    print 'Countries'
    print '---------'
    for c in countries:
        insertCountry(c, forceEnable)
    print

    print 'Towns For Countries'
    print '-------------------'
    for tc in townsForCountries:
        insertTownsOfCountry(tc, forceEnable)
    print

    print 'Towns'
    print '-----'
    for t in towns:
        insertTown(t, forceEnable)
    print


def main(args):
    """
    Give ability to enter command-line interactive mode.

    Options are printed on startup or if input is empty.
    If input not valid for the menu options, standard errors are raised
    with appropriate messages.

    @param args: list of command-line arguments as strings.

    @return: None
    """
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage: python utils/jobManager.py [-i|--interactive]'\
            ' [-h|--help]'
        print '--help        : show help message'
        print '--interactive : enter interactive mode and show options.'
    else:
        if set(args) & set(('-i', '--interactive')):
            options = [
                ('quit', sys.exit),
                ('get counts', getCounts),
                ('get records', getRecords),
                ('enable one', enableOne),
                ('disable one', disableOne),
                ('delete one', deleteOne),
                ('enable all', enableAll),
                ('disable all', disableAll),
                ('delete all', deleteAll),
                ('view configured values in conf file', printConfiguredValues),
                ('insert configured values into db', insertDefaults),
            ]

            print 'Job Manager interactive mode.'
            print
            print 'You are now viewing and editing PlaceJob table.'
            print

            assert db.PlaceJob.tableExists(), 'PlaceJob table must be created'\
                ' still.'

            # Loop until exit option is selected.
            while True:
                print 'OPTIONS'
                for i, option in enumerate(options):
                    print '{0:2d}) {1:s}'.format(i, option[0])
                print
                print 'Enter a number. Leave input blank to call up options'\
                    ' again.'
                print

                choice = True

                # Loop until choice is empty string.
                while choice:
                    choice = raw_input('jobManager /> ')
                    try:
                        index = int(choice)
                        command = options[index][1]
                        command()
                    except StandardError as e:
                        print '{0}. {1}'.format(type(e).__name__, str(e))
                print

if __name__ == '__main__':
    main(sys.argv[1:])
