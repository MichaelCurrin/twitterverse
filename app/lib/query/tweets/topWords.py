# -*- coding: utf-8 -*-
"""
Top words application file.

Search through messages of tweets in the database, the words and print out
the occurence of each word. Characters are removed, but the hashtag (#)
and mention (@) symbols are kept.

Functions are made available for imports but this script can also be run
directly.

Usage:
    $ python -m lib.query.tweets.topWords --help
"""
import argparse
import re
from collections import Counter

from lib import database as db


# TODO
# Consider limiting items in print functions to v above threshold count only.
# Or limiting the count of keys on the output.


def printCounterByCount(counter):
    """
    Pretty print data of a Counter instance, ordered by count descending.

    @param counter: A collections.Count instance.

    @return None
    """
    for k, v in counter.most_common():
        print k, v


def printCounterByKey(counter):
    """
    Pretty print data of a Counter instance, ordered by keys.

    Not necessarily alphabetical.

    @param counter: A collections.Count instance.

    @return None
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


def printHashtagsAndMentions(tweetLimit=0, searchText=None, filter=False):
    """
    Print reports on the unique terms in Tweet sample, broken down into
    headings as 'Summary', 'Hashtags' and 'Mentions'.

    @param tweetLimit: Count of Tweets records to get, using class's
        default ordering by most recent. The limit defaults to zero,
        which gets all Tweets.
    @searchText: Optional text phrase to search. Filter Tweet to those
        which have a message that contains this phrase. This case insensitive,
        at least in the SQLite implementation of this project.
        We filter using .contains on the Tweet message attribute. Since
        in sqlbuilder.py that calls .CONTAINSSTRING, which is a wrapper
        on .LIKE that uses the SQL `LIKE` statement.

    @return None
    """
    tweets = db.Tweet.select()
    if searchText is not None:
        tweets = tweets.filter(db.Tweet.q.message.contains(searchText))
    tweets = tweets.limit(tweetLimit)

    hashtags, mentions, plain = getHashtagsAndMentions(tweets)

    ###
    # FILTER HERE
    ###

    # Unique word count for each area.
    hashtagWC = len(hashtags)
    mentionWC = len(mentions)
    plainWC = len(plain)

    print 'Summary'
    print '=============='
    # Count items in the sliced selection since .count() does not work with
    # a limit.
    count = len(list(tweets)) if tweetLimit else tweets.count()
    print "{0:7,d} tweets".format(count)
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

def main():
    """
    Function for executing command-line arguments.

    TODO: Filter tweets by date range or Campaign, or Profile Category
    Consider how that logic would be used in a utility or
    larger application before making it here without a good case to use it.
    """
    parser = argparse.ArgumentParser(description="Print the unique terms"
                                     " in messages across tweets in the db.")
    parser.add_argument(
        'limit',
        type=int,
        help="""Max count of tweets to select, ordered by most recent
            post time. The terms will be derived from this sample of tweets.
            Set as 0 to use all tweets in the db."""
    )
    parser.add_argument(
        '-s', '--search',
        metavar='PHRASE',
        help="""Text phrase. If supplied, filter the Tweet records to
            those which contain input PHRASE in their message text,
            ignoring case. Enclose the argument in single quotes to
            escape a hashtag or to include spaces."""
    )
    parser.add_argument(
        '-f', '--filter',
        action='store_true',
        help="""If supplied, filter the output unique terms to only those which
            contain the input term. This will tend to provide much shorter
            lists, but is useful for identifying hashtags or handles which
            are similar because they share a common string."""
    )

    args = parser.parse_args()

    printHashtagsAndMentions(
        tweetLimit=args.limit,
        searchText=args.search,
        filter=args.filter
    )


if __name__ == '__main__':
    main()
