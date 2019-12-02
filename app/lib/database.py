# -*- coding: utf-8 -*-
"""
Database initialisation and storage handling module.

See docs for how to set up the database.

Logging messages to a log file is not needed here as this is run directly
as a command-line script. The detailed creation of places might be good to
move to a log file with only summary level data printed to the console.
"""
from __future__ import absolute_import
from __future__ import print_function
import os

from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError

import models
from etc import base_data
from lib import locations
from lib.config import AppConf

# Make model objects available on the database module.
from models import (
    Supername,
    Continent,
    Country,
    Town,
    Category,
    Campaign,
)
from models.connection import conn
import six


conf = AppConf()


def _getModelClasses():
    return [getattr(models, tableName) for tableName in models.__all__]


def _dropTables(verbose=True):
    """
    Drop all tables.
    """
    modelsList = _getModelClasses()

    if verbose:
        print('Dropping tables...')
    for m in modelsList:
        if verbose:
            print("-> Dropping {0}".format(m.__name__))
        m.dropTable(ifExists=True, cascade=True)

    return None


def _createTables(verbose=True):
    """
    Create all tables which do not already exist.
    """
    modelsList = _getModelClasses()

    if verbose:
        print('Creating tables...')
    for m in modelsList:
        if verbose:
            print("-> Creating {0}".format(m.__name__))
        m.createTable(ifNotExists=True)

    return None


def addWorldAndContinents():
    """
    Insert default data into the database. This should be called when the
    database is initialized.
    """
    # Create the world as a Place.
    woeid = 1
    name = 'Worldwide'
    try:
        world = Supername(
            woeid=woeid,
            name=name
        )
        print(u"Created - Supername: `{}`.".format(name))
    except DuplicateEntryError:
        world = Supername.byWoeid(1)
        print(u"Exists - Supername: `{}`.".format(name))

    # Create the continents as Places, with the world as the parent.
    for woeid, name in base_data.continentBase.items():
        try:
            Continent(
                woeid=woeid,
                name=name,
                supernameID=world.id
            )
            print(u"Created - Continent: `{}`.".format(name))
        except DuplicateEntryError:
            print(u"Exists - Continent: `{}`.".format(name))


def addTownsAndCountries(maxTowns=None):
    """
    Add Town and Country level data extracted from Twitter API to the database.

    The function in locations will get the sample location file provided
    with the repo but can also reference a custom JSON.

    :param maxTowns: In development, set this optionally to an integer
        as maximum number of towns to insert into db. The total is
        usually around 400.

    :return: None
    """
    # Load from JSON file of Twitter locations. This is a generator so
    # we don't store it otherwise the 2nd time we iterate it is finished.
    for loc in locations.getJSON():
        if loc['placeType']['name'].lower() == 'country':
            woeid = loc['woeid']
            name = loc['name']
            countryCode = loc['countryCode']
            try:
                Country(
                    woeid=woeid,
                    name=name,
                    countryCode=countryCode
                )
                print(u"Country - created: {}.".format(name))
            except DuplicateEntryError:
                print(u"Country - exists: {}.".format(name))

    townCount = 0
    for loc in locations.getJSON():
        if maxTowns is not None and townCount == maxTowns:
            break
        # Increment on both new and existing town.
        townCount += 1

        if loc['placeType']['name'].lower() == 'town':
            try:
                parentCountryID = Country.byWoeid(loc['parentid']).id
            except SQLObjectNotFound as e:
                parentCountryID = None
                msg = "Unable to find parent country in DB with WOEID {woeid}"\
                    " for town {name}.".format(
                        woeid=loc['parentid'],
                        name=loc['name']
                    )
                print("ERROR {type}. {msg}".format(
                    type=type(e).__name__,
                    msg=msg
                ))

            woeid = loc['woeid']
            name = loc['name']
            try:
                Town(
                    woeid=woeid,
                    name=name,
                    countryID=parentCountryID
                )
                print(u"Town - created: {}.".format(name))
            except DuplicateEntryError:
                print(u"Town - exists: {}.".format(name))


def mapCountriesToContinents():
    """
    Iterate through the countries in the database and ensure they have a
    parent continent set.

    :return: None
    """
    for c in Country.select():
        # If Continent is not already set for the Country, then iterate
        # through our mapping to find the appropriate Continent name.
        if not c.continent:
            for continent, countries in six.iteritems(base_data.continentMapping):
                # Check if the country name in the DB falls in the countries
                # list we have mapped to the current continent.
                if c.name in countries:
                    # We have found the right continent.
                    break
            else:
                raise ValueError("Continent could not be found for country: {}"
                                 .format(c))
            # Lookup Continent object. Returns as None if no match.
            # Use order by to avoid ambiguity error on id.
            continentResults = Continent.selectBy(name=continent)\
                .orderBy('place.id')
            if continentResults:
                # Update the country object with the continent we found.
                continentRecord = continentResults.getOne()
                c.continentID = continentRecord.id
                print("Link - created: {continent:15} <-- {country:15}".format(
                    continent=continentRecord.name,
                    country=c.name
                ))
        else:
            print("Link - exists: {continent:15} <-- {country:15}".format(
                continent=c.continent.name,
                country=c.name
            ))


def addLocationData(maxTowns=None):
    """
    Add location data and associations to database. Using preset data and
    also JSON extracted from Twitter API.

    Any existing data is skipped and is not overwritten and should not raise
    errors. In development and testing, set maxTowns to a low integer to save
    time rather than adding about 400 towns to the db.

    TODO: Improve these with bulk insert statements, using Python to build
    the insert statements or SQLite. This takes too long to do on setting
    up the application.

    :return: None
    """
    addWorldAndContinents()
    addTownsAndCountries(maxTowns)
    mapCountriesToContinents()


def _checkDBexists():
    dbPath = conf.get('SQL', 'dbPath')
    status = os.path.exists(dbPath)
    print(dbPath)
    print("DB file exists." if status else "DB file not created yet.")
    print()

    return status


def _baseLabels():
    print('Inserting all base labels...')
    categoryKeys = ('fetchProfiles', 'influencers', 'search',
                    'lookupTweets')
    campaignKeys = ('fetchTweets', 'search', 'lookupTweets')

    for key in categoryKeys:
        label = conf.get('Labels', key)
        try:
            categoryRec = Category(name=label)
            print("Created category: {0}".format(categoryRec.name))
        except DuplicateEntryError:
            print("Skipped category: {0}".format(label))

    for key in campaignKeys:
        label = conf.get('Labels', key)
        try:
            campaignRec = Campaign(name=label, searchQuery=None)
            print("Created campaign: {0}".format(campaignRec.name))
        except DuplicateEntryError:
            print("Skipped campaign: {0}".format(label))


def _populate(maxTowns=None):
    # TODO Make this and the internal calls not verbose for tests.

    print('Adding default data...')
    if isinstance(maxTowns, int):
        addLocationData(maxTowns)
    else:
        addLocationData()
    print('-> Added fixtures data.\n')

    return maxTowns
