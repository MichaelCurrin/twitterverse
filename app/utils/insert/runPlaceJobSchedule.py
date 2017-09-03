#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Utility to get trend data, based on a list of required places.

Gets enabled records from PlaceJob table and use the WOEID of each place
to access trend data for that place from Twitter API and store in the
database.
"""
# Make dirs in app dir available for import.
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)
import datetime
import time

from sqlobject.sqlbuilder import OR

from lib import database as db
from lib.config import AppConf
from lib.trends import insertTrendsForWoeid


appConf = AppConf()


def requestTrends(placeJob):
    """
    Run the place job - get trend data and insert into the database.

    Use the Place of PlaceJob record, get its WOEID, then request trend
    data and store in the Trend table. Last attempted time is always
    updated on starting the job and last successful is updated on
    completion.

    We catch all errors so the next job item can run.
    We use Exception since StandardError does not cover tweepy.error.TweepError
    """
    placeJob.start()

    place = placeJob.place
    try:
        trendsCount = insertTrendsForWoeid(place.woeid, verbose=False)
        print '{0:20} | {1} topics added'.format(place.name, trendsCount)

        placeJob.end()
    except Exception as e:
        msg = 'PlaceJob {0} failed for {1}. {2}. {3}'.format(
                placeJob.id, place.name, type(e).__name__, str(e)
        )
        print msg


def runAllJobs(lookbackHours=25):
    """
    Select all enabled rows in PlaceJob table which have NOT been run in
    the past N hours and run the jobs.

    The time between API calls is forced to be at least the configured
    cron minimum seconds.

    @lookbackHours: number of hours to look back from current time. If the
        job was run after that time then it is considered recently run.
        Defaults to 25 hours to give margin on a running a job every 24 hours.

    @return: None
    """
    minSeconds = appConf.getint('Cron', 'minSeconds')

    lookbackTime = datetime.datetime.now() \
        - datetime.timedelta(hours=lookbackHours)

    enabled = db.PlaceJob.selectBy(enabled=True)
    queued = enabled.filter(OR(db.PlaceJob.q.lastCompleted == None,
                               db.PlaceJob.q.lastCompleted < lookbackTime))

    print 'Starting PlaceJob cronjobs'
    print '  queued items: {0}'.format(queued.count())

    for placeJob in queued:
        start = time.time()

        requestTrends(placeJob)

        duration = time.time() - start
        print '  took {0}s'.format(int(duration))
        diff = minSeconds - duration
        if diff > 0:
            time.sleep(diff)


def main(args):
    runAllJobs()


if __name__ == '__main__':
    main(sys.argv[1:])
