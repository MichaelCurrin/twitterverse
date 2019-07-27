# -*- coding: utf-8 -*-
"""
Twitter auth application file.

Generate tweepy API connection object for doing queries.

The following types of authorisation are available:
- App Access Token
- User Access Token
- Application-Only Auth

Note on Application-Only Auth:
    This method does not have a sense of a user, but it does have relaxed
    rate limits and still be used for useful tasks like pulling user timelines
    or searching for tweets.

    See Twitter's documentation:
        https://developer.twitter.com/en/docs/basics/authentication/overview/application-only

    The flow implemented here is based on this article:
        https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

This script is based on these examples:
    https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
    http://docs.tweepy.org/en/latest/code_snippet.html

Usage:
    # Test configured credentials or user flow.
    $ python -m lib.twitter.auth --help

    # Create API connection object to be used in other scripts.
    >>> from lib.twitter import auth
    >>> appCon = auth.getAPIConnection()
    >>> userCon = auth.getAPIConnection(userFlow=True)
    >>> appOnlyCon = auth.getAppOnlyConnection()
"""
import datetime
import logging
import sys
import webbrowser

import tweepy

from lib.config import AppConf


conf = AppConf()
logger = logging.getLogger("lib.twitter.auth")

# Setup configured authentication values as global variables.
CONSUMER_KEY = conf.get('TwitterAuth', 'consumerKey')
CONSUMER_SECRET = conf.get('TwitterAuth', 'consumerSecret')
ACCESS_KEY = conf.get('TwitterAuth', 'accessKey')
ACCESS_SECRET = conf.get('TwitterAuth', 'accessSecret')

# Raise an error for unset or default consumer values. But, do not check access
# keys, since a user token can be generated still, using the user flow.
msg = ("Invalid Twitter auth details. Register your own Twitter app at"
       " dev.twitter.com, then paste your credentials in a `app.local.conf`"
       " file using headings as in `app.conf`.")
assert CONSUMER_KEY and CONSUMER_SECRET and \
    CONSUMER_KEY != 'YOUR_CONSUMER_KEY', msg


def _generateAppToken():
    """
    Generate a Twitter API connection with app access.

    Uses the Twitter account details set in the config files and generates
    a auth object with no input required.

    :return: tweetpy.OAuthHandler instance, with App Access Token set.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    return auth


def _generateUserToken():
    """
    Generate a Twitter API connection with user access.

    Requires the user to view the browser URI which is automatically opened,
    then manually enter the pin in the command-line in order to generate
    the access token.

    :return: tweetpy.OAuthHandler instance, with User Access Token set.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    print "You need to authorise the application. Opening page in browser...\n"
    authURL = auth.get_authorization_url()
    webbrowser.open(authURL)

    # This is limited to command line input for now, with no GUI.
    userPin = raw_input("Generate a pin and enter it here, or type"
                        " `quit`. /> ")
    if not userPin or userPin.lower() in ('q', 'quit', 'exit'):
        print 'Exiting.'
        exit(0)
    print 'Authenticating...'
    auth.get_access_token(userPin)

    return auth


def _getTweepyConnection(auth):
    """
    Return tweepy API connection using configured parameters.

    Override wat defaults so that tweepy will always wait if rate limit is
    exceeded and will print out a notification.
    """
    return tweepy.API(
        auth,
        retry_count=conf.getint('APIRequests', 'retryCount'),
        retry_delay=conf.getint('APIRequests', 'retryDelay'),
        retry_errors=[401, 404, 500, 503],
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )


def getAPIConnection(userFlow=False):
    """
    Generate a tweepy API object using the App Access or User Access Token flow.

    :param userFlow: If True, use the browser-based user flow and generate
        a User Access Token.

        NOTE: When testing the user flow functionality, do NOT sign into
        Twitter in the browser as SAME user you use to create Twitter
        app credentials with. Otherwise your access token and secret will be
        regenerated and you will have to get new values from dev.twitter.com
        and then add them to app conf.

    :return api: Authenticated tweepy.API instance for doing queries with,
        with either App or User Access Token set depending on the
        userFlow argument value.
    """
    print 'Generating API token...'
    start = datetime.datetime.now()

    if userFlow:
        tokenType = "User Access Token"
        auth = _generateUserToken()
    else:
        tokenType = "App Access Token"
        auth = _generateAppToken()
    api = _getTweepyConnection(auth)

    duration = datetime.datetime.now() - start

    me = api.me()
    message = "Authenticated with Twitter API as `{name}`. {tokenType}."\
        " Duration: {duration:3.2f}s.".format(
            name=me.name,
            tokenType=tokenType,
            duration=duration.total_seconds()
        )
    logger.info(message)

    return api


def getAppOnlyConnection():
    """
    Generate a tweepy API object using Application-only Auth flow.

    The App-only authentication method uses consumer credentials and no
    access credentials. It has different rate limits and is better in some
    cases such as searching for tweets.

    :return api: authenticated tweepy.API instance with Application-only
        Auth permissions to do queries with.
    """
    print "Generating Application-Only Auth..."
    start = datetime.datetime.now()

    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = _getTweepyConnection(auth)

    duration = datetime.datetime.now() - start
    message = "Authenticated with Twitter API. Application-only Auth."\
        " Duration: {duration:3.2f}".format(duration=duration.total_seconds())
    logger.info(message)

    return api


def main(args):
    """
    Main function to test script with command-line arguments.

    TODO: Add separate test Application-only Auth and update the arg parser.
    Also, rewrite using argparse.
    """
    if not args or set(args) & {'-h', '--help'}:
        print 'Usage: python -m lib.twitter_api.auth [-t|--test] [-u|--user]'\
            ' [-h|--help]'
        print 'Options and arguments:'
        print '--test : Run test to get Twitter API connection and print out '
        print '         authenticated user name. Defaults to builtin app'\
            ' token method'
        print '         which uses configured app credentials.'
        print '--user : Use in conjunction with --test flag to make'
        print '         authentication method follow the user flow where the'\
            ' user is'
        print '         prompted to authorise in the browser, get a pin'\
            ' number and'
        print '         paste it back into the application.'
    else:
        if set(args) & {'-t', '--test'}:
            userFlow = set(args) & {'-u', '--user'}
            getAPIConnection(userFlow)


if __name__ == '__main__':
    main(sys.argv[1:])