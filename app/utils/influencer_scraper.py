#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Twitter influencer scraping utility.

Scrape profile usernames of the most influencial Twitter accounts from
a website and then writes text file to output directory. The usernames
can later be read in and used to look up Profiles and Tweets for those users.

The source is socialblade.com webpages, which covers the profiles with
highest followers, highest following count, most tweets or most engagements.

These Twitter influencers tend to be policitians, companies, musicians, actors
and so on. They are likely to talk to each other and to possibly talk
about trending topics - they may even be the reason that a topic becomes
trending or they may simply be sharing opinion on what is already a trending
topic.
"""
import argparse
import datetime
import sys
import os

import requests
from bs4 import BeautifulSoup

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir)
))

from lib.config import AppConf


conf = AppConf()
# The 4 possible areas which the socialblade site categorises Twitter accounts.
# These are expected to be static and therefore are not configurable.
INFLUENCER_CATEGORIES = ['followers', 'following', 'tweets', 'engagements']


def getUsernamesInCategory(category, short=True):
    """
    Get top Twitter usernames from website for a given category.

    When doing requests from all categories in quick succession, the 4th
    one often times out on a 5 second limit, therefore this extended to 10
    seconds.

    :param category: an influencer category as a string, indicating which
        webpage to lookup and therefore which category the usernames returned
        will fit into.
    :param short: Default True. If True, scrape 10 items from each category,
        otherwise get 100.

    :return userList: List of usenames as str, for Twitter profiles which
        match the category argument.
    """
    assert category in INFLUENCER_CATEGORIES, "Category must be one of {0}."\
                                              .format(INFLUENCER_CATEGORIES)

    URI = "https://socialblade.com/twitter/top/{count}/{category}".format(
        count=10 if short else 100,
        category=category
    )
    headers = {'User-Agent': conf.get('Scraper', 'userAgent')}
    timeout = conf.getfloat('Scraper', 'timeout')

    resp = requests.get(
        URI,
        headers=headers,
        timeout=timeout
        )
    assert resp.status_code == 200, \
        "Expected 200 status code but got: {code} {reason} \n{uri}".format(
            code=resp.status_code,
            reason=resp.reason,
            uri=URI
        )
    data = resp.text
    soup = BeautifulSoup(data, 'lxml')

    userList = []
    # Find the <a> tags which contain the usernames.
    for tag in soup.find_all("a"):
        # If the link value matches the expected format, we get the tag's
        # value i.e. just the username.
        link = tag.get("href")
        if link and link.startswith("/twitter/user/"):
            # The data object was unicode, but we don't expect any special
            # unicode characters, so force values to str for simplified file
            # writing.
            userList.append(str(tag.string))

    return userList


def writeInfluencerFiles(short=True):
    """
    Lookup short or long lists of Twitter influencer names from source
    website for the configured categories, then write out a text file
    for each category with rows of usernames.

    :param short: Default True. If True, scrape 10 items from each category,
        otherwise get 100.

    :return: None
    """
    outputDir = conf.get('Scraper', 'outputDir')
    assert os.access(outputDir, os.W_OK), (
        "Unable to write to configured influencer scraper output dir: {0}"
        .format(outputDir)
    )
    print 'Output dir: {0}'.format(outputDir)
    today = str(datetime.date.today())

    for cat in INFLUENCER_CATEGORIES:
        users = getUsernamesInCategory(cat, short)

        filename = "{cat}-{size}-{date}.txt".format(
            cat=cat,
            size="short" if short else "long",
            date=today
        )
        path = os.path.join(outputDir, filename)
        with open(path, 'wb') as f:
            f.writelines("\n".join(users))
        print "Wrote: {0}".format(filename)


def main():
    """
    Command-line tool to get all Twitter usernames from available
    categories and write to appropriately named files in the configured dir.

    :return: None
    """
    parser = argparse.ArgumentParser(
        description="""Influencer scraper utility. Scrape usernames of
            influencial Twitter users from a website and store locally in
            text files for each category. The files are saved to a
            configured location (shown when the output is generated).
            Filenames are in the following format "CATEGORY-SIZE-DATE.txt",
            where CATEGORY is a relevant category, SIZE is either "short"
            or "long" and DATE is today's date . Existing files with the same
            name will be overwritten without warning."""
    )
    parser.add_argument(
        'size',
        choices=['short', 'long'],
        help="""Retrieve either short (10) or long (100) list of profiles
            for each category. Counts are restricted based on values allowed
            on the source website."""
    )

    args = parser.parse_args()

    short = (args.size == 'short')
    writeInfluencerFiles(short=short)


if __name__ == '__main__':
    main()
