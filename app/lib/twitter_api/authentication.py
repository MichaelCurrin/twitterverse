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


def _generateAppAccessToken():
    """
    Generate a Twitter API connection with app access.

    This will use the Twitter account details set in the config files and
    generate an auth object, with no input required.

    :return: tweetpy.OAuthHandler instance, with App Access Token set.
    """
    consumer_key, consumer_secret = conf.getAuthConsumerFields()
    access_key, access_secret = conf.getAuthAccessFields()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return auth


def _generateUserAccessToken():
    """
    Generate a Twitter API connection with access for a specific user.

    Requires the user to view the browser URI that is automatically opened,
    then manually enter the pin in the command-line in order to generate
    the access token.

    :return: tweepy.OAuthHandler instance, with User Access Token set.
    """
    consumer_key, consumer_secret = conf.getAuthConsumerFields()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    print("You need to authorize the application. Opening page in browser...\n")
    authURL = auth.get_authorization_url()
    webbrowser.open(authURL)

    userPin = input("Generate a pin and enter it here, or type"
                    " `quit`. /> ")
    if not userPin or userPin.lower() in ('q', 'quit', 'exit'):
        print('Exiting.')
        exit(0)
    print('Authenticating...')
    auth.get_access_token(userPin)

    return auth


def _getTweepyConnection(auth):
    """
    Return API object which can be used for API calls.

    :param auth: A tweepy.OAuthHandler instance.

    :return: API connection. We override wait defaults, so that tweepy
        will always wait if rate limit is exceeded and will print out a notification.
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
    print('Generating API token...')
    start = datetime.datetime.now()

    if userFlow:
        tokenType = "User Access Token"
        auth = _generateUserAccessToken()
    else:
        tokenType = "App Access Token"
        auth = _generateAppAccessToken()
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
    print("Generating Application-Only Auth...")
    start = datetime.datetime.now()

    consumer_key, consumer_secret = conf.getAuthConsumerFields()
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
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
        print('Usage: python -m lib.twitter_api.auth [-t|--test] [-u|--user]'
              ' [-h|--help]')
        print('Options and arguments:')
        print('--test : Run test to get Twitter API connection and print out ')
        print('         authenticated user name. Defaults to builtin app'
              ' token method')
        print('         which uses configured app credentials.')
        print('--user : Use in conjunction with --test flag to make')
        print('         authentication method follow the user flow where the'
              ' user is')
        print('         prompted to authorise in the browser, get a pin'
              ' number and')
        print('         paste it back into the application.')
    else:
        if set(args) & {'-t', '--test'}:
            userFlow = bool(set(args) & {'-u', '--user'})
            getAPIConnection(userFlow)


if __name__ == '__main__':
    main(sys.argv[1:])
