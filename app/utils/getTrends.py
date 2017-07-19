#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Get Trend data for Places. This is a utility intended to be run as cronjob.

Usage:
    $ python ./utils/getTrends.py
"""
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))

from sqlobject import SQLObjectNotFound

from lib import database as db
from lib.setupConf import conf


countryWoeid = conf.getint('Cron', 'countryWoeid')
try:
    countryObj = db.Place.byWoeid(countryWoeid)
except SQLObjectNotFound as e:
    msg = 'Unable to find country WOEID {0} in the database.'\
            .format(countryWoeid)
    print 'ERROR {0}. {1}'.format(type(e).__name__, msg)
    raise type(e)(msg)

print countryObj
