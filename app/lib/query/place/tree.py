# -*- coding: utf-8 -*-
"""
Report to show mapping of Places to each other, in a tree format.

Usage:
    $ python -m lib.query.place.tree
    # => print results to console.
"""
from lib import database as db


def printTree():
    """
    Print out data of all records in Place table.

    Records are grouped in a visual tree structure as child and parent objects.
    No items are repeated, except where two towns happen to have the same name.
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
