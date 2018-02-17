# -*- coding: utf-8 -*-
"""
Database initialisation and storage handling module.

See docs for setting up the database.

Usage:
    $ python -m lib.database [args]
"""
import os
import sys

from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError

import models
from lib import locations
from lib.config import AppConf
from lib.query.schema import tableCounts
from etc.baseData import continentBase, continentMapping

# Make model objects available on the database module.
from models import *
from models.connection import conn


conf = AppConf()


def initialise(dropAll=False, createAll=True):
    """
    Initialise the tables in the database.

    By default, no tables are dropped and all tables are created (or skipped).

    @param dropAll: default False. If set to True, drop all tables before
        creating them.
    @param createAll: default True. Iterate through table names and create
        the tables which they do not exist yet.

    @return: count of table models in the available list.
    """
    modelsList = []

    # Get classes from names.
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        modelsList.append(tableClass)

    # Drop tables.
    if dropAll:
        for m in modelsList:
            # TODO: Add cherrypy logging.
            # cherrypy.log("Dropping %s" % m.__name__, 'DATABASE.INIT')
            m.dropTable(ifExists=True, cascade=True)

    # Create tables.
    if createAll:
        for m in modelsList:
            # TODO: Add cherrypy logging.
            # cherrypy.log("Creating %s" % m.__name__, 'DATABASE.INIT')
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
        world = Supername(woeid=woeid, name=name)
        print u'Created - Supername: `{}`.'.format(name)
    except DuplicateEntryError:
        world = Supername.byWoeid(1)
        print u'Exists - Supername: `{}`.'.format(name)

    # Create the continents as Places, with the world as the parent.
    for woeid, name in continentBase.items():
        try:
            Continent(woeid=woeid, name=name, supernameID=world.id)
            print u'Created - Continent: `{}`.'.format(name)
        except DuplicateEntryError:
            print u'Exists - Continent: `{}`.'.format(name)


def addTownsAndCountries(maxTowns=None):
    """
    Add Town and Country level data extracted from Twitter API to the database.

    The function in locations will get the sample location file provided
    with the repo but can also reference a custom JSON.

    @parma maxTowns: In development, set this optionally to an integer
        as maximum number of towns to insert into db. The total is
        usually around 400.
    """
    # Load from JSON file of Twitter locations. This is a generator so
    # we don't store it otherwise the 2nd time we iterate it is finished.
    for loc in locations.getJSON():
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
    for loc in locations.getJSON():
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
                Town(woeid=woeid, name=name, countryID=parentCountryID)
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
                print 'Link - created: {0:15} <= {1:15}'.format(
                    continentRecord.name, c.name)
        else:
            print 'Link - exists: {0:15} <= {1:15}'.format(
                c.continent.name, c.name)


def addLocationData(maxTowns=None):
    """
    Add location data and associations to database. Using preset data and
    also JSON extracted from Twitter API.

    In development and testing, set maxTowns to a low integer to save time
    adding 400 towns to the db.

    Any existing data is skipped and is not overwritten and should not raise
    errors.
    """
    addWorldAndContinents()
    addTownsAndCountries(maxTowns)
    mapCountriesToContinents()


def main(args):
    """
    Run functions using command-line arguments.
    """
    if len(args) == 0 or set(args) & set(('-h', '--help')):
        helpMsg = """\
Usage:
$ python -m lib.database [-p|--path] [-s|--summary] [-d|--drop] [-c|--create]
                         [-P|--populate] [-h|--help]

Options and arguments:
--help        : Show help.
--path        : Show path to configured db file.
--summary     : Show summary of tables and records in db.
--drop        : Drop all tables.
--create      : Create all tables in models, but do not drop or alter existing
                tables or modify their data. Then insert base Campaigns and
                category labels (see config file), so they can be assigned as
                labelling process within utilities. Even the Campaign or
                Category tables existed already, base records are still
                inserted. If a base record exists then it's creation is
                skipped.
--populate [N]: Populate tables with default location data and relationships.
                If used without the other flags, accepts an integer of maxTowns
                to be set for debug purposes and applies it.

Note:
  Flags can be combined.
  e.g. $ python -m lib.database -p -d -c -P -s
  Actions will always be performed with the following priority from
  first to last: drop -> create -> populate.
        """
        print helpMsg
    else:
        if set(args) & set(('-p', '--path')):
            dbPath = conf.get('SQL', 'dbPath')
            status = os.path.exists(dbPath)
            print dbPath
            print "Exists." if status else "Not created yet."
            print
        if set(args) & set(('-d', '--drop')):
            confirm = raw_input('Are you sure you want to drop all tables?'
                                ' [Y/N] /> ')
            if confirm.strip().lower() in ('y', 'yes'):
                print 'Dropping tables...'
                d = initialise(dropAll=True, createAll=False)
                print '-> {0} tables were dropped.\n'.format(d)
            else:
                print 'Cancelled dropping tables. Exiting.'
                sys.exit(0)
        if set(args) & set(('-c', '--create')):
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
                    print "Created campaign: {0}".format(categoryRec.name)
                except DuplicateEntryError:
                    print "Skipped campaign: {0}".format(label)
        if set(args) & set(('-P', '--populate')):
            print 'Adding default data...'
            if len(args) == 2 and args[1].isdigit():
                addLocationData(int(args[1]))
            else:
                addLocationData()
            print '-> Added default data.\n'
        if set(args) & set(('-s', '--summary')):
            print 'Getting table summary...'
            tableCounts.showTableCounts()


if __name__ == '__main__':
    main(sys.argv[1:])
