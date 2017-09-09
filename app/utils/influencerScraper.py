#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 23:12:33 2016

@author: michaelcurrin

Get the handles of top users on twitter
by scraping data from four top 100 lists from socialblade.com
Create a list of unique handles across the lists.
Sort and print it.
"""
import requests # for opening URLs
from bs4 import BeautifulSoup # for processing HTML tags
import re # for regex matches

# Setup categories and URLs

base_url = 'https://socialblade.com/twitter/top/100/%s'
pages = [dict(name= 'Top Followers', url= base_url % 'followers'),
         dict(name= 'Top Following', url= base_url % 'following'),
         dict(name= 'Most Tweets', url= base_url % 'tweets'),
         dict(name= 'Most Engagements', url = base_url % 'engagements')
         ]

search_string = '/twitter/user/'

# Query each URL in pages list

for i in range(len(pages)):
    pages[i]['handles'] = [] # create empty list in dict

    # load data from url
    url = pages[i]['url']
    data = requests.get(url).text
    soup = BeautifulSoup(data,'lxml')

    # find <a> tags on the page to get 100 users on page
    for tag in soup.find_all('a'):
        link = tag.get('href')

        # search for pattern using
        pattern = '^%s' % search_string
        result = re.match(pattern,link)

        if result:
            # extract handle after search term
            handle = link[len(search_string):]
            pages[i]['handles'].append(handle)

# set to True to print contents of each list
if False:
    for item in pages:
        print item['name']
        print '----------'
        for i, h in enumerate(item['handles']):
            print '%i) %s' % (i+1, h)
        print

# Create unique list
unique_handles = []

for item in pages:
    for handle in item['handles']:
        if handle not in unique_handles:
            unique_handles.append(handle)

# Sort and print unique list
sorted_handles = sorted(unique_handles)
print 'Top Twitter handles'
for i, h in enumerate(sorted_handles):
    print '%i) %s' % (i+1, h)


# Sample result
"""
Top Twitter handles
1) 000120o
2) 2m___m2
3) 2morrowknight
4) 2of__
5) 2thank
...
374) xtina
375) yokoono
376) youm7
377) yvesjean
378) zaynmalik
"""
