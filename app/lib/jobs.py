# -*- coding: utf-8 -*-
"""
Jobs lib application file.
"""
from __future__ import absolute_import
import datetime

from sqlobject.sqlbuilder import OR

from lib import database as db
from lib.config import AppConf


conf = AppConf()


def orCondition():
    """
    Create time filter for jobs to be run.

    A job record be should run at least once per day and may run multiple
    times on a day, but with a minimum interval of N hours between runs.
    A cron manager could even run a job session (of job records) hourly,
    yet skip over job records where the data we have is recent enough.

    This process is useful for getting data say 4 times a day at 6-hour
    intervals. Also, if a job session crashes and is restarted, it only
    continues with the jobs not completed in that job session.

    A job record should be run if ANY of the following are true:
        - it has never run, or
        - it has not run today (since we need values for today and we might
            not again the job session again today), or
        - it was run today but more than N hours ago (the time since
            the last success for today is old enough that it is useful
            to get more records for today, as we might want to compare
            changes over the day).
    """
    now = datetime.datetime.now()

    # Use current time to get midnight for today, but as datetime object.
    dateCuttoff = datetime.datetime(now.year, now.month, now.day)

    # Use minimum number of hours between job sessions to get the cuttoff time
    # for considering a job run recently.
    interval = conf.getint('TrendCron', 'interval')
    hoursCuttoff = now - datetime.timedelta(hours=interval)

    # From the last two conditions, we check whether the last completed time
    # is either less than the start of today or the recent cuttoff time,
    # therefore we can simplify by comparing against the higher of the two.
    recencyCuttoff = max(dateCuttoff, hoursCuttoff)

    # The ORM needs `==` rather than `is` to build the query correctly.
    return OR(db.PlaceJob.q.lastCompleted == None,  # noqa: E711
              db.PlaceJob.q.lastCompleted < recencyCuttoff)
