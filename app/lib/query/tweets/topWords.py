# -*- coding: utf-8 -*-
"""
Top words application file.

Search through messages of tweets in the database, the words and print out
the occurence of each word. Characters are removed, but the hashtag (#)
and mention (@) symbols are kept.
"""
import re
import sys
from collections import Counter

from lib import database as db


# TODO
# Consider limiting printing to above threshold count only.
# Or limiting the count of terms on the output.


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
    Get the unique terms across the text in received tweets and output as
    three groups.

    Note on regex:
        The simple approach would be to split on '\W' (non-words,
        e.g. punctuation), as that leaves us with '\w' (words). But
        we want to keep the '#' since we are working with Twitter data.
        So we use '^' to do inverse of everything in hard brackets,
        which is the hash and the words. i.e. we split on non-word
        characters EXCLUDING #.
        Similarly, the '@' is added to the pattern to keep it in words.
        We that if '#'' or '@'' are used in the middle of a word rather than
        that start, that those symbols act as delimiters to split the word.
        As this is likely how Twitter perceives the terms.

    @param tweets: A list of Tweet objects. We iterate through the tweets
        and the words in each tweet, to count the terms.

    @return hashtags: counter object, including unique terms starting with '#'
        and count of occurrences of each term across the received tweets.
    @return mentions: counter object, including unique terms starting with '@'
        and count of occurrences of each term across the received tweets.
    @return plain: counter object, including unique terms which do not
        contain '#' or '@' and a count of occurrences of each term across
        the received tweets.
    """
    hashtags = Counter()
    mentions = Counter()
    plain = Counter()

    # TODO: check out how \w matches punctuation - are words split on
    # apostrophes? What about "can't" vs "I said 'hello'"?
    pattern = re.compile('[^#@\w]+')
    for t in tweets:
        # Use filter to remove empty strings in the list, caused by line breaks
        # or a sequence of punctuation.
        words = filter(None, re.split(pattern, t.message))
        for word in words:
            # Add 1 to the count for that word for the appropriate Counter.
            if word.startswith('#'):
                hashtags.update({word: 1})
            elif word.startswith('@'):
                mentions.update({word: 1})
            else:
                # TODO: apply nltk.corpus.stopwords.words() here,
                # across languages. Consider that the stopwords cut off before
                # apotrophe, therefore check if the word starts with.
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


def main(args):
    """
    Function for executing command-line arguments.
    """
    if not args or set(args) & set(('-h', '--help')):
        print """\
Print the unique terms for most recent N tweets in the Tweet table.

Usage:
$ python -m lib.query.tweets.topWords [LIMIT N] [-h|--help]

Options and arguments:
--help : Show this help message and exit.
LIMIT  : Count of tweets to get. Set as 0 to get all.
"""
    else:
        limit = int(args[0]) if args else 1
        printHashtagsAndMentions(limit)


if __name__ == '__main__':
    main(sys.argv[1:])
