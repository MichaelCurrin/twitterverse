# -*- coding: utf-8 -*-
"""
Database stats report to show how Places are mapped to each other, as a tree
structure.

Usage:
    $ python -m lib.query.place.tree
    # => print results to console.
"""
from lib import database as db


def printTree():
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
    printTree()
