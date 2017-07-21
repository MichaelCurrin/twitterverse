# -*- coding: utf-8 -*-
"""
Setup tweepy authentication.

Fill in your Twitter app credentials in app.conf or app.local.conf as an
override.
Then from app/ dir, test as:
   $ python lib/twitterAuth.py

Based on 
    https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
    http://docs.tweepy.org/en/latest/code_snippet.html
    https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy
"""
import webbrowser

import tweepy

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib.setupConf import conf

# Setup configured authentication value as global variables.
CONSUMER_KEY = conf.get('TwitterAuth', 'consumerKey')
CONSUMER_SECRET =  conf.get('TwitterAuth', 'consumerSecret')
ACCESS_KEY = conf.get('TwitterAuth', 'accessKey')
ACCESS_SECRET = conf.get('TwitterAuth', 'accessSecret')


def generateAppToken():
    """
    Read configured details for twitter account app and generate auth object
    with an access token set.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    return auth


def generateUserToken():
    """
    Generate a Twitter API access token using configured Twitter app
    credentials.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    print 'You need to authorise the application. Opening page in browser.'
    authURL = auth.get_authorization_url()
    webbrowser.open(authURL)

    # This is fixed to command line input for now.
    userPin = raw_input('Generate a pin and enter it here or enter `quit`. /> ')
    if not userPin or userPin.lower() in ('q', 'quit', 'exit'):
        print 'Exiting.'
        exit(0)
    print 'Authenticating...'
    auth.get_access_token(userPin)

    return auth


def getAPIConnection(userFlow=False):
    """
    Return tweepy API object for API requests. 

    @param userFlow: Default False so that access token is set for configured 
        app. Set to True to use OAuth flow where user directed to sign in with
        a browser and return a pin number back to the application.
    """
    if userFlow:
        auth = generateUserToken()
    else:
        auth = generateAppToken()

    # Construct the API instance. Set tweepy to automatically wait if rate
    # limit is exceeded and to print out a notification.
    api = tweepy.API(auth, wait_on_rate_limit=True, 
                     wait_on_rate_limit_notify=True)

    me = api.me()
    print 'Authenticated as {0}.\n'.format(me.name)

    return api


def _test(args):
    # Opt for authentication with user token instead of app token.
    if args and args[0] in ('-u', '--user'):
        userFlow = True
        args.pop(0)
    else:
        userFlow = False

    api = getAPIConnection(userFlow)


if __name__ == '__main__': 
    _test(sys.argv[1:])
