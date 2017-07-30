#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A utility to get trend data for a country and cities and add to the database.

Usage:
    $ cd twitterverse
    $ ./app/utils/trendsCountryAndTowns.py
"""
# Make dirs in app dir available for import.
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import places, trends
from lib.query.place import countryReport
from lib.config import AppConf

appConf = AppConf()


def main(args):
    if not args or set(args) & set(('-h', '--help')):
        print u'Help option selected.'
        print u'See available countries below...\n'
        import time
        time.sleep(2)
        countryReport.showTownCountByCountry(byName=True)
        print u'Enter a country name from the above as first argument, ' \
            'or use `default` to get the configured country.'
    else:
        print u'Starting job for trends by country and towns.'
        if args[0] == 'default':
            # Use configured country name.
            countryName = appConf.get('Cron', 'countryName')
	    assert countryName, ('Please fill in a country name in Cron '
				 'section of local app conf file.')
        else:
            # Set country name string from arguments list.
            countryName = ' '.join(args)
        print u'Country: {}'.format(countryName)

        woeidIDs = places.countryAndTowns(countryName)
        for woeid in woeidIDs:
            trends.insertTrendsForWoeid(woeid)


main(sys.argv[1:])
