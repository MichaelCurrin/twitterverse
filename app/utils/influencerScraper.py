#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Twitter influencer scraping utility.

Usage:
    $ ./utils/influencerScraper.py > var/influencers.txt

Scrape profile usernames of the most influencial Twitter accounts from
a website and then save the output. The usernames can be stored in a database
and used to lookup tweets by those users.

The source is webpages on socialblade.com, which covers the profiles with
highest followers, highest following count, most tweets or most engagements.

These Twitter influencers tend to be policitians, companies, musicians, actors
and so on. They are likely to talk to each other and to possibly talk
about trending topics - they may even be the reason that a topic becomes
trending or they may simply be sharing opinion on what is already a trending
topic.
"""
import requests
from bs4 import BeautifulSoup


CATEGORIES = ['followers', 'following', 'tweets', 'engagements']


def getUsernamesInCategory(category, count=100):
    """
    Get top Twitter usernames from website for a given category.

    @param category: an influencer category as a string, indicating which
        webpage to lookup and therefore which category the usernames returned
        will fit into.
    @param count: Number of influecers to get as an integer. Expected values
        based on current existing webpages are 100 or 10. Default 100.

    @return userList: List of usenames as strings, for Twitter profiles
        which match the category argument.
    """
    global CATEGORIES
    assert category in CATEGORIES, 'Category must be one of {0}.'\
        .format(CATEGORIES)

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


def getAllUsernames():
    """
    Return Twitter influencer names from across available categories.

    @param userList: List of unqiue, alphabetically sorted Twitter usernames
        as strings, from across the available categories.
    """
    aggregateList = []
    for c in CATEGORIES:
        aggregateList.extend(getUsernamesInCategory(c))

    userSet = set(aggregateList)
    userList = sorted(userSet)

    return userList


def main():
    """
    Get all Twitter usernames from available categories and print to stdout.
    """
    for username in getAllUsernames():
        print username


if __name__ == '__main__':
    main()
