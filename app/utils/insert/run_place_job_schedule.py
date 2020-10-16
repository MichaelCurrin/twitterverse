#!/usr/bin/env python
"""
Utility to get trend data based on a list of watched places.

Gets enabled records from PlaceJob table and use the WOEID of each place to
access trend data for that place from Twitter API and store in the database.
"""
import os
import sys
import time

# Allow imports to be done when executing this file directly.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
    ),
)

from lib import database as db, jobs
from lib.config import AppConf
from lib.trends import insertTrendsForWoeid


appConf = AppConf()


def requestTrends(placeJob):
    """
    Run the place job to get trend data, then insert into the database.

    Use the Place of a PlaceJob record, get its WOEID, then request trend data
    and store in the Trend table. Last attempted time is always updated on
    starting the job, while last successful is updated only on completion.

    We catch all errors, so the next job item can run. We use Exception since
    StandardError does not cover the tweepy.error.TweepError exception.
    """
    placeJob.start()

    place = placeJob.place
    try:
        trendsCount = insertTrendsForWoeid(place.woeid, verbose=False)
        print(f"{place.name:20} | {trendsCount} topics added")

        placeJob.end()
    except Exception as e:
        print(
            f"PlaceJob {placeJob.id} failed for {place.name}."
            f" {type(e).__name__}. {str(e)}"
        )


def runAllJobs():
    """
    Select enabled rows in PlaceJob table and run them.

    The time between API calls is forced to be at least the configured cron
    minimum seconds value, by applying a wait if actual duration was too quick.

    :return: None
    """
    minSeconds = appConf.getint("TrendCron", "minSeconds")

    enabled = db.PlaceJob.selectBy(enabled=True)
    queued = enabled.filter(jobs.orCondition())

    print("Starting PlaceJob cron_jobs")
    print(f"  queued items: {queued.count()}")

    for placeJob in queued:
        start = time.time()

        requestTrends(placeJob)

        duration = time.time() - start
        print("  took {0}s".format(int(duration)))
        diff = minSeconds - duration
        if diff > 0:
            time.sleep(diff)


def main(args):
    if set(args) & {"-h", "--help"}:
        print("Run all jobs in the db.")
        print("No options are available for this script.")
    else:
        runAllJobs()


if __name__ == "__main__":
    main(sys.argv[1:])
