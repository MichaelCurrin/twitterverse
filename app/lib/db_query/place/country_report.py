"""
Select country data from the database.

Usage:
    $ python -m lib.db_query.place.country_report --help
"""
from collections import Counter

from lib import database as db


def showTownCountByCountry(by_name=False, by_frequency=False):
    """
    Print a list of all countries and number of towns in each.
    """
    countries = db.Country.select().orderBy('name')

    assert by_name or by_frequency, \
        'Choose at least one of the by name or by frequency report.'

    if by_name:
        print("Report by country name")
        print('Country              | Towns')
        print('=====================|======')
        for x in countries:
            stars = len(x.hasTowns) // 10 * '*'
            print(f'{x.name:20} | {len(x.hasTowns):4,d} {stars}')
        print()

    if by_frequency:
        print("Report by most towns")
        print('Country              | Towns')
        print('=====================|======')
        country_set = Counter()
        for x in countries:
            country_set.update({x.name: len(x.hasTowns)})
        for y in country_set.most_common():
            stars = y[1] // 10 * '*'
            print(f'{y[0]:20} | {y[1]:4,d} {stars}')
        print()


def main(args):
    """
    Function to run when executing this script directly on the command-line.

    Prints usage instructions and if appropriate arguments are given prints
    a report of town and country stats.
    """
    if not args or set(args) & {'-h', '--help'}:
        print('Usage: python -m lib.db_query.place.country_report [-n|--name]'
              ' [-f|--frequency] [-h|--help]')
        print('Order by name ascending or by frequency of towns descending.'
              ' Or use, both flags to output two reports.')
    else:
        by_name = set(args) & {'-n', '--name'}
        by_freq = set(args) & {'-f', '--frequency'}
        showTownCountByCountry(by_name, by_freq)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
