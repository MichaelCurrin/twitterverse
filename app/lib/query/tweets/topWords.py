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
# Consider limiting items in print functions to v above threshold count only.
# Or limiting the count of keys on the output.


def printCounterByCount(counter):
    """
    Pretty print data of a Counter instance, ordered by count descending.
    """
    for k, v in counter.most_common():
        print k, v


def printCounterByKey(counter):
    """
    Pretty print data of a Counter instance, ordered by keys.

    Not necessarily alphabetical.
    """
    for k in counter.keys():
        print k, counter[k]


def getHashtagsAndMentions(tweets):
    """
    Get the unique terms across the text in received tweets and output as
    three groups.

    We separate words in sentences using regex. We split words by
    any characters which are not #, @, alphanumeric, single or
    double quotes or a hyphen. Essentially we split by remaining
    punctuation and white spaces. Though by keeping hyphen in words,
    we still end up with standalone hyphens in the list which originally
    had white space on either side.

    We use + in the pattern to greedily match multiple split characters
    in a sequence, so we get a list of fewer null strings.

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

    pattern = re.compile(r"[^#@\w'-]+")

    for t in tweets:
        words = pattern.split(t.message)
        for word in words:
            # Ignore null strings caused by split characters at the end of a
            # message and remove standalone hyphens.
            if word and not word.startswith('-'):
                # Increment count for the word in the Counter.
                if word.startswith('#'):
                    hashtags.update({word: 1})
                elif word.startswith('@'):
                    mentions.update({word: 1})
                else:
                    # TODO: apply nltk.corpus.stopwords.words() here,
                    # across languages. Consider that the stopwords cut off
                    # before apostrophe, therefore check if the word
                    # starts with the stopword.
                    plain.update({word: 1})

    return hashtags, mentions, plain


def printHashtagsAndMentions(tweetLimit=0, searchText=None):
    tweets = db.Tweet.select()
    if searchText is not None:
        tweets = tweets.filter(db.Tweet.q.message.contains(searchText))
    tweets = tweets.limit(tweetLimit)

    hashtags, mentions, plain = getHashtagsAndMentions(tweets)

    # Unique word count for each area.
    hashtagWC = len(hashtags)
    mentionWC = len(mentions)
    plainWC = len(plain)

    print 'Summary'
    print '=============='
    print "{0:7,d} tweets".format(tweets.count())
    print "{0:7,d} unique words".format(hashtagWC + mentionWC + plainWC)
    print "{0:7,d} unique hashtags".format(hashtagWC)
    print "{0:7,d} unique mentions".format(mentionWC)
    print "{0:7,d} unique plain words".format(plainWC)
    print

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
$ python -m lib.query.tweets.topWords [LIMIT N] [SEARCH_TERM] [-h|--help]

Options and arguments:
--help     : Show this help message and exit.
LIMIT      : Count of tweets to get. Set as 0 to get all.
SEARCH_TERM: If supplied, filter tweets containing this term.
             Only accepts # strings in the command-line if they are escaped
             or quoted. A term with spaces should be quoted.
"""
    else:
        limit = int(args[0])
        searchText = args[1] if len(args) > 1 else None
        printHashtagsAndMentions(limit, searchText)


if __name__ == '__main__':
    main(sys.argv[1:])
