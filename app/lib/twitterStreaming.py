# -*- coding: utf-8 -*-
"""
Setup tweepy streaming.

This is not directly related to the tweet and trending part of the Twitterverse package but it has been included anyway. Results are not guaranteed due to rate limiting not being investigated fully.
Also, the scale of this app is not intended for an environment with super fast server, database or internet connection, so it may never be optimal for capturing all stream tweets. But it can be used for reading a tweet every second or so safely, as a sample of the data.

Even still, this error occurs
    urllib3.exceptions.ProtocolError: ('Connection broken: IncompleteRead(0 bytes read, 512 more expected)', IncompleteRead(0 bytes read, 512 more expected))


Fill in your Twitter app credentials in app.conf or app.local.conf as an
override.

http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
Using the streaming api has three steps -
    Create a class inheriting from StreamListener
    Using that class create a Stream object
    Connect to the Twitter API using the Stream.

Resources
    https://github.com/tweepy/tweepy/blob/master/examples/streaming.py
    https://dev.twitter.com/streaming/overview/connecting
    https://www.dataquest.io/blog/streaming-data-python/
        Rate limiting and other concerns

        The Twitter Streaming API has rate limits, and prohibits too many connection attempts happening too quickly. It also prevents too many connections being made to it using the same authorization keys. Thankfully, tweepy takes care of these details for us, and we can focus on our program.

        The main thing that we have to be aware of is the queue of tweets that we’re processing. If we take too long to process tweets, they will start to get queued, and Twitter may disconnect us. This means that processing each tweet needs to be extremely fast.
"""
import json
import os
import sys
import datetime
import time

import tweepy

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import twitterAuth
from lib.config import AppConf

appConf = AppConf()

count = 0

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

        The following are produced on dir(self)
            'keep_alive', 'on_connect', 'on_data', 'on_delete', 'on_direct_message', 'on_disconnect', 'on_error', 'on_event', 'on_exception', 'on_friends', 'on_limit', 'on_status', 'on_timeout', 'on_warning', 'output'

        @param full: default True. By default, print the full data structure.
            Set to False to print tweets using simplified format.
        """
        super(tweepy.streaming.StreamListener, self).__init__()
        self.full = full

    def output(self, jsonData):
        """
        Format JSON tweet data for output.
        """
        if 'limit' in jsonData.keys():
            # The request succeeds but we get a limit error message instead of
            # a tweet object. This is seems to be a soft limit since the next
            # response we get is a normal tweet object rather than error status.
            now = datetime.datetime.now()
            timestampSeconds = int(jsonData['limit']['timestamp_ms'])/1000
            given = datetime.datetime.fromtimestamp(timestampSeconds)

            print u'\n=======================\n'
            print u'Limit info'
            print u'----------'
            print u'Now: {}'.format(str(now))
            print u'Given: {}'.format(str(given))
            duration = int((now-given).total_seconds())
            print u'Difference: {:,d}s'.format(duration)
            print
            print u'Raw response:'
            print jsonData
            print
            print u'\n=======================\n'

            # Sleep to make sure we don't hit a hard rate limit.
            time.sleep(10)
        else:
            if self.full:
                print u'{0}'.format(json.dumps(jsonData, indent=4))
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
            time.sleep(1)

    def on_data(self, strData):
        global count
        count += 1
        jsonData = json.loads(strData)
        self.output(jsonData)
        return True

    def on_error(self, status):
        # This was recommended in tweepy docs.
        print status
        if status == 420:
            # Disconnect the stream on rate limiting.
            return False


def limitHandled(cursor):
    """
    Function to handle Twitter API rate limiting when cursoring through items.
    This is only needed if api object is setup with default value left as default wait_on_rate_limit_notify=False.

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
            print u'Sleeping 15 min. {0}'.format(str(e))
            time.sleep(15 * 60)


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
        auth = twitterAuth.generateAppToken()

    listener = _StdOutListener(full)
    stream = tweepy.Stream(auth, listener, async=True)

    return stream


def startStream(track):
    """
    See docs dir for AND / OR rules of stream searches.
    """
    auth = twitterAuth.generateAppToken()
    stream = getStreamConnection(auth, full=False)
    print u'Searching for: {}\n'.format(track)
    print u'Starting stream...\n'

    # This requires more testing.
    # Not enough volume to see if these args actually work as the
    # stream seemed to not pick up anything.
    #languages='en'
    #filter_level='medium'
    try:
        stream.filter(track=track)
    except KeyboardInterrupt as e:
        global count
        print u'\nClosing stream. Received {:,d} items in session'.format(count)
        exit(1)


def main(args):
    """
    Test streaming API using command-line arguments list of input terms.

    See docs dir for AND / OR rules of stream searches.

    Transform  items split to work with tweepy. Spaces on either side
    of commas are optional and have no effect.
    e.g.
      $ python script.py abc def,ABC DEF, xyz
      => ['abc def', 'MNO QRS', 'xyz']
      => which translates to
          ('abc' and 'def' in one tweet in any order) or
          ('MNO' and 'QRS' in one tweet in any order) or
          ('xyz')
    """
    if not args:
        print 'Usage: '
        print '$ python {} [words, words, ...]'.format(__file__)
        print
        print 'e.g.'
        print '$ python {} abc def, MNO QRS,xyz'.format(__file__)
        print '   --> track: ("abc" and "def") or ("MNO" and "QRS") or "xyz"'
        print
        return None

    argsStr = ' '.join(args)
    track = argsStr.split(',')
    track = [x.strip() for x in track]

    startStream(track)


if __name__ == '__main__':
    main(sys.argv[1:])