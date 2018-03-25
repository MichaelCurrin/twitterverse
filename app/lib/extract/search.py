# -*- coding: utf-8 -*-
"""
Extract search application file.

Retrieved tweets with author data from the Twitter Search API and write out
to a CSV in the staging directory.

Application-Only Auth is used for its 480 search requests per rate limit window,
which is better than the 180 of the other token.
"""
import datetime
import logging

from lib.twitter import auth, search
from lib.config import AppConf
from lib.extract import writer


conf = AppConf()
logger = logging.getLogger("lib.extract.search")


def fetchAndWrite(searchQuery, campaignName=None, pageCount=1, extended=True,
                  printOnly=False, APIConn=None):
    """Get tweets from the Search API and periodically append rows to a CSV.

    @param searchQuery: Query string to match tweets on the Search API.
    @param campaignName: Optional name of Campaign. This will be written
        as a Campaign label for each tweet in the CSV and will be an empty
        string if left as None.
    @param pageCount: Count of pages to attempt to get from the Search API.
        Defaults to 1. One page can have up to 100 tweets on it.
    @param extended: If True, request to get then expanded text form of
        tweet messages.
    @param printOnly: If True, print formatted data to the screen but do not
        write to a CSV.
    @param APIConn: Optional authorised tweepy.API connection object. If
        not supplied, then an Application-only Auth connection will be
        generated and used to do the search.

    @return: None
    """
    if APIConn is None:
        APIConn = auth.getAppOnlyConnection()

    outPath = conf.get('Staging', 'searchTweets')
    outPages = []
    # History of how many rows are written on each write command. This can be
    # used to get total count of rows written out at the end of the function.
    # Since the log does not just that total.
    writeHistory = []

    searchResults = search.fetchTweetsPaging(
        APIConn,
        searchQuery=searchQuery,
        pageCount=pageCount,
        extended=extended
    )

    for i, page in enumerate(searchResults):
        outPages.append(page)

        # TODO: Use window wait time as well as max X pages to write data,
        # Prioritise doing a write during deadtime but also use a max multiple
        # to avoid increasing memory, or in case request times are so slow are
        # the rate limit is not reached and tweets have accumulated over an a
        # few window periods. But if write time is quick enough even at high
        # volumes, then this can be simplified to max only and avoid the
        # deadtime implementaton.

        # Write out all pages in memory on every 480th page. This is based
        # on the 480 request per 15-min window and avoids holding a large
        # number in memory without writing them.
        if (i+1) % 480 == 0:
            # TODO: Print limited form of the tweets to the console if
            # requesting to print only. Printing all the data is too verbose.
            rowsWritten = writer.writeProfilesAndTweets(
                outPath,
                outPages,
                campaignName=campaignName,
                modified=datetime.datetime.now()
            )
            writeHistory.append(rowsWritten)

            # The pages are no longer needed once written out. Remove them
            # so they can be cleared from memory.
            outPages[:] = []

    # Write any pages which have not been written yet.
    if outPages:
        rowsWritten = writer.writeProfilesAndTweets(
            outPath,
            outPages,
            campaignName=campaignName,
            modified=datetime.datetime.now()
        )
        writeHistory.append(rowsWritten)

    print "Appended to CSV {0:,d} times.".format(len(writeHistory))
    print "Wrote {0:,d} rows in total.".format(sum(writeHistory))
