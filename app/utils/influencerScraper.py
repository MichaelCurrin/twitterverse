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
import io
import sys
import os

import requests
from bs4 import BeautifulSoup

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))
from lib.config import AppConf

conf = AppConf()
CATEGORIES = ['followers', 'following', 'tweets', 'engagements']


def getUsernamesInCategory(category, short=True):
    """
    Get top Twitter usernames from website for a given category.

    @param category: an influencer category as a string, indicating which
        webpage to lookup and therefore which category the usernames returned
        will fit into.
    @param short: Default True. If True, scrape 10 items from each category,
        otherwise get 100.

    @return userList: List of usenames as unicode strings, for Twitter profiles
        which match the category argument.
    """
    global CATEGORIES
    assert category in CATEGORIES, 'Category must be one of {0}.'\
        .format(CATEGORIES)

    count = 10 if short else 100
    URI = 'https://socialblade.com/twitter/top/{0}/{1}'.format(count, category)
    data = requests.get(URI, timeout=5).text
    soup = BeautifulSoup(data, 'lxml')

    userList = []
    # Find the <a> tags which contain the usernames.
    for tag in soup.find_all('a'):
        # If the link value matches the expected format, we get the tag's
        # value i.e. just the username.
        link = tag.get('href')
        if link and link.startswith('/twitter/user/'):
            userList.append(tag.string)

    return userList


def writeInfluencerFiles(short=True):
    """
    Lookup short or long lists of Twitter influencer names from source
    website for the configured categories, then write out a text file of
    usernames for each category.

    @param short: Default True. If True, scrape 10 items from each category,
        otherwise get 100.

    @return: None
    """
    if short:
        count = 10
        size = 'short'
    else:
        count = 100
        size = 'long'

    outputDir = conf.get('Data', 'scrapeOutputDir')
    assert os.access(outputDir, os.W_OK), (
        "Unable to write to configured influencer scraper output dir: {0}"
        .format(outputDir)
    )
    print 'Output dir: {0}'.format(outputDir)
    today = str(datetime.date.today())

    for cat in CATEGORIES:
        users = getUsernamesInCategory(cat, count)
        filename = "{cat}-{size}-{date}.txt".format(cat=cat, size=size,
                                                    date=today,)
        path = os.path.join(outputDir, filename)
        # Write out unicode with this instead of the open builtin.
        with io.open(path, 'wb') as f:
            f.writelines(u'\n'.join(users))
        print "Wrote {0}".format(filename)


def main():
    """
    Command-line tool to get all Twitter usernames from available
    categories and write to appropriately named files in the configured dir.

    @param args: command-line arguments as list of strings.

    @return: None
    """
    # Use  a help formatter to wrap description with deliberate line breaks,
    # The alternative raw text help formatter would wrap argument help
    # unnaturally by ignoring the boundary between arguments and help.
    parser = argparse.ArgumentParser(
        description="Influencer scraper utility. \n\nScrape usernames of"
            " influencial Twitter users from a website and store locally in"
            " text files for each category. The files are saved to a"
            " configured directory, with filenames in the following format:"
            " CATEGORY-DATE-SIZE.txt where CATEGORY is a relevant category,"
            " DATE is today's date and SIZE is either short or long.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--short', dest='short', action='store_true',
                        help="Retrieve only 10 profiles for each category."
                             " Defaults to True.")
    parser.add_argument('--long', dest='short', action='store_false',
                        help="Boolean flag to retrieve 100 profiles for"
                             " category instead of the usual 10. Default false."
                        )
    parser.set_defaults(short=True)

    args = parser.parse_args()

    writeInfluencerFiles(short=args.short)


if __name__ == '__main__':
    main()
