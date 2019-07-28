# -*- coding: utf-8 -*-
"""
Database initialisation and storage handling module.

See docs for how to set up the database.

Logging messages to a log file is not needed here as this is run directly
as a command-line script. The detailed creation of places might be good to
move to a log file with only summary level data printed to the console.

Usage:
    $ python -m lib.database --help

TODO: Move the command-line aspects to utils directory script.
"""
import os
import sys

from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError

import models
from etc import base_data
from lib import locations
from lib.config import AppConf
from lib.db_query.schema import table_counts

# Make model objects available on the database module.
from models import *
from models.connection import conn


conf = AppConf()


def initialise(dropAll=False, createAll=True):
    """
    Initialise the tables in the database.

    By default, no tables are dropped and all tables are created (or skipped).

    :param dropAll: default False. If set to True, drop all tables before
        creating them.
    :param createAll: default True. Iterate through table names and create
        the tables which they do not exist yet.

    :return: count of table models in the available list.
    """
    modelsList = []

    # Get class objects using the imported list of names.
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        modelsList.append(tableClass)

    # Optionally drop all tables.
    if dropAll:
        for m in modelsList:
            print "Dropping {0}".format(m.__name__)
            m.dropTable(ifExists=True, cascade=True)

    # Optionally create all tables.
    if createAll:
        for m in modelsList:
            print "Creating {0}".format(m.__name__)
            m.createTable(ifNotExists=True)

    return len(modelsList)


def addWorldAndContinents():
    """
    Insert default data into the database. This should be called when the
    database is initialised.
    """
    # Create the world as a Place.
    woeid = 1
    name = 'Worldwide'
    try:
        world = Supername(
            woeid=woeid,
            name=name
        )
        print u"Created - Supername: `{}`.".format(name)
    except DuplicateEntryError:
        world = Supername.byWoeid(1)
        print u"Exists - Supername: `{}`.".format(name)

    # Create the continents as Places, with the world as the parent.
    for woeid, name in base_data.continentBase.items():
        try:
            Continent(
                woeid=woeid,
                name=name,
                supernameID=world.id
            )
            print u"Created - Continent: `{}`.".format(name)
        except DuplicateEntryError:
            print u"Exists - Continent: `{}`.".format(name)


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
                print u"Country - created: {}.".format(name)
            except DuplicateEntryError:
                print u"Country - exists: {}.".format(name)

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
                print "ERROR {type}. {msg}".format(
                        type=type(e).__name__,
                        msg=msg
                    )

            woeid = loc['woeid']
            name = loc['name']
            try:
                Town(
                    woeid=woeid,
                    name=name,
                    countryID=parentCountryID
                )
                print u"Town - created: {}.".format(name)
            except DuplicateEntryError:
                print u"Town - exists: {}.".format(name)


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
            for continent, countries in base_data.continentMapping.iteritems():
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
                print "Link - created: {continent:15} <-- {country:15}".format(
                    continent=continentRecord.name,
                    country=c.name
                )
        else:
            print "Link - exists: {continent:15} <-- {country:15}".format(
                continent=c.continent.name,
                country=c.name
            )


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


def main(args):
    """
    Run functions using command-line arguments.
    """
    if len(args) == 0 or set(args) & {'-h', '--help'}:
        helpMsg = """\
Usage:
$ python -m lib.database [-p] [-s] [-d] [-c] [-P] [-h]

Options and arguments:
-h --help    : Show help and exit.
-p --path    : Show path to configured db file.
-s --summary : Show summary of tables and records in db.
-d --drop    : Drop all tables.
-c --create  : Create all tables in models, but do not drop or alter 
               existing tables or modify their data. Then insert base data 
               for Campaign and Category labels (see config file), so they 
               can be assigned as labelling process within utilities. 
               Even the Campaign or Category tables existed already, base 
               records are still inserted. If a base record exists then its 
               creation is skipped.
-P --populate: Populate tables with default location data and relationships.
               ONLY if used without other flags, accepts an optional
               integer as max number of towns to create from fixtures data.
               This is useful during development to save time, if only a few
               or no towns are needed.
                
Note:
  Flags can be combined.
  e.g. $ python -m lib.database -p -d -c -P -s
  Actions will always be performed with the following priority from
  first to last: drop -> create -> populate.
        """
        print helpMsg
    else:
        if set(args) & {'-p', '--path'}:
            dbPath = conf.get('SQL', 'dbPath')
            status = os.path.exists(dbPath)
            print dbPath
            print "Exists." if status else "Not created yet."
            print
        if set(args) & {'-d', '--drop'}:
            confirm = raw_input('Are you sure you want to drop all tables?'
                                ' [Y/N] /> ')
            if confirm.strip().lower() in ('y', 'yes'):
                print 'Dropping tables...'
                d = initialise(dropAll=True, createAll=False)
                print '-> {0} tables were dropped.\n'.format(d)
            else:
                print 'Cancelled dropping tables. Exiting.'
                sys.exit(0)
        if set(args) & {'-c', '--create'}:
            print 'Creating tables...'
            c = initialise(dropAll=False, createAll=True)
            print '-> Count of tables is now {}.\n'.format(c)

            print 'Inserting all base labels...'
            categoryKeys = ('fetchProfiles', 'influencers', 'search',
                            'lookupTweets')
            campaignKeys = ('fetchTweets', 'search', 'lookupTweets')

            for key in categoryKeys:
                label = conf.get('Labels', key)
                try:
                    categoryRec = Category(name=label)
                    print "Created category: {0}".format(categoryRec.name)
                except DuplicateEntryError:
                    print "Skipped category: {0}".format(label)
            for key in campaignKeys:
                label = conf.get('Labels', key)
                try:
                    campaignRec = Campaign(name=label, searchQuery=None)
                    print "Created campaign: {0}".format(campaignRec.name)
                except DuplicateEntryError:
                    print "Skipped campaign: {0}".format(label)
        if set(args) & {'-P', '--populate'}:
            print 'Adding default data...'
            if len(args) == 2 and args[1].isdigit():
                addLocationData(int(args[1]))
            else:
                addLocationData()
            print '-> Added fixtures data.\n'
        if set(args) & {'-s', '--summary'}:
            print 'Getting table summary...'
            table_counts.showTableCounts()


if __name__ == '__main__':
    main(sys.argv[1:])
