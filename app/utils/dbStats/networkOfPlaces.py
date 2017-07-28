#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Database stats report for Network of Places.

Usage:
    $ python networkOfPlaces.py
    # => print results to console.

    $ python networkOfPlaces.py > ~/path/to/file.csv
    # => redirect output to CSV file.
"""
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                                      os.pardir))
# Make dirs in app dir importable.
if appDir not in sys.path:
    sys.path.insert(0, appDir)

from lib import database as db


def getPlacesNetwork():
    """
    Create output showing Place objects mapping to parent Places, shown
    as two columns. Parents place names are repeated.

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
    getPlacesNetwork()
