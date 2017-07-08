# -*- coding: utf-8 -*-
"""
Database initialisation and storage handling module.

Usage (from app dir):
    # First time, run script as main file to do setup.
    # Set values in config to reset tables and base data if necessary.
    1. $ python -m lib.database
    OR $ python lib/database.py

    # Get data from db schema that is already create and has tables.
    1. $ python
    2. >>> from lib import database as db
    3. >>> for x in list(Country.select()[:10]):
       ...     print x
       >>>
"""
import os
import sys

#import cherrypy # to be used for logging
from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    sys.path.insert(0, os.path.abspath('.'))

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
    msg = 'Initialising database with dropAll={0} and createAll={1}.'.format(dropAll, createAll)
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
        print 'Created - Supername: `{}`.'.format(name)
    except DuplicateEntryError as e:
        world = Supername.byWoeid(1)
        print 'Exists - Supername: `{}`.'.format(name)

    # Create the continents as Places, with the world as a parent.
    for woeid, name in continentBase.items():
        try:
            c = Continent(woeid=woeid, name=name, supernameID=world.id)
            print 'Created - Continent: `{}`.'.format(name)
        except DuplicateEntryError as e:
            print 'Exists - Continent: `{}`.'.format(name)


def addTownsAndCountries(maxTowns=None):
    """
    Add Town and Country level data extracted from Twitter API to the database.

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
            try:
                c = Country(woeid=woeid, name=name)
                print 'Created - Country: `{}`.'.format(name)
            except DuplicateEntryError as e:
                print 'Exists - Country: `{}`.'.format(name)

    townCount = 0
    for loc in readLocations():
        if loc['placeType']['name'].lower() == 'town':
            try:
                parentCountryID = Country.byWoeid(loc['parentid']).id
            except SQLObjectNotFound as e:
                parentCountryID = None
                msg = 'Unable to find parent country in DB with WOEID {0} '\
                      'for town {1}.'.format(loc['parentid'], loc['name'])
                print 'ERROR {0}. {1}'.format(type(e).__name__, msg)

            woeid = loc['woeid']
            name = loc['name']
            try:
                t = Town(woeid=woeid, name=name, countryID=parentCountryID)
                print 'Created - Town: `{}`.'.format(name)
            except DuplicateEntryError as e:
                print 'Exists - Town: `{}`.'.format(name)
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
            continentResults = Continent.selectBy(name=continent)
            if continentResults:
                # Update the country object with the continent we found.
                continentRecord = continentResults.getOne()
                c.continentID = continentRecord.id
                print 'Mapped - {0:15} <= {1:15}'.format(continentRecord.name,
                                                         c.name)

def addLocationData(maxTowns=None):
    """
    Add location data and associations to database, using preset data and Jalso SON from Twitter API (using custom  JSON if available otherwise using sample JSON).

    In development and testing, set maxTowns to a low integer to save time adding 400 towns to the db.
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
