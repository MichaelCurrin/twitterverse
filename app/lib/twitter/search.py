# -*- coding: utf-8 -*-
"""
Search Tweets application file.

Search for tweets in the Twitter API based on a query string and return the
tweepy tweet objects, which have an author attribute.

Results are limited to about 7 days back from the current date, regardless
of count or possible date values set.
The limit is covered here:
    https://developer.twitter.com/en/docs/tweets/search/overview

Query syntax:
    - See Twitter's documentation on search query syntax here:
        https://developer.twitter.com/en/docs/tweets/rules-and-filtering/guides/using-premium-operators
    - Note that combining terms is different between REST API and Streaming API.
      Here, in the REST API, terms are implictly ANDed together, but 'OR'
      can be used. There does not appear to be a limit on the length
      of the query or number of terms.
    - Symbols like @ or # can be used at the start of terms, but this will
      be give fewer tweets than searching without the symbols, so consider
      if they make sense.
    - Double quotes can be used to enclose words as an exact match phrase,
      but quotes sentences must appear at the start of the search query to
      avoid getting zero results overall. This is a known bug on Twitter API.
    - Examples:
        * 'wordA wordB wordC' => search for tweets containing all 3 words,
            in any order.
        * 'wordA OR #wordB OR wordC' => search for tweets containing any of
            the 3 words.
        * '@handleA OR wordB' => search for tweets about either term.
        * '"Welcome home" OR "Good luck" OR wordC' => search for terms
            about either of the quoted phrases or wordC

Note that the tweepy.Cursor approach has known memory leak issues.
It has been recommended to use a while loop with max or since ID values
instead. This may be necessary for high volume queries only, so the
Cursor approach is used here for now until that becomes an issue.
- https://stackoverflow.com/questions/22469713/managing-tweepy-api-search/22473254#22473254
- https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
"""
import datetime
import logging

import tweepy


logger = logging.getLogger("lib.twitter.search")


def getSearchQueryHelp(argName='--query'):
    """
    Return help text, as a guide for search queries which can be safely
    entered on the command-line and conform to the Twitter Search API rules.
    See search.py docstring for more info.

    Multiple words could technically be entered without quotes and joined
    and as hashtag or double quotes could be escaped with a backslash.
    But it is simplest to always expect it the input already as a single
    quoted string, rather than as a list.

    @param argName: Name of argument to be inserted into the output template,
        based on where the help is shown to the user.

    @return: Help text as string, with argName substituted in.
    """
    return """\
Note that text with multiple words, double quotes or a hashtag symbol
must be inside a quoted string, as show below.

Examples:
    single term
        {0} wordA
        {0} '#abc'

    AND terms, without applying order
        {0} 'wordA wordB wordC wordD'
        {0} 'to:handleA wordA'
        {0} 'from:handleA wordA'

    OR terms
        {0} 'wordA OR wordB'
        {0} '#def OR xyz OR #ghi'

    Exclusion
        {0} 'wordA -wordB'

    AND on groupings
        {0} '(wordA OR wordB) (wordC OR house)'
        {0} '(wordA OR wordB) -(wordC OR wordD OR wordE)'

    Exact match
        {0} '"My Quote"'
        {0} '"My Quote" OR "Another quote" OR wordC'

Note that for the last case, double-quoted phrases must be *before*
ordinary terms, due to a known Twitter Search API bug.

When combing AND and OR functionality in a single rule, AND logic is
evaluated first, such that 'wordA OR wordB wordC' is equivalent to
'wordA OR (wordB wordC)'. Though, braces are preferred for readability.
    """.format(argName)


def fetchTweetsPaging(APIConn, searchQuery, pageCount=1, extended=True):
    """
    Search for tweets in Twitter API and store in the database.

    Though the Cursor object is a generator, it is fine to add generator on top
    of it, even using a conditional statement if necessary.
    See https://pybit.es/generators.html in their Cursor example.

    The Cursor object here is wrapped in a generator so that the duration for
    each query request can be logged. We set the current time before looping
    back to the start of the for loop where the query is done. Note that
    any time between the yield statement and setting of queryStartTime is
    ignored, meaning the duration logged is for the request alone and excludes
    time to process the data.

    @param APIConn: authorised API connection.
    @param searchQuery: tweet text to search, following Twitter REST API search
        format, as string.
    @param pageCount: Count pages of tweets to fetch. Each page contains 100
        tweets, which is the Search API's limit.
    @param extended: If True, get the expanded tweet message instead of the
        truncated form.

    @return: tweepy Cursor object. Iterate of over this to do a query for a
        page of 100 tweets and return the page as a list of tweets objects
        in the current iteration.
    """
    logger.info("Starting Search query.")

    params = {'tweet_mode': 'extended'} if extended else {}

    cursor = tweepy.Cursor(
        APIConn.search,
        q=searchQuery,
        count=100,
        **params
    ).pages(pageCount)

    start = datetime.datetime.now()
    queryStartTime = start

    for page in cursor:
        splitTime = datetime.datetime.now() - queryStartTime
        logger.info("Retrieved page of search tweets. Duration: {0:3.2f}s."
                     .format(splitTime.total_seconds()))
        yield page
        queryStartTime = datetime.datetime.now()
