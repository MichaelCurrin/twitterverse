# -*- coding: utf-8 -*-
"""
Get data from the database.

Usage:
    $ python -m lib.query.place.countryReport --help
"""
from collections import Counter

from lib import database as db


def showTownCountByCountry(byName=False, byFrequency=False):
    """
    Print a list of all countries and number of towns in each.
    """
    countries = db.Country.select().orderBy('name')

    assert byName or byFrequency, ('Choose at least one of the by name '
                                   'or by frequency report.')
    if byName:
        # Report by country name.
        print 'Country              | Towns'
        print '=====================|======'
        for x in countries:
            print '{0:20} | {1:4,d} {2}'.format(x.name, len(x.hasTowns),
                                                (len(x.hasTowns)/10)*'*')
        print
    if byFrequency:
        # Report by most towns.
        print 'Country              | Towns'
        print '=====================|======'
        countrySet = Counter()
        for x in countries:
            countrySet.update({x.name: len(x.hasTowns)})
        for y in countrySet.most_common():
            print '{0:20} | {1:4,d} {2}'.format(y[0], y[1], (y[1]/10)*'*')
        print


def main(args):
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage: python -m lib.query.place.countryReport [-n|--name] [-f|--frequency] [-h|--help]'
        print 'Select to order by by name ascending or by frequency of towns descending, or both to output two reports.'
    else:
        byName = set(args) & set(('-n', '--name'))
        byFrequency = set(args) & set(('-f', '--frequency'))
        showTownCountByCountry(byName, byFrequency)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
