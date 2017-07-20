#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SQLite database model in SQLObject.

The db model structure is:
 * Place
    - contains records of all Places
 * Supername -> Continent -> Country -> Town
     - These tables are linked to each other in a hiearchy such that a Supername has Continents, which have Countries, which have Towns.
    - These all inherit from Place.
    - Every record in  one of these tables has a record in Place table
        with the same ID.
 * Trend
    - contains a trend record for a specific time and space. Each record has a foreign key to map it to a Place record, derived from the Trend's WOEID value in the API.

This approach makes it easy to always map a Trend record to the same table (Place) instead of many, while still allowing easy seperation of Place types in the Place-related tables.
    e.g. show all Places
    e.g. show all from Countries table and count of its Towns we have mapped
        to it.
    e.g. show Towns which are in Asia
"""
import sqlobject as so
from sqlobject.inheritance import InheritableSQLObject

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from connection import conn


class Place(InheritableSQLObject):
    """
    A place in the world. This is created from the Yahoo Where On Earth
    locations as returned by Twitter API.

    The inheritance pattern used here means that an item inserted in Town, Country, Continent or Supername will be inserted in Place with the *same* ID, but without duplicating data, such as name.

    This table has childName to indicate which table the object is in and therefore the Place's location type.

    Name is not an alternateID, since place names can be duplicated around the world e.g. Barcelona in Venezuela and Spain.
    Therefore `.byName` is not available, but we can do a `.selectBy` with both town name and the country's ID set in the where clause, to ensure we get one result.

    Default order by ID is omitted as it causes ambiguity issues on some selects. And timestamp is not recognised as a column on the subclasses so cannot be used either.
    """
    _connection = conn

    # WOEID integer value from Yahoo system.
    # Note that `.byWoeid` can be used on Place class, but cannot be used
    # on any subclasses. This is because of the `id` in the order by statement
    # having ambiguous meaning in `where (Place.id = {subclass}.id)`.
    woeid = so.IntCol(alternateID=True)

    # Name of the place.
    name = so.UnicodeCol(default=None)
    # Create an index on name.
    nameIdx = so.DatabaseIndex(name)

    # Date and time when record was created.
    timestamp = so.DateTimeCol(default=so.DateTimeCol.now)
    # Create an index on timestamp.
    timestampIdx = so.DatabaseIndex(timestamp)

    @classmethod
    def getColumnNames(cls):
        """
        Return a list of column names for the class, as strings. This is
        created from a dictionary, so the order is not guaranteed.
        """
        return cls.sqlmeta.column.keys()

    def getData(self, quiet=True):
        """
        Output the current record with key:value pairs for column name
        and value. Note that this is not suitable to converted to JSON
        because of the data types of values.
        """
        data = {col: getattr(self, col) for col in self.getColumnNames()}

        if not quiet:
            for k, v in data.items():
                # Align key to the right.
                print u'{0:>15} : {1}'.format(k, v)


class Supername(Place):
    """
    Global level place, which can have continents. Taken from 'Supername'
    title for the world, in Twitter API.
    """
    _inheritable = False

    # Get Continent objects belong to the Supername. Defaults to null list.
    hasContinents = so.MultipleJoin('Continent')


class Continent(Place):
    """
    A continent, which can have countries.
    """
    _inheritable = False

    # Supername which this Continent belongs to.
    supername = so.ForeignKey('Supername')

    # Get Country objects belonging to the Continent. Defaults to null list.
    hasCountries = so.MultipleJoin('Country')


class Country(Place):
    """
    Place which is a Country in Twitter API.
    """
    _inheritable = False

    # Continent which this Country belongs to.
    continent = so.ForeignKey('Continent', default=None)

    # Get Town objects belonging to the Country. Defaults to null list.
    hasTowns = so.MultipleJoin('Town')

    # Two-character string as the country's code.
    countryCode = so.UnicodeCol(length=2, default=None)


class Town(Place):
    """
    Place which falls into Town or Unknown category in Twitter API.
    """
    _inheritable = False

    # Country which this Town belongs. Optional and defaults to None.
    country = so.ForeignKey("Country", default=None)


class Trend(so.SQLObject):
    """
    A trending topic on Twitter, meaning a lot of Twitter accounts are talking
    about that topic.

    A topic exists at a point in time and maps to a specific place. It's term
    can either be a hashtag (starts with '#' and has no spaces) or a keyword
    phrase (no '#' and can have multiple words).

    Note that the topic is not unique, since the topic can be repeated in
    many locations and it can be repeated in one location across time.

    The topic has a trending volume figure, which is how many tweets there are
    about the topic in the past 24 hours (according to Twitter API docs). 

    Note that the topic volume shown is always global total volume and independent of  the location used to look up the topic. Volume usually ranges from around 10,000 to 1 million and smaller values are returned as null by Twitter API. Adding up trends for a Place taken at the same time each day should give an accurate total of tweets for the period, since there should not be any overlap in tweets across two consecutive 24-hour periods.

    However, it is still useful to count the number of places which a tppic is trending in as an indication of how widespread it is. 
    """
    class sqlmeta:
        # Set sort order by most recent items first.
        defaultOrder = '-timestamp'

    _connection = conn

    # The topic which is trending.
    topic = so.UnicodeCol(length=64)
    # Create the index to make searches faster.
    topicIdx = so.DatabaseIndex(topic)

    # Whether the topic is a hashtag i.e. starts with '#'.
    hashtag = so.BoolCol(default=False)

    # Number of global tweets about topic in past 24 hours. Can be set to null but is not set by default.
    volume = so.IntCol(notNull=False)

    # The place associated with this trend record. See `setPlace` for why this is an optional field.
    place = so.ForeignKey("Place", notNull=False, default=None)

    # Date and time when record was created.
    timestamp = so.DateTimeCol(default=so.DateTimeCol.now)
    # Create an index on timestamp.
    timestampIdx = so.DatabaseIndex(timestamp)

    def setPlace(self, woeid):
        """
        Links an existing Trend record to an existing Place record, given
        a Place WOEID.

        Expects a WOEID int, gets ID for the Place, then stores it as the
        foreign key for the Trend.

        This doesn't work to be placed in __init__ since then its called
        on a select and doen't work for modelCreate because the input kwargs
        are validated before the method is called.

        @param woeid: integer value for WOEID of the Place to link to.

        @return self: returns object instance.
        """
        assert isinstance(woeid, int), 'Expected WOEID as an `int`, but '\
            'got type `{0}`.'.format(type(woeid).__name__)
        try:
            self.placeID = Place.byWoeid(woeid).id
        except SQLObjectNotFound as e:
            raise type(e)('Place with WOEID {0} could not be found in the db.'\
                          .format(woeid))

        return self

    def _set_topic(self, value):
        """
        Override the topic setting method, so that hashtag boolean is updated
        automatically whenever topic is set.

        @param value: string value to set as the topic.
        """
        self._SO_set_topic(value)
        if value.startswith('#'):
            self._SO_set_hashtag(True)
        else:
            self._SO_set_hashtag(False)

    @classmethod
    def getColumnNames(cls):
        """
        Return a list of column names for the class, as strings. This is
        created from a dictionary, so the order is not guaranteed.
        """
        return cls.sqlmeta.columns.keys()

    def getData(self, quiet=True):
        """
        Output the current record with key:value pairs for column name
        and value. Note that this is not suitable to converted to JSON
        because of the data types of values.
        """
        data = {col: getattr(self, col) for col in self.getColumnNames()}
        
        if not quiet:
            for k, v in data.items():
                # Align key to the right.
                print u'{0:>15} : {1}'.format(k, v)
