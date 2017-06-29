# -*- coding: utf-8 -*-
"""
Initialisation file for lib directory.

Makes app configuration file available.
Makes tweepy objects available.
"""
from ConfigParser import SafeConfigParser

import tweepy

conf = SafeConfigParser()
conf.read(('etc/app.conf', 'etc/app.local.conf'))

# Based on https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
auth = tweepy.OAuthHandler(conf.get('TwitterAuth', 'CONSUMER_KEY'),
                           conf.get('TwitterAuth', 'CONSUMER_SECRET'))
auth.set_access_token(conf.get('TwitterAuth', 'ACCESS_KEY'),
                      conf.get('TwitterAuth', 'ACCESS_SECRET'))

api = tweepy.API(auth)

if __name__ == '__main__':
    # If the authentication was successful, you should
    # see the name of the account print out.
    print api.me().name
