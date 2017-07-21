#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
# Allow imports of dirs in app.
sys.path.insert(0, os.path.abspath(os.path.curdir))

from lib.setupConf import conf


name = cron.get('Cron', 'countryName')

woeidIDs = places.countryAndTowns(name)

for w in woeidIDs:
    insertTrendsForWoeid(w)
