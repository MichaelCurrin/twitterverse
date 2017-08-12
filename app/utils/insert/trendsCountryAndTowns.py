#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A utility to get trend data for a country and cities and add to the database.

Run file directly (not as a module) and with `--help` flag in order to see
usage instructions.
"""
import time

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


def listCountries():
    print u'See available countries below...\n'
    countryReport.showTownCountByCountry(byName=True)
    print u'Enter a country name from the above an argument.'
    print u'Or, use `--default` flag to get the configured country, which ' \
          u'is currently `{}`.'.format(appConf.get('Cron', 'countryName'))


def main(args):
    """
    Provide help for the user or runs as a produce to get data from the
    Twitter API for the selected country.

    The API restriction is max 75 trend calls in a 15min window, which is
    5 requests a minute, or 12 seconds allowed between each request.
    Therefore waiting is applied between calls, to reduce the load.

    The max time is set in the app configuration file. If the duration of
    the current iteration was less than the required max then we sleep for
    the remaining number of seconds to make the iteration's total time close
    to 12 seconds. If the duration was more, or the max was configured to
    zero, no waiting is applied.
    """
    global MAX_SECONDS

    if not args or set(args) & set(('-h', '--help')):
        print u'Usage: ./app/utils/trendsCountryAndTowns.py'\
            ' [-d|--default|COUNTRYNAME] [-s|--show] [-f|--fast] [-h|--help]'
    elif set(args) & set(('-s', '--show')):
        listCountries()
    else:
        print u'Starting job for trends by country and towns.'
        if set(args) & set(('-d', '--default')):
            # Use configured country name.
            countryName = appConf.get('Cron', 'countryName')
        else:
            # Set country name string from arguments list, ignoring flags.
            words = [word for word in args if not word.startswith('-')]
            countryName = ' '.join(words)
        assert countryName, ('Country name input is missing.')

        if set(args) & set(('-f', '--fast')):
            # User can override the waiting with a --fast flag, which
            # means queries will be done quick succession, at least within
            # each 15 min rate limited window.
            maxSeconds = 0
        else:
            maxSeconds = appConf.getint('Cron', 'maxSeconds')

        woeidIDs = places.countryAndTowns(countryName)

        for woeid in woeidIDs:
            start = time.time()
            trends.insertTrendsForWoeid(woeid)
            duration = time.time() - start

            print u'  took {}s'.format(int(duration))
            diff = maxSeconds - duration
            if diff > 0:
                time.sleep(diff)


main(sys.argv[1:])
