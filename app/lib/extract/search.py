# -*- coding: utf-8 -*-
"""
Extract search application file.

Retrieve tweets with author data from the Twitter Search API and write out
to a CSV in the staging directory.

Application-Only Auth is used for its 480 search requests per rate limit window,
which is better than the 180 of the other token.

TODO: Split into fetch, write and fetchAndWrite functions. Allow printing
after fetch without writing. From the outside, fetch or fetchAndWrite or even
fetchAndPrint could be called rather than using a flag to store vs print only.
"""
import datetime
import logging

from lib.twitter_api import auth, search
from lib.config import AppConf
from lib.extract import csv_writer


conf = AppConf()
logger = logging.getLogger("lib.extract.search")


def _write(searchResults, outPath, campaignName):
    """
    Write out Twitter API search results to a CSV.

    @param Iterable searchResults: Iterable using tweepy.Cursor which produces
        pages of Twitter search results.
    @param str outPath: Path to write out CSV.
    @param str campaignName: Name of Tweet campaign to use in output.

    @return list writeHistory: list of row write counts.
    """
    outPages = []
    # History of how many rows are written on each write command. This can be
    # used to get total count of rows written out at the end of the function.
    # Since the log output does not show that total.
    writeHistory = []

    for i, page in enumerate(searchResults):
        outPages.append(page)

        # Write out all pages in memory on every Nth page. This is based
        # on the limit of 480 requests per 15-min window as a starting point.
        # This could write out more frequently (to see results externally,
        # to reduce memory size and to avoid the risk of losing data in memory)
        # but this less is efficient from a file writing perspective.
        # TODO: This could be a config value.
        if (i+1) % 480 == 0:
            # TODO: Print limited form of the tweets to the console if
            # requesting to print only. Printing all the data is too verbose.
            rowsWritten = csv_writer.writeProfilesAndTweets(
                outPath,
                outPages,
                campaignName=campaignName,
                modified=datetime.datetime.now()
            )
            writeHistory.append(rowsWritten)

            # TODO: When in python3 use list.clear()
            outPages = []

    # Write any pages which have not been written yet.
    if outPages:
        rowsWritten = csv_writer.writeProfilesAndTweets(
            outPath,
            outPages,
            campaignName=campaignName,
            modified=datetime.datetime.now()
        )
        writeHistory.append(rowsWritten)

    return writeHistory


def fetchAndWrite(searchQuery, campaignName=None, pageCount=1, extended=True,
                  APIConn=None):
    """
    Get tweets from the Search API and periodically append rows to a CSV.

    @param searchQuery: Query string to match tweets on the Search API.
    @param campaignName: Optional name of Campaign. This will be written
        as a Campaign label for each tweet in the CSV and will be an empty
        string if left as None.
    @param pageCount: Count of pages to attempt to get from the Search API.
        Defaults to 1. One page can have up to 100 tweets on it.
    @param extended: If True, request to get then expanded text form of
        tweet messages.
    @param APIConn: Optional authorised tweepy.API connection object. If
        not supplied, then an Application-only Auth connection will be
        generated and used to do the search.

    @return: None
    """
    if APIConn is None:
        APIConn = auth.getAppOnlyConnection()

    outPath = conf.get('Staging', 'searchTweets')

    searchResults = search.fetchTweetsPaging(
        APIConn,
        searchQuery=searchQuery,
        pageCount=pageCount,
        extended=extended
    )
    writeHistory = _write(searchResults, outPath, campaignName)

    print "Appended to CSV {0:,d} times.".format(len(writeHistory))
    print "Wrote {0:,d} rows in total.".format(sum(writeHistory))
    print "Output location: {0}".format(outPath)
