# -*- coding: utf-8 -*-
"""
Setup tweepy authentication.

Based on https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
"""
import os
import sys

import tweepy

p = os.path.abspath(os.path.curdir)
sys.path.insert(0, p)
from lib import conf

# Get access token.
auth = tweepy.OAuthHandler(conf.get('TwitterAuth', 'CONSUMER_KEY'),
                           conf.get('TwitterAuth', 'CONSUMER_SECRET'))
auth.set_access_token(conf.get('TwitterAuth', 'ACCESS_KEY'),
                      conf.get('TwitterAuth', 'ACCESS_SECRET'))

# Construct the API instance.
api = tweepy.API(auth)

if __name__ == '__main__':
    # From app dir, test as:
    #   $ python lib/twitterAuth.py
    # If the authentication was successful, you should see the name of your 
    # account print out.
    print api.me().name
