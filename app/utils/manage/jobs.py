#!/usr/bin/env python
"""
Job manager utility.

This does not run the jobs but simply manages the records in the PlaceJob
table.

This is easier to managing jobs using SQL. Though this could been done in a
simpler way using a SQL UI or even a YAML config. Also, once I set this up I
didn't need that much flexibility, so the inserting of configured data and
adding a few records with the SINGLE options are the most import. The rest
doesn't have to exist in this tool - but this tool exists and works now so use
it.

Usage: $ ./job.py --help

    # Or use functions of module in python console.
    $ python
    >>> from utils.manager import jobs
    >>> jobs.insertPlaceByName('United Kingdom')
"""
import os
import sys

from sqlobject.dberrors import DuplicateEntryError

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db, jobs
from lib.config import AppConf


conf = AppConf()


def getCounts():
    """
    Print count stats for the PlaceJob table.
    """
    print('PlaceJob stats')
    print()

    total = db.PlaceJob.select()
    enabled = db.PlaceJob.selectBy(enabled=True)
    queued = enabled.filter(jobs.orCondition())

    print('total: {0:,d}'.format(total.count()))
    print(' * enabled: {0:,d}'.format(enabled.count()))
    print('   * queued to run: {0:,d}'.format(queued.count()))
    print('   * not queued to run: {0:,d}'.format(
        enabled.count() - queued.count()
    ))
    print(' * disabled: {0:,d}'.format(total.count() - enabled.count()))
    print()


def getRecords():
    """
    Print all records in the PlaceJob table.

    :return: None
    """
    print('PlaceJob records')
    print('Ordered by enabled first then oldest completed and oldest'
          ' attempted.')
    print()
    template = \
        '{0:>7} | {1:20} | {2:^8} | {3:^17} | {4:^17} | {5:^10} | {6:^7}'
    print(template.format('Job ID', 'Place Name', 'Status', 'Attempted',
                          'Completed', 'Created', 'Enabled'))

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
        print(template.format(*data))
    print()


def resetTimes(jobID=None):
    """
    Reset the times for one PlaceJob record.

    Set the last completed and last attempted times to None. This is useful
    in testing in order to reset a job which may have just run.

    :param jobID: Database record ID for PlaceJob table.

    :return: None
    """
    if not jobID:
        jobID = int(input("jobManager. Reset last attempted and last"
                          " completed times - enter PlaceJob ID /> "))
    db.PlaceJob.get(jobID).set(lastAttempted=None, lastCompleted=None)
    print('Removed attempted and completed times for job ID {0}'.format(jobID))


def enableOne(jobID=None):
    """
    Enable one record in PlaceJob table.

    :return: None
    """
    if not jobID:
        jobID = int(input("jobManager. Enable - enter PlaceJob ID /> "))
    db.PlaceJob.get(jobID).setEnabled()
    print('Enabled job ID {0}'.format(jobID))


def disableOne(jobID=None):
    """
    Disable one record in PlaceJob table.

    :param jobID: Database record ID for PlaceJob table.

    :return: None
    """
    if not jobID:
        jobID = int(input("jobManager. Disable - enter PlaceJob ID /> "))
    db.PlaceJob.get(jobID).setDisabled()
    print('Disabled job ID {0}'.format(jobID))


def deleteOne(jobID=None):
    """
    Delete one record in PlaceJob table.

    :param jobID: Database record ID for PlaceJob table.

    :return: None
    """
    if not jobID:
        jobID = int(input("jobManager. Delete - PlaceJob ID /> "))
    db.PlaceJob.deleteBy(id=jobID)
    print('Deleted job ID {0}'.format(jobID))


def deleteAll():
    """
    Remove all records from PlaceJob table.

    :return: None
    """
    db.PlaceJob.clearTable()
    print("All PlaceJob records deleted.")


