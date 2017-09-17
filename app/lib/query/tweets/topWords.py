# -*- coding: utf-8 -*-
"""
Top words application file.

Search through messages of tweets in the database, the words and print out
the occurence of each word. Characters are removed, but the hashtag (#)
and mention (@) symbols are kept.
"""
import re
from collections import Counter

from lib import database as db


# TODO
# Consider limiting printing to above threshold count only.


def printCounterByCount(counter):
    """
    Pretty print data of a Counter instance, ordered by count descending.
    """
    for k, v in counter.most_common():
        print k, v


def printCounterByKey(counter):
    """
    Pretty print data of a Counter instance, ordered by key.

    Not necessarily alphabetical.
    """
    for k in counter.keys():
        print k, counter[k]


def getHashtagsAndMentions(tweets):
    """
    The simple approach would be to split on '\W' (non-words, e.g. punctuation),
    as that leaves us with '\w' (words). But we want to keep the '#'
    since we are working with Twitter data. So we use '^' to do inverse
    of everything in hard brackets, which is the hash and the words.
        i.e. we split on non-word characters EXCLUDING #.

    Similarly, the '@' is added to the pattern to keep it in words.
    """
    hashtags = Counter()
    mentions = Counter()
    plain = Counter()

    pattern = re.compile('[^#@\w]+')
    for t in tweets:
        words = re.split(pattern, t.message)
        for word in words:
            # Add 1 to the count for that word for the appropriate Counter.
            if word.startswith('#'):
                hashtags.update({word: 1})
            elif word.startswith('@'):
                mentions.update({word: 1})
            else:
                plain.update({word: 1})

    return hashtags, mentions, plain


def printHashtagsAndMentions(tweetLimit=0):
    tweets = db.Tweet.select().limit(tweetLimit)

    hashtags, mentions, plain = getHashtagsAndMentions(tweets)

    print 'Hashtags'
    print '========'
    printCounterByCount(hashtags)
    print

    print 'Mentions'
    print '========'
    printCounterByCount(mentions)

    '''
    # Removal of stopwords and handling of URIs is needed to make this
    # useful.
    print 'Plain'
    print '========'
    printCounterByCount(plain)
    '''

printHashtagsAndMentions()
