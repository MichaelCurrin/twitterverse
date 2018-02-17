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
import sys
import webbrowser

import tweepy

from lib.config import AppConf


conf = AppConf()

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

    @return: tweetpy.OAuthHandler instance, with App Access Token set.
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

    @return: tweetpy.OAuthHandler instance, with User Access Token set.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    print "You need to authorise the application. Opening page in browser..."
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


def getAPIConnection(userFlow=False):
    """
    Generate a tweepy API object using either App or User Access Token flow.

    @param userFlow: If True, use the browser-based user flow and generate
        a User Access Token.

        NOTE: When testing the user flow functionality, do NOT sign into
        Twitter in the browser as same user you use to create Twitter
        app credentials. Otherwise your access token and secret will be
        regenerated and you will have to get new values from dev.twitter.com
        and then add them to app conf.

    @return api: Authenticated tweepy.API instance for doing queries with,
        with either App or User Access Token set depending on the
        userFlow argument value.
    """
    if userFlow:
        print 'Generating user API token...'
        auth = _generateUserToken()
    else:
        print 'Generating app API token...'
        auth = _generateAppToken()

    # Override defaults so that tweepy always wait if rate limit is exceeded
    # and will print out a notification.
    api = tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    me = api.me()
    print 'Authenticated with Twitter API as `{0}`.\n'.format(me.name)

    return api


def getAppOnlyConnection():
    """
    Follow Application-only Auth flow for authenticating with Twitter API.

    @return api: authenticated tweepy.API instance with Application-only
        Auth permissions to do queries with.
    """
    print "Generating Application-Only Auth..."
    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Override defaults so that tweepy always wait if rate limit is exceeded
    # and will print out a notification.
    api = tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )
    print 'Authenticated with Twitter API.'

    return api


def main(args):
    """
    Main function to test script with command-line arguments.

    TODO: Add separate test Application-only Auth and update the arg parser.
    Also, rewrite using argparse.
    """
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage: python -m lib.twitter.auth [-t|--test] [-u|--user]'\
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
        if set(args) & set(('-t', '--test')):
            userFlow = set(args) & set(('-u', '--user'))
            getAPIConnection(userFlow)


if __name__ == '__main__':
    main(sys.argv[1:])
