# -*- coding: utf-8 -*-
"""
Database initialisation and storage handling module.

See README.md for setting up the database.
"""
#import cherrypy # to be used for logging
from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import conf
# Make tables available for iteration.
import models
# Make tables available as `db.tableName`.
from models import *
# Make connection available as `db.conn`.
from models.connection import conn
from etc.baseData import continentBase, continentMapping


def initialise(dropAll=False, createAll=True):
    """
    Initialise the database. By default, all tables are created and none are dropped.

    @param dropAll: default False. If set to True, drop all tables before creating them.
    @param createAll: default True. Iterate through table names and create the tables which they do not exist yet.
    """
    msg = """Initialising database.
    * dropAll: {0}
    * createAll: {1}
    * location: {2}""".format(dropAll, createAll, conf.get('SQL', 'dbName'))
    print msg

    modelsList = []

    # Get classes from names.
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        modelsList.append(tableClass)

    # Drop tables.
    if dropAll:
        for m in modelsList:
            #cherrypy.log("Dropping %s" % m.__name__, 'DATABASE.INIT')
            m.dropTable(ifExists=True, cascade=True)

    # Create tables.
    if createAll:
        for m in modelsList:
            #cherrypy.log("Creating %s" % m.__name__, 'DATABASE.INIT')
            m.createTable(ifNotExists=True)


def addWorldAndContinents():
    """
    Insert default data into the database. This should be called when the
    database is initialised.
    """
    # Create the world as a Place.
    woeid = 1
    name = 'Worldwide'
    try:
        world = Supername(woeid=woeid, name=name)
        print u'Created - Supername: `{}`.'.format(name)
    except DuplicateEntryError as e:
        # Use `Place` to avoid id ambiguity in sql statement.
        world = Place.byWoeid(1)
        print u'Exists - Supername: `{}`.'.format(name)

    # Create the continents as Places, with the world as the parent.
    for woeid, name in continentBase.items():
        try:
            c = Continent(woeid=woeid, name=name, supernameID=world.id)
            print u'Created - Continent: `{}`.'.format(name)
        except DuplicateEntryError as e:
            print u'Exists - Continent: `{}`.'.format(name)


def addTownsAndCountries(maxTowns=None):
    """
    Add Town and Country level data extracted from Twitter API to the database.

    The readLocations function will get the sample location file provided with the repo but can also reference a custom JSON.

    @parma maxTowns: In development, set this optionally to an integer
        as maximum number of towns to insert into db. The total is
        usually around 400.
    """
    # Load a JSON file of Twitter locations. The import is inside this
    # function, so that it is called we always load the latest file and
    # clear it when the function has completed.
    from lib.locations import readLocations

    for loc in readLocations():
        if loc['placeType']['name'].lower() == 'country':
            woeid = loc['woeid']
            name = loc['name']
            countryCode = loc['countryCode']
            try:
                c = Country(woeid=woeid, name=name, countryCode=countryCode)
                print u'Country - created: {}.'.format(name)
            except DuplicateEntryError as e:
                print u'Country - exists: {}.'.format(name)

    townCount = 0
    for loc in readLocations():
        if loc['placeType']['name'].lower() == 'town':
            try:
                # Use Place class to avoid ambiguity on id on order by.
                parentCountryID = Place.byWoeid(loc['parentid']).id
            except SQLObjectNotFound as e:
                parentCountryID = None
                msg = 'Unable to find parent country in DB with WOEID {0} '\
                      'for town {1}.'.format(loc['parentid'], loc['name'])
                print 'ERROR {0}. {1}'.format(type(e).__name__, msg)

            woeid = loc['woeid']
            name = loc['name']
            try:
                t = Town(woeid=woeid, name=name, countryID=parentCountryID)
                print u'Town - created: {}.'.format(name)
            except DuplicateEntryError as e:
                print u'Town - exists: {}.'.format(name)

            # Increment on other new or existing town.
            townCount += 1
            if maxTowns and townCount == maxTowns:
                break


def mapCountriesToContinents():
    """
    Iterate through the countries in the database and ensure they have a
    parent continent set.
    """
    for c in Country.select():
        # If Continent is not already set for the Country, then iterate
        # through our mapping to find the appropriate Continent name.
        if not c.continent:
            for continent, countries in continentMapping.iteritems():
                # Check if the country name in the db falls in the countries
                # list we have mapped to the current continent.
                if c.name in countries:
                    # We have found the right continent.
                    break
            # Lookup Continent object. Returns as None if no match.
            # Use order by to avoid ambiguity error on id.
            continentResults = Continent.selectBy(name=continent)\
                                   .orderBy('place.id')
            if continentResults:
                # Update the country object with the continent we found.
                continentRecord = continentResults.getOne()
                c.continentID = continentRecord.id
                print 'Link - created: {0:15} <= {1:15}'.format(continentRecord.name,
                                                         c.name)
        else:
            print 'Link - exists: {0:15} <= {1:15}'.format(c.continent.name,
                                                          c.name)

def addLocationData(maxTowns=None):
    """
    Add location data and associations to database. Using preset data and also JSON extracted from Twitter API.

    In development and testing, set maxTowns to a low integer to save time adding 400 towns to the db.

    Any existing data is skipped and is not overwritten and should not raise errors.
    """
    addWorldAndContinents()
    addTownsAndCountries(maxTowns)
    mapCountriesToContinents()


def resetAll(maxTowns=None):
    """
    Drop all tables from database if they exist and then create all tables, then add all location data.

    In development and testing, set maxTowns to a low integer to save time adding 400 towns to the db.
    """
    initialise(dropAll=True)
    addLocationData(maxTowns)


def main(args):
    """
    Run functions using command-line arguments.
    """
    if len(args) == 0 or '-h' in args or '--help' in args:
        print 'Usage:'
        print '  # Show options.'
        print '  $ python {} --help'.format(__file__)
        print
        print '  # Create tables and do not add data.'
        print '  $ python {} --initialise'.format(__file__)
        print
        print '  # Create tables and then populate with default location data,'
        print '  # up to optional limit.'
        print '  $ python {} --reset [maxTowns]'.format(__file__)
    else:
        if args[0] in ['-i', '--initialise']:
            initialise()
        elif args[0] in ['-r', '--reset']:
            maxTowns = int(args[1]) if len(args) >= 2 else None
            resetAll(maxTowns)


if __name__ == '__main__':
    main(sys.argv[1:])
