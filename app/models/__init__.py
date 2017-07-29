# -*- coding: utf-8 -*-
"""
Models module.

The application SQLite database model as setup in SQLObject.

The db model structure is:
 * Place
    - contains records of all Places
 * Supername -> Continent -> Country -> Town
     - These tables are linked to each other in a hiearchy such that a
         Supername has Continents, which have Countries, which have Towns.
    - These all inherit from Place.
    - Every record in  one of these tables has a record in Place table
        with the same ID.
 * Trend
    - contains a trend record for a specific time and space. Each record
        has a foreign key to map it to a Place record, derived from the
        Trend's WOEID value in the API.

This approach makes it easy to always map a Trend record to the same
table (Place) instead of many, while still allowing easy seperation of
Place types in the Place-related tables.
    e.g. show all Places
    e.g. show all from Countries table and count of its Towns we have mapped
        to it.
    e.g. show Towns which are in Asia
"""
# Create __all__ list using values set in other application files.
from places import __all__ as p
from trends import __all__ as t
__all__ = p + t

# Make objects available on models module.
from places import *
from trends import *
