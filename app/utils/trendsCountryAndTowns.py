#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
# Allow imports of dirs in app.
sys.path.insert(0, os.path.abspath(os.path.curdir))

from lib import places, trends, twitterAuth
from lib.setupConf import conf


api = twitterAuth.getAPIConnection()

countryName = conf.get('Cron', 'countryName')
print countryName

woeidIDs = places.countryAndTowns(countryName)
for woeid in woeidIDs:
    trends.insertTrendsForWoeid(woeid)
