#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A utility to be called on schedule to trend data for a country and cities and
add to the database.

The default connection details are used from trends.py.

Usage:
    ./utils/trendsCountryAndTowns.py
"""
import os
import sys
# Allow imports of dirs in app.
sys.path.insert(0, os.path.abspath(os.path.curdir))

from lib import dbQueries, places, trends, twitterAuth
from lib.setupConf import conf


def main(args):
    print 'Starting job for trends by country and towns.'
    if args:
        if '--help' in args or '-h' in args:
            print 'Help option selected. See available countries below.\n'
            dbQueries.showTownCountByCountry()
            print 'Enter a country name from the above as first argument, ' \
                'or use no arguments to get the configured country.'
            sys.exit(0)

        # Set country name from first argument.
        countryName = args[0]
    else:
        # Use configured country name.
        countryName = conf.get('Cron', 'countryName')

    print u'Country: {}'.format(countryName)

    woeidIDs = places.countryAndTowns(countryName)
    for woeid in woeidIDs:
        trends.insertTrendsForWoeid(woeid)


main(sys.argv[1:])
