# -*- coding: utf-8 -*-
"""
Search Tweets application file.

Search for tweets in the Twitter API based on a query string and return them.
Results are limited to about 7 days back from the current date, regardless
of count or possible date values set.
The limit is covered here: https://developer.twitter.com/en/docs/tweets/search/overview

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


Language can be set as a query parameter before the search is started.
Unfortunately while English can be filtered in 'en', undefined
cannot be filtered by supplying 'und'. Therefore the language of tweets
should be filtered out after the search is complete, to catch the widest
range of English tweets. Since users who speak English could leave their
language as not set in the preferences.
See https://twittercommunity.com/t/language-attribute-lang-and-retweets/14573

Use extended mode to stop text from being truncated. Note that the
response message attribute is `.full_text` and not `.text`.
See https://twittercommunity.com/t/retrieve-full-tweet-when-truncated-non-retweet/75542/4

Note that the tweepy.Cursor approach has known memory leak issues.
It has been recommended to use a while loop with max or since ID values
instead. This may be necessary for high volume queries only, so the
Cursor approach is used here for now.
- https://stackoverflow.com/questions/22469713/managing-tweepy-api-search/22473254#22473254
- https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./
"""
import tweepy


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


def fetchTweets(APIConn, searchQuery, count=100, lang=['en']):
    """
    Do a basic search for up to 100 tweets with text matching a query string.

    There is no benefit to using this simple function over the one below
    which has paging.

    @param APIConn: authorised API connection.
    @param searchQuery: tweet text to search, following Twitter REST API search
        format, as string.
    @param count: Number of tweets to get. The API limit is max 100 in
        a single query, otherwise paging must be used - see other
        functions in this script.
    @param lang: Language codes to filter by, as list of strings.
        Defaults to English only. Set to None to use all languages.

    @return tweetSearch: list of tweepy tweet objects, only including
        those matching the language argument list or undefined, if lang
        argument was not None.
    """
    assert count <= 100, "Expected count of 100 or below for simple"\
        " fetchTweets function, but got {0}.".format(count)

    tweetSearch = APIConn.search(
        q=searchQuery,
        count=count,
    )

    if lang:
        # Include undefined language.
        lang.extend(['und'])

        return map(lambda t: t.lang in lang, tweetSearch)
    else:
        return tweetSearch


def fetchTweetsPaging(APIConn, searchQuery, itemLimit=100, lang=['en']):
    """
    Search for tweets in Twitter API and store in the database.

    This approach is a variation of the fetchTweets function, as here we
    handle paging. It is not practical for memory usage to create a
    long list of tweets for the Cursor generator and only then iterate
    through them to store. So we implement our own generator on top of it.
    Based on implementation in this article https://pybit.es/generators.html
    it is fine to add generator logic on top of the Cursor.

    Based on my own testing, using cursor.items(300) is only efficient
    as cursor.pages(3) in terms of number of queries if needed if the
    count for the first one is set to 100 (get 100 items per page).
    And if the items(N) method has N less than 100, only N tweets
    will be returned (even if the full 100 might be fetched, which
    is no additional rate limit cost).

    @param APIConn: authorised API connection.
    @param searchQuery: tweet text to search, following Twitter REST API search
        format, as string.
    @param itemLimit: Number of tweets to get. The API limit is max 100 in
        a single query, otherwise paging will be used.
    @param lang: Language codes to filter by, as list of strings.
        Defaults to English only. Set to None to include all languages.

    @return: generator of tweepy tweet objects, only including those
        matching the language argument list or undefined.
    """
    # Include undefined language.
    if lang:
        lang.extend(['und'])

    cursor = tweepy.Cursor(
        APIConn.search,
        count=100,
        q=searchQuery,
    )

    for t in cursor.items(itemLimit):
        if lang is None or t.lang in lang:
            yield t
