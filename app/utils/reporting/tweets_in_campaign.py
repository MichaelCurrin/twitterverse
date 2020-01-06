#!/usr/bin/env python
"""
Tweets in campaign report.

Generate a CSV report of tweets and profiles, for a given campaign name which
was allocated to tweets.
"""
import csv
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db
from lib.config import AppConf

conf = AppConf()
REPORT_DIR = conf.get('Reporting', 'reportingDir')


def write_csv(path, rows, append=False):
    """
    Write a CSV file to a path with given rows and header from first row.

    Default behavior is to overwrite an existing file. Append to existing file
    if append is flag True. Either way, the header will only be added on a new
    file. Appending is useful when adding sections to a report, but overwriting
    is better when rerunning an entire report.
    """
    if not rows:
        print("No rows to write")
        print()
        return

    is_new_file = not os.path.exists(path)
    mode = 'a' if append else 'w'

    fieldnames = rows[0].keys()
    with open(path, mode) as f_out:
        writer = csv.DictWriter(f_out, fieldnames)
        if is_new_file or not append:
            writer.writeheader()
        writer.writerows(rows)

    print("Wrote CSV:")
    print(f" - {path}")
    print(f" - {len(rows)} rows {'appended' if append else ''}")
    print()


campaign_name = 'foo'
campaign_tweets = db.Campaign.byName(campaign_name).tweets


rows = [tweet.report() for tweet in campaign_tweets]


filename = f"Tweets for campaign - {campaign_name}.csv"
path = os.path.join(REPORT_DIR, filename)

write_csv(path, rows)