def enableAll():
    """
    Set all records in PlaceJob table to enabled.

    :return: None
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=False):
        p.setEnabled()
        count += 1
    print("{0} records enabled".format(count))


def disableAll():
    """
    Set all records in PlaceJob table to disabled.

    :return: None
    """
    count = 0
    for p in db.PlaceJob.selectBy(enabled=True):
        p.setDisabled()
        count += 1
    print("{0} records disabled".format(count))


def insertPlaceByName(placeName=None):
    """
    Expect a Place name and add a record in PlaceJob for it.

    A Place could be Supername, Country or a Town. Continents should not
    be looked up.

    Multiples places with the same name will all be added e.g. add both
    towns for input 'Valencia'.

    :param placeName: Default name of place to add job for, as a string.
        If not supplied, prompt user for input text.

    :return: None
    """
    if not placeName:
        placeName = input("jobManager. Insert - enter place name /> ")

    results = db.Place.selectBy(name=placeName)

    if results.count():
        for place in results:
            output = (place.woeid, place.name)
            try:
                db.PlaceJob(placeID=place.id)
                print("{0:10} | {1:15} | -> added".format(*output))
            except DuplicateEntryError:
                print("{0:10} | {1:15} | -> already exists".format(*output))
    else:
        raise ValueError('The name `{0}` was not found in Place table.'
                         .format(placeName))


def insertTownsOfCountry(countryName=None):
    """
    Add all towns of a country to trend job list, excluding country itself.

    Expect country name and add its child towns to the Place Job table, if
    the country exists in the Country table and if it has child towns.
    Existing values are skipped.

    :param countryName: Default None. Name of country to look up towns for
        and then add as jobs.

    :return: None
    """
    if not countryName:
        countryName = input("jobManager. Intert towns - enter country"
                            " name /> ")

    results = db.Country.selectBy(name=countryName)

    if results.count():
        # Expect one result exactly, since country names will be never
        # duplicated, unlike towns.
        country = results.getOne()

        towns = country.hasTowns
        if not towns:
            raise ValueError("Country `{0}` has no towns linked to it which"
                             " can be added.".format(countryName))
        # Add each town on the country.
        for town in towns:
            # Include country code of town.
            output = (town.woeid, town.name, country.countryCode)
            try:
                db.PlaceJob(placeID=town.id)
                print("{0:10} | {1:15} | {2:2} | -> added".format(*output))
            except DuplicateEntryError:
                print("{0:10} | {1:15} | {2:2} | -> already exists"
                      .format(*output))
    else:
        raise ValueError("Country `{0}` was not found.".format(countryName))


def _getConfiguredValues():
    """
    Get configured values for fields in job section of config file and return.

    :return countries: list of configured country name strings.
    :return townsForCountries: list of configured country names where towns
        are needed.
    :return towns: list of configured town names.
    """
    countriesStr = conf.get('PlaceJob', 'countries')
    countries = [v.strip() for v in countriesStr.split('\n') if v]

    townsForCountriesStr = conf.get('PlaceJob', 'townsForCountries')
    townsForCountries = [v.strip() for v in townsForCountriesStr.split('\n')
                         if v]

    townsStr = conf.get('PlaceJob', 'towns')
    towns = [v.strip() for v in townsStr.split('\n') if v]

    return countries, townsForCountries, towns


def printConfiguredValues():
    """
    Print configured values in job section of config file.

    :return: None
    """
    countries, townsForCountries, towns = _getConfiguredValues()

    print("World")
    print("-----")
    for superObj in db.Supername.select():
        print(superObj.name)
    print()

    print("Countries")
    print("---------")
    for c in countries:
        print(c)
    print()

    print("Towns for Countries")
    print("-------------------")
    for tc in townsForCountries:
        print(tc)
    print()

    print('Towns')
    print('-----')
    for t in towns:
        print(t)
    print()


def insertDefaults():
    """
    Add default data to PlaceJob table.

    Lookup configured data in trendJobs file and insert records for countries
    and for towns of certain countries.

    The World is always added before reading from the configured default
    values.

    :return: None
    """
    print('World')
    print('-----')
    for superObj in db.Supername.select():
        insertPlaceByName(superObj.name)
    print()

    # Get user-configured text values of job records to add.
    countries, townsForCountries, towns = _getConfiguredValues()

    print('Countries')
    print('---------')
    for c in countries:
        insertPlaceByName(c)
    print()

    print('Towns For Countries')
    print('-------------------')
    for tc in townsForCountries:
        insertTownsOfCountry(tc)
    print()

    print('Towns')
    print('-----')
    for t in towns:
        insertPlaceByName(t)
    print()


def main(args):
    """
    Give ability to enter command-line interactive mode.

    Options are printed on startup or if input is empty. If input not valid
    for the menu options, standard errors are raised with appropriate messages.

    :param args: list of command-line arguments as strings.

    :return: None
    """
    if not args or set(args) & {'-h', '--help'}:
        print('Usage: python utils/job_manager.py [-i|--interactive]'
              ' [-h|--help]')
        print('--help        : show help message')
        print('--interactive : enter interactive mode and show options.')
    else:
        if set(args) & {'-i', '--interactive'}:
            options = [
                ('QUIT', sys.exit),
                ('VIEW counts', getCounts),
                ('VIEW records', getRecords),
                ('SINGLE - enable one PlaceJob record', enableOne),
                ('SINGLE - disable', disableOne),
                ('SINGLE - delete', deleteOne),
                ('SINGLE - reset times', resetTimes),
                ('ALL - enable all PlaceJob records', enableAll),
                ('ALL - disable', disableAll),
                ('ALL - delete', deleteAll),
                ('CREATE a job from specified town or country name',
                 insertPlaceByName),
                ('CREATE a job for all towns within a specified country name',
                 insertTownsOfCountry),
                ('VIEW the list of pre-configured places to watch, set in the'
                 ' app config file',
                 printConfiguredValues),
                ('INSERT - Watch all pre-configured places',
                 insertDefaults),
            ]

            print('Job Manager interactive mode.')
            print()
            print('You are now viewing and editing the PlaceJob table'
                  ' records. Actions like enable only work after a record'
                  ' has been created using CREATE or INSERT options.')
            print()

            assert db.PlaceJob.tableExists(), \
                'PlaceJob table must be created still.'

            # Loop until exit option is selected.
            while True:
                print('OPTIONS')
                for i, option in enumerate(options):
                    print('{0:2d}) {1:s}'.format(i, option[0]))
                print()
                print("TIPS")
                print('- Enter an option number then hit enter.'
                      "\n- The 'VIEW ...' options do not alter data."
                      '\n- To see menu options again, leave text blank and'
                      ' press enter.')
                print()

                choice = True

                # Loop until choice is empty string.
                while choice:
                    choice = input('jobManager /> ')
                    try:
                        index = int(choice)
                        command = options[index][1]
                        command()
                    except Exception as e:
                        print('{0}. {1}'.format(type(e).__name__, str(e)))
                print()


if __name__ == '__main__':
    main(sys.argv[1:])
