# -*- coding: utf-8 -*-
"""
SQL database tables relating to places.
"""
# Names of tables to be included in the db. The order for when they are created
# matters.
__all__ = ['Place', 'Supername', 'Continent', 'Country', 'Town']

import sqlobject as so
from sqlobject.inheritance import InheritableSQLObject

from connection import conn


class Place(InheritableSQLObject):
    """
    A place in the world. This is created from the Yahoo Where On Earth
    locations as returned by Twitter API.

    The inheritance pattern used here means that an item inserted in
    Town, Country, Continent or Supername will be inserted in Place with
    the *same* ID, but without duplicating data, such as name.

    This table has childName to indicate which table the object is in and
    therefore the Place's location type.

    Name is not an alternateID, since place names can be duplicated around
    the world e.g. Barcelona in Venezuela and Spain.
    Therefore `.byName` is not available, but we can do a `.selectBy` with
    both town name and the country's ID set in the where clause, to ensure
    we get one result.

    Default order by ID is omitted as it causes ambiguity issues on some
    selects. And timestamp is not recognised as a column on the subclasses
    so cannot be used either.
    """
    _connection = conn

    # WOEID integer value from Yahoo system.
    # Note that `.byWoeid` can be used on Place class, but cannot be used
    # on any subclasses. This is because of the `id` in the order by statement
    # having ambiguous meaning in `where (Place.id = {subclass}.id)`.
    woeid = so.IntCol(alternateID=True)

    # Name of the place.
    name = so.UnicodeCol(length=64, default=None)
    # Create an index on name.
    nameIdx = so.DatabaseIndex(name)

    # Date and time when record was created.
    timestamp = so.DateTimeCol(default=so.DateTimeCol.now)
    # Create an index on timestamp.
    timestampIdx = so.DatabaseIndex(timestamp)

    # Get all the trend records relating to this Place.
    hasTrends = so.MultipleJoin('Trend')

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
        and value. Note that this is not suitable to be converted to JSON
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
    # Create the index on country foreign key.
    countryIdx = so.DatabaseIndex(country)
