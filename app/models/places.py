"""
Places model application file.

SQL database tables relating to places.

The inheritance pattern is based on SQLObject documentation. An important
result of this is that a record created in a child table (Supername, Continent,
Country or Town) will automatically be created in the parent table Place,
with the *identical* record ID. This is a major benefit for this project, since
the Trend table only has to reference the ID in Place table as it's foreign
key, instead of checking which type of Place it is referencing.
At the same time, a place record is treated appropriately as Supername,
Continent, Country or Town. This allows powerful filtering, such as selecting
trends only at the Country level or getting trends for all Towns in
a certain Continent.

The reasoning for and the implementation of this pattern is as follows:
- All places share base attributes. These are set centrally as columns
  in the Place table, to avoid repetition across child tables.
- Every value in a child table has a corresponding row in the Place table
  with the same ID, such that a complete record can be retrieved using select
  from both tables where the ID the same. (A value in Place does not actually
  need a child value, but that will not be useful. Also, a harmless side
  effect of this that the IDs in the child tables are not necessarily
  continuous in the way they autoincrement.)
- Instead of using a foreign key column to link a Place to another Place,
  there is a foreign key link from a record child table to a record
  in a different kind of child table. Such that a Supername (world) has
  Continents, which have Countries, which have Towns.
- No data in the child table should be duplicated from the Place table,
  such that a child table may function with simply a ID column and foreign key
  column. The value of Place.child_name further assists with this link
  and is used when doing SELECT queries. Additional columns or helper
  JOIN methods in the ORM can be added as details of child table
  as necessary.

TODO: Compare this docstring with models.md document and simplify.
"""
# Names of tables to be included in the db. The order for when they are created
# matters.
__all__ = ["Place", "Supername", "Continent", "Country", "Town"]

import sqlobject as so
from sqlobject.inheritance import InheritableSQLObject

from .connection import conn


class Place(InheritableSQLObject):
    """
    A place in the world. This is created from the Yahoo Where On Earth
    locations as returned by Twitter API.

    This table has childName to indicate which table the object is in and
    therefore the parent Place's location type.

    Name is *not* an alternateID, since place names can be duplicated around
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
    name = so.StringCol(length=64, default=None)
    nameIdx = so.DatabaseIndex(name)

    # Date and time when record was created.
    timestamp = so.DateTimeCol(default=so.DateTimeCol.now)
    timestampIdx = so.DatabaseIndex(timestamp)

    # Get all the trend records relating to this Place.
    hasTrends = so.MultipleJoin("Trend")

    @classmethod
    def getColumnNames(cls):
        """
        Return a list of column names for the class, as strings. This is
        created from a dictionary, so the order is not guaranteed.
        """
        return list(cls.sqlmeta.columns.keys())

    def getData(self, quiet=True):
        """
        Output the current record with key:value pairs for column name
        and value. Note that this is not suitable to be converted directly to
        JSON because of the data types of some values.

        TODO: Ensure that attributes of the parent and child are all accessed,
        to get more use out of this.
        """
        data = {col: getattr(self, col) for col in self.getColumnNames()}

        if not quiet:
            for k, v in data.items():
                print(f"{k:>15} : {v}")

        return data


class Supername(Place):
    """
    Global level place, which can have continents. Taken from 'Supername'
    title for the world, in Twitter API.
    """

    _inheritable = False

    # Get Continent objects belong to the Supername. Defaults to null list.
    hasContinents = so.MultipleJoin("Continent")


class Continent(Place):
    """
    A continent, which can have countries.
    """

    _inheritable = False

    # Supername which this Continent belongs to.
    supername = so.ForeignKey("Supername")

    # Get Country objects belonging to the Continent. Defaults to null list.
    hasCountries = so.MultipleJoin("Country")


class Country(Place):
    """
    Place which is a Country in Twitter API.
    """

    _inheritable = False

    # Continent which this Country belongs to.
    continent = so.ForeignKey("Continent", default=None)

    # Get Town objects belonging to the Country. Defaults to null list.
    hasTowns = so.MultipleJoin("Town")

    # Two-character string as the country's code.
    countryCode = so.StringCol(length=2, default=None)


class Town(Place):
    """
    Place which falls into Town or Unknown category in Twitter API.
    """

    _inheritable = False

    # Country which this Town belongs. Optional and defaults to None.
    country = so.ForeignKey("Country", default=None)
    countryIdx = so.DatabaseIndex(country)
