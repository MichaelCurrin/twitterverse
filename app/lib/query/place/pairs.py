# -*- coding: utf-8 -*-
"""
Database stats report to show how Places are mapped to each other, as child
and parent pairs.

Usage:
    $ python -m lib.query.place.pairs
    # => print results to console.

    $ python -m lib.query.place.pairs > ~/path/to/file.csv
    # => redirect output to CSV file.
"""
from lib import database as db


def getPairs():
    """
    Create output showing Place objects mapping to parent Places.

    The output is shown as two columns. Parents place names are repeated.

    This can be exported to a CSV file using redirection. The CSV is ideal
    for uploading to Google Fusion tables as an input for a network graph.

    Entries in `Supername` table appear in parent column, but cannot be
    entered here as main places since they do not have a parent.
    """
    data = [('Child', 'Parent')]
    for x in db.Continent.select().orderBy('name'):
        data.append((x.name, x.supername.name))
    for x in db.Country.select().orderBy('name'):
        data.append((x.name, x.continent.name))
    for x in db.Town.select().orderBy('name'):
        data.append((x.name, x.country.name))

    for row in data:
        r = u'"{0}", "{1}"'.format(*row)
        # Handle unicode characters
        r = r.encode('ascii', 'ignore')
        print r


if __name__ == '__main__':
    getPairs()
