# -*- coding: utf-8 -*-
"""
Setup tweepy authentication.

Based on 
    https://github.com/tweepy/tweepy/blob/master/examples/oauth.py
    https://github.com/tweepy/tweepy/blob/master/examples/streaming.py
    http://docs.tweepy.org/en/latest/code_snippet.html

Fill in your Twitter app credentials in app.conf or app.local.conf as an
override.
Then from app/ dir, test as:
   $ python lib/twitterAuth.py
"""
from __future__ import print_function

import json
import os
import sys
import time
import webbrowser

import tweepy

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import conf


class _StdOutListener(tweepy.streaming.StreamListener):
    """
    A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    This is based on an example from tweepy docs. This is just here as
    a prototype/experiment for accessing streaming. I have tested
    successfully on a small scale with some limit handling and sleeping.
    But has not been optimised. 
    Use at your own risk of exceeding your rate limit or of having your script 
    exit when a limit is hit. Or possibly keep the safe sleep values but risk
    missing out on tweets.
    """
    def __init__(self, full=True):
        """
        Initialise the standard out listener object, with optional param.

        @param full: default True. By default, print the full data structure. 
            Set to False to print tweets using simplified format.
        """
        super(tweepy.streaming.StreamListener, self).__init__()
        self.full = full

    def output(self, jsonData):
        """
        Format JSON tweet data for output.
        """
        if jsonData.keys() == ['limit']:
            # The request succeeds but we get a limit error message instead of 
            # a tweet object. This is seems to be a soft limit since the next
            # response we get is a normal tweet object.
            print('\n==========limit hit=============\n')
            # Sleep to make sure we don't hit a hard rate limit.
            time.sleep(10)
        else:
            if self.full:
                print(json.dumps(jsonData, indent=4))
            else:
                # At this point data could be sent to a tweet processor
                # method to extract values and then insert in database.

                # Make string unicode to avoid UnicodeEncodeError for certain
                # ASCII characters.
                print(u'{0} -- {1} \n'.format(
                        jsonData['user']['screen_name'],
                        jsonData['text'].replace('\n', '<br>')
                        )
                    )
            # If this is not set, or at 1 second, then we seem to get a limit
            # response occasionally, instead of a tweet (though the connection 
            # continues).
            time.sleep(3)

    def on_data(self, strData):
        jsonData = json.loads(strData)
        self.output(jsonData)
        return True

    def on_error(self, status):
        # This was recommended in tweepy docs.
        if status == 420:
            # Disconnect the stream on rate limiting.
            return False
        print(status)


def limitHandled(cursor):
    """
    Function to handle Twitter API rate limiting when cursoring through items.

    Since cursors raise RateLimitErrors in their next() method, handling 
    them can be done by wrapping the cursor in an iterator.

    @param: cursor: tweepy Cursor items list.
        Usage: 
            for x in limitHandled(tweepy.Cursor(api.followers).items()):
                print x

    @return: None
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError as e:
            print('Sleeping 15 min. {0}'.format(str(e)))
            time.sleep(15 * 60)


def generateToken(userToken=False):
    """
    Generate a Twitter API access token using configured Twitter app
    credentials.
    """
    # Get access token.
    auth = tweepy.OAuthHandler(conf.get('TwitterAuth', 'consumerKey'),
                               conf.get('TwitterAuth', 'consumerSecret'))

    if userToken:
        print('Authorise Twitterverse to have access to your data.')
        authURL = auth.get_authorization_url()
        print(authURL)

        # Open in browser
        webbrowser.open(authURL)
        print()

        userPin = raw_input('Enter your pin (or "quit"). /> ')
        if not userPin or userPin.lower() in ('q', 'quit', 'exit'):
            print('Exiting.')
            exit(0)

        auth.get_access_token(userPin)
    else:
        auth.set_access_token(conf.get('TwitterAuth', 'accessKey'),
                              conf.get('TwitterAuth', 'accessSecret'))
    return auth


def getStreamConnection(auth, full=True):
    """
    Expects terms as a list of strings.

    Make auth optional by generating app token if auth object is not specified.

    Use spaces to use AND phrases and commas for OR phrases.
        e.g. 'the twitter' => 'the AND twitter'
        e.g. 'the,twitter' => 'the OR twitter'
    Usage:
        >>> terms = ['abc,def', 'xyz']
        >>> stream = streamConnection(auth)
        >>> stream.filter(track=terms)
    """
    if not auth:
        auth = generateToken()

    listener = _StdOutListener(full)
    stream = tweepy.Stream(auth, listener)
    
    return stream


def getAPIConnection(auth=None):
    """
    Make auth optional by generating app token if auth object is not specified.
    """
    if not auth:
        auth = generateToken()

    # Construct the API instance.
    api = tweepy.API(auth)

    return api


def _test():
    args = sys.argv[1:]
    # Opt for authentication with user token instead of app token.
    if args and args[0] in ('-u', '--user'):
        userFlow = True
        args.pop(0)
    else:
        userFlow = False

    auth = generateToken(userFlow)
    api = getAPIConnection(auth)

    ## Test REST API.

    # If the authentication was successful, you should see the name of your 
    # account print out.
    me = api.me()
    #print(me)
    print('You are authenticated as {0}.'.format(me.name))
    print()

    ## Test streaming API.

    if args and args[0] in ('-s', '--stream'):
        args.pop(0)
        stream = getStreamConnection(auth, full=False)
        # Use remaining arguments as list of input terms.
        # See docs dir for AND / OR rules of stream searches.
        if not args:
            raise ValueError('Require at least one search item to stream.')

        # Transform args split to work with tweepy. Spaces on either side
        # of commas are optional and have no effect.
        # e.g.
        #   $ python filename.py -s abc def,ABC DEF, xyz 
        #   => ['abc def', 'ABC DEF', 'xyz']
        #   => which means
        #       ('abc' and 'def' in one tweet in any order) or 
        #       ('ABC' and 'DEF' in one tweet in any order) or
        #       ('xyz')
        argsStr = ' '.join(args)
        track = argsStr.split(',')
        track = [x.strip() for x in track]

        print('Starting stream...')
        print(track)
        print()

        # Require more testing.
        # Not enough volume to see if these args actually work as the
        # stream seemed to not pick up anything.
        #languages='en'
        #filter_level='medium'
        stream.filter(track=track)

if __name__ == '__main__': 
    _test()
