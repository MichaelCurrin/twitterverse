# -*- coding: utf-8 -*-
"""
Streaming module.

Usage:
    $ python -m lib.twitter.streaming --help

This is not directly related to the tweet and trending part of the
Twitterverse package but it has been included anyway. Results are not
guaranteed due to rate limiting not being investigated fully.

This does not need any database setup like the rest of the project does.
You just need your Twitter credentials setup in app.local.conf config file
as per the installation instructions.

The scale of this app is not intended for an environment with
super fast server, database or internet connection, so it may never
be optimal for capturing all stream tweets. But it can be used for
reading a tweet every second or so safely, as a sample of the data.

Even still, this error occurs
    urllib3.exceptions.ProtocolError: ('Connection broken:
        IncompleteRead(0 bytes read, 512 more expected)',
            IncompleteRead(0 bytes read, 512 more expected))

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

    The Twitter Streaming API has rate limits, and prohibits too many
    connection attempts happening too quickly. It also prevents too many
    connections being made to it using the same authorization keys.
    Thankfully, tweepy takes care of these details for us, and we can
    focus on our program.

    The main thing that we have to be aware of is the queue of tweets
    that we’re processing. If we take too long to process tweets, they
    will start to get queued, and Twitter may disconnect us. This means
    that processing each tweet needs to be extremely fast.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import json
import sys
import time

import tweepy

import lib.text_handling
from lib.config import AppConf
from lib.twitter_api import authentication


appConf = AppConf()


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
        Initialize the standard out listener object, with optional param.

        Setup tweet count on the instance as 0. This is increment on each
        tweet encountered.

        The following are produced on dir(self)
            'keep_alive', 'on_connect', 'on_data', 'on_delete',
            'on_direct_message', 'on_disconnect', 'on_error', 'on_event',
            'on_exception', 'on_friends', 'on_limit', 'on_status',
            'on_timeout', 'on_warning', 'output'

        :param full: default True. By default, print the full data structure.
            Set to False to print tweets using simplified format.
        """
        super(_StdOutListener, self).__init__()
        self.full = full
        self.count = 0

    def output(self, jsonData):
        """
        Format JSON tweet data for output.
        """
        if 'limit' in list(jsonData.keys()):
            # The request succeeds but we get a limit error message instead of
            # a tweet object. This is seems to be a soft limit since the next
            # response we get is a normal tweet object rather than error
            # status.
            now = datetime.datetime.now()
            timestampSeconds = int(jsonData['limit']['timestamp_ms']) / 1000
            given = datetime.datetime.fromtimestamp(timestampSeconds)

            print(u'\n=======================\n')
            print(u'Limit info')
            print(u'----------')
            print(u'Now: {}'.format(str(now)))
            print(u'Given: {}'.format(str(given)))
            duration = int((now - given).total_seconds())
            print(u'Difference: {:,d}s'.format(duration))
            print()
            print(u'Raw response:')
            print(jsonData)
            print()
            print(u'\n=======================\n')

            # Sleep to make sure we don't hit a hard rate limit.
            time.sleep(10)
        else:
            if self.full:
                print(u'{0}'.format(json.dumps(jsonData, indent=4)))
            else:
                # At this point data could be sent to a tweet processor
                # method to extract values and then insert in database.

                # Make string unicode to avoid UnicodeEncodeError for certain
                # ASCII characters.
                print((u'{0} -- {1} \n'.format(
                    jsonData['user']['screen_name'],
                    lib.text_handling.flattenText(jsonData['text'])
                )
                ))
            # If this is not set, or less than 1 second, then we seem to get a
            # limit response occasionally, instead of a tweet
            # (though the connection continues). This requires further testing.
            # Waiting may also slow down the stream and mean tweets or missed
            # or the API breaks connection because we are listening to slowly.
            time.sleep(1)

    def on_data(self, strData):
        self.count += 1
        jsonData = json.loads(strData)
        self.output(jsonData)
        return True

    def on_error(self, status):
        # This was recommended in tweepy docs.
        print(status)
        if status == 420:
            # Disconnect the stream on rate limiting.
            return False


def getStreamConnection(authObj=None, full=True):
    """
    Create stream connection object and return it.

    Use spaces to use AND phrases and commas for OR phrases.
        e.g. 'the twitter' => 'the AND twitter'
        e.g. 'the,twitter' => 'the OR twitter'
    Usage:
        >>> terms = ['abc,def', 'xyz']
        >>> stream = streamConnection()
        >>> stream.filter(track=terms)
    """
    if not authObj:
        authObj = authentication._generateAppToken()

    listener = _StdOutListener(full)
    stream = tweepy.Stream(authObj, listener, async_=True)

    return stream


def startStream(track):
    """
    Start an API stream for the tracking input phrase.

    See docs dir for AND / OR rules of stream searches.

    For most of this project we want to get a tweepy.API object for doing
    requests with. But for the streaming API we just need a
    tweetpy.OAuthHandler object.

    """
    stream = getStreamConnection(full=False)

    print(u"Searching for: {}\n".format(track))
    print(u"Starting stream...\n")

    # This requires more testing.
    # Not enough volume to see if these args actually work as the
    # stream seemed to not pick up anything.
    # filter_level='medium'
    try:
        stream.filter(track=track)
    except KeyboardInterrupt:
        print(u"Closed stream.")
        print(u"Received {:,d} items in session".format(stream.listener.count))
        sys.exit(1)


def main(args):
    """
    Test streaming API using command-line arguments list of input terms.

    See docs dir for AND / OR rules of stream searches.

    Transform items split to work with tweepy. Spaces on either side
    of commas are optional and have no effect.
    e.g.
      $ python -m lib.twitter_api.streaming abc def,ABC DEF, xyz
      => ['abc def', 'MNO QRS', 'xyz']
      => which translates to
          match ('abc' and 'def' in one tweet in any order)
          or match ('MNO' and 'QRS' in one tweet in any order)
          or match ('xyz')
    """
    if not args or set(args) & {'-h', '--help'}:
        print('Usage: python -m lib.twitter_api.streaming [WORD, WORD, ...]')
        print('e.g. abc def, MNO QRS,xyz')
        print('      --> track: ("abc" and "def") or ("MNO" and "QRS")'
              ' or "xyz"')
        print()
    else:
        argsStr = ' '.join(args)
        track = argsStr.split(',')
        track = [x.strip() for x in track]

        startStream(track)


if __name__ == '__main__':
    main(sys.argv[1:])
