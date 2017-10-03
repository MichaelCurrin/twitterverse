# -*- coding: utf-8 -*-
"""
Setup authentication so tweepy package can access Twitter API.

Usage:
    # Test configured credentials or user flow.
    $ python -m lib.twitter.auth --help

    # Create API connection object to be used in other scripts.
    $ python
    >>> from lib.twitter import auth
    >>> APIConn = auth.getAPIConnection()

Based on
    https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
    http://docs.tweepy.org/en/latest/code_snippet.html
"""
import webbrowser

import tweepy

from lib.config import AppConf

appConf = AppConf()

# Setup configured authentication values as global variables.
CONSUMER_KEY = appConf.get('TwitterAuth', 'consumerKey')
CONSUMER_SECRET = appConf.get('TwitterAuth', 'consumerSecret')
ACCESS_KEY = appConf.get('TwitterAuth', 'accessKey')
ACCESS_SECRET = appConf.get('TwitterAuth', 'accessSecret')

# Raise an error for consumer values, but access keys may still be blank
# if only user tokens will be used using user flow.
msg = ('Invalid Twitter auth details. Register your own Twitter app at '
       'dev.twitter.com, then paste your credentials in a `app.local.conf`'
       ' file using headings as in `app.conf`.')
assert CONSUMER_KEY and CONSUMER_SECRET and \
    CONSUMER_KEY != 'YOUR_CONSUMER_KEY', msg


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

    Get an App Access Token by default, but if userFlow flag is supplied
    as True then a User Access Token is attempted.

    IMPORTANT: When testing the user flow functionality, do not sign in
    to Twitter in the browser the same user you use to create Twitter
    app credentials. Otherwise your access token and secret will be
    regenerated and you will have to get new values from dev.twitter.com
    and add them to app conf.

    @param userFlow: Default False so that access token is set for configured
        app. Set to True to use OAuth flow where user directed to sign in with
        a browser and return a pin number back to the application.

    @return api: authenticated tweepy.API instance, for doing queries with.
    """
    if userFlow:
        print 'Generating user API token...'
        auth = generateUserToken()
    else:
        print 'Generating app API token...'
        auth = generateAppToken()

    # Construct the API instance. Set tweepy to automatically wait if rate
    # limit is exceeded and to print out a notification.
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    me = api.me()
    print 'Authenticated with Twitter API as `{0}`.\n'.format(me.name)

    return api


def getAppOnlyConnection():
    """
    Follow Application-only Auth flow for authenticating with Twitter API.

    This is an alternative to the App or User Access Token method. It does
    not have a sense of a user, but it has more relaxed rate limits and
    still be used for tasks like pulling user timelines or searching for tweets.
    See https://developer.twitter.com/en/docs/basics/authentication/overview/application-only

    The flow here is based on this article: https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

    @return api: authenticated tweepy.API instance, for doing queries with.
    """
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Construct the API instance. Set tweepy to automatically wait if rate
    # limit is exceeded and to print out a notification.
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    print 'Authenticated with Twitter API using Application-only auth.'

    return api


def main(args):
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage: python -m lib.twitter.auth [-t|--test] [-u|--user]'\
            ' [-h|--help]'
        print 'Options and arguments:'
        print '--test : Run test to get Twitter API connection and print out '
        print '         authenticated user name. Defaults to builtin app token'\
            ' method'
        print '         which uses configured app credentials.'
        print '--user : Use in conjunction with --test flag to make'
        print '         authentication method follow the user flow where the'\
            ' user is'
        print '         prompted to authorise in the browser, get a pin number'\
            ' and'
        print '         paste it back into the application.'
    else:
        if set(args) & set(('-t', '--test')):
            userFlow = set(args) & set(('-u', '--user'))
            getAPIConnection(userFlow)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
