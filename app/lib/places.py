# -*- coding: utf-8 -*-
"""
Get Place data from the database.

Usage:
    $ python -m lib.places --help
"""
import sys

import sqlobject.sqlbuilder as builder
from sqlobject import SQLObjectNotFound

from lib import database as db
from lib.config import AppConf


appConf = AppConf()


def countryAndTowns(countryName):
    """
    Retrieve WOEID values for a country and its towns.
    """
    try:
        country = db.Country.selectBy(name=countryName).getOne()
    except SQLObjectNotFound as e:
        raise type(e)("Country `{}` could not be found in the database."
                      .format(countryName))

    woeidList = [x.woeid for x in country.hasTowns]
    woeidList.append(country.woeid)

    return woeidList


def allCountriesSomeTowns(include, quiet=True):
    """
    Get the WOEIDs of Places to be queued for retrieving Trend data.
    Includes all countries and a selection of towns based on input.

    @param include: A list of country names for which towns must be looked up.
    All country level data will be looked up regardless of what is set here.
        e.g. ['South Africa', 'United Kingdom', 'United States']
    @param quiet: Default True. Set to False to print country and town names.
    """
    assert isinstance(include, list), ("Expected `include` as type `list`"
                                       "but got type `{}`.".format(
                                           type(include).__name__)
                                       )
    # Get all countries.
    woeidList = [c.woeid for c in db.Country.select()]

    # Lookup towns belonging to a set of countries.
    filteredCountries = db.Country.select(
        builder.IN(db.Country.q.name, include)
    )
    for x in filteredCountries:
        townWoeids = [y.woeid for y in x.hasTowns]
        woeidList.extend(townWoeids)
        if not quiet:
            print x.name
            townNames = [y.name for y in x.hasTowns]
            print townNames
            print


def allCountriesAndTowns():
    """
    Return list of WOEID values for all towns and countries in the db.
    """
    countryWoeids = [c.woeid for c in db.Country.select()]
    townWoeids = [t.woeid for t in db.Town.select()]
    woeidList = countryWoeids + townWoeids

    return woeidList

'''
def getConfiguredCountryWoeid():
    """
    Return a country object for the WOEID specified in configuration.
    Raises an error if not found in db.
    """
    countryWoeid = conf.getint('Cron', 'countryWoeid')
    try:
        countryObj = db.Place.byWoeid(countryWoeid)
    except so.SQLObjectNotFound as e:
        msg = 'Unable to find country WOEID {0} in the database.'\
                .format(countryWoeid)
        print 'ERROR {0}. {1}'.format(type(e).__name__, msg)
        raise type(e)(msg)

    return countryObj


def someTowns():
    """
    This is a related form of allCountriesSomeTowns which may be faster due
    to doing a single select on towns instead of looking up for each country.
    """
    filteredCountries = db.Country.select(
        builder.IN(db.Country.q.name, include)
        )
    filteredTowns = db.Town.select(
        builder.IN(db.Town.q.countryID, filteredCountries)
        )
    for x in filteredTowns:
        print x.name

    return woeidList


def continentFiltering():
    # Get towns, for countries which have been marked as towns are required.
    continentNames = ('Europe', 'North America')
    continentsFiltered = db.Continent.select(
        builder.IN(db.Continent.q.name, continentNames)
        )
    print continentsFiltered.count()
    for x in continentsFiltered:
        print x.name
    matchedCountries = db.Country.select(builder.IN(db.Country.q.continentID,
        continentsFiltered))
    print matchedCountries.count()
    for x in matchedCountries:
        print x.name, len(x.hasTowns)
'''

def main(args):
    # TODO: allow input of multiple names with comma separators, as
    # with streaming input.

    if not args or '-h' in args or '--help' in args:
        helpMsg = ('Usage: python -m lib.places [countryName] \n'
                   'Options and arguments: \n'
                   '  [countryName]: Set as `default` to get configured '
                   'default, otherwise set as country\'s name to look up '
                   'country and town objects for.')
        print helpMsg
    else:
        countryOption = args[0].strip()
        if countryOption != 'default':
            include = appConf.get('TrendCron', 'countryName')
        else:
            include = countryOption
        allCountriesSomeTowns([include], quiet=False)


if __name__ == '__main__':
    main(sys.argv[1:])
