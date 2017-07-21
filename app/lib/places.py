# -*- coding: utf-8 -*-
if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))

import sqlobject.sqlbuilder as builder

from lib import database as db
from lib.setupConf import conf


def countryAndTowns(countryName):
    """
    Retrieve WOEID values for a country and its towns.
    """
    country = db.Country.selectBy(name=countryName).getOne()
    woeidList = [x.woeid for x in country.hasTowns]
    woeidList.append(country.woeid)

    return woeidList


def queuePlaces(include, quiet=True):
    """
    Get the WOEIDs of Places to be queued for retrieving Trend data.
    Includes all countries and a selection of towns based on input.

    @param include: A list of country names for which towns must be looked up. All country level data will be looked up regardless of what is set here.
        e.g. ['South Africa', 'United Kingdom', 'United States']
    @param quiet: Default True. Set to False to print country and town names.
    """
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

    return woeidList


    ## This is an alternative form which may be faster due to doing a single select on towns instead of looking up for each country.
    # filteredTowns = db.Town.select(
    #     builder.IN(db.Town.q.countryID, filteredCountries)
    #     )
    # for x in filteredTowns:
    #     print x.name
    # print filteredTowns.count()


    ## Continent filtering.
    # Get towns, for countries which have been marked as towns are required.
    # continentNames = ('Europe', 'North America')
    # continentsFiltered = db.Continent.select(
    #     builder.IN(db.Continent.q.name, continentNames)
    #     )
    # print continentsFiltered.count()
    # for x in continentsFiltered:
    #     print x.name
    # matchedCountries = db.Country.select(builder.IN(db.Country.q.continentID, continentsFiltered))
    # print matchedCountries.count()
    # for x in matchedCountries:
    #     print x.name, len(x.hasTowns)


# def getConfiguredCountry():
#     countryWoeid = conf.getint('Cron', 'countryWoeid')
#     try:
#         countryObj = db.Place.byWoeid(countryWoeid)
#     except SQLObjectNotFound as e:
#         msg = 'Unable to find country WOEID {0} in the database.'\
#                 .format(countryWoeid)
#         print 'ERROR {0}. {1}'.format(type(e).__name__, msg)
#         raise type(e)(msg)

#     print countryObj

if __name__ == '__main__':
    queuePlaces(['South Africa'], quiet=False)
