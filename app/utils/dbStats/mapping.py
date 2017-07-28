#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Database stats report for how Places are mapped to each other.

Usage:
    $ python mapping.py
    # => print results to console.
"""
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                                      os.pardir))
# Make dirs in app dir importable.
if appDir not in sys.path:
    sys.path.insert(0, appDir)

from lib import database as db


def showPlacesMapping():
    """
    Print out data of all records in Place table, grouping records in
    a visual tree structure as child and parent objects.

    Parent place names are not repeated.
    """
    supers = db.Supername.select()

    for s in supers:
        continents = s.hasContinents
        print u'* {0} ({1:d} continents)'.format(s.name, len(continents))

        for continent in continents:
            countries = continent.hasCountries
            print u'  * {0} ({1:d} countries)'.format(continent.name,
                                                      len(countries))

            for country in countries:
                towns = country.hasTowns
                print u'    * {0} ({1:d} towns)'.format(country.name,
                                                        len(towns))

                for town in towns:
                    print u'      * {0}'.format(town.name)


if __name__ == '__main__':
    showPlacesMapping()