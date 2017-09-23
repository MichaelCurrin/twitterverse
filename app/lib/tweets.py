# -*- coding: utf-8 -*-
"""
Tweets lib application file.

Interfaces with the tweet-related table in the database. See the tweets file
in models dir.

These are the overall steps, which can be automated:
 1. Start with a Twitter screen name or screen names, read as
    list in the command-line arguments or read from a text file.
 2. Get the Profile data for the users and store in the database, either
    creating the record or updating if record exists in Profile table.
 3. Get tweets from the timeline of the user and store in Tweets table, with
    link back to the Profile record. Repeat for all profiles of interest.
"""
import json
import math
import pytz

from sqlobject.dberrors import DuplicateEntryError
import tweepy
from tweepy.error import TweepError

from lib import database as db
from lib.twitter import auth


def getProfile(APIConn, screenName=None, userID=None):
    """
    Get data of one profile from the Twitter API, for a specified user.

    Either screenName string or userID integer must be specified, but not both.

    @param APIConn: authenticated API connection object.
    @param screenName: Default None. The name of Twitter user to fetch, as
        a string.
    @param userID: Default None. The ID of the Twitter user to fetch, as an
        integer.

    @return profile: tweepy profile object of requested user.
    """
    print 'Fetching user: {0}'.format(screenName if screenName else userID)

    assert screenName or userID, 'Expected either screenName (str) or userID'\
        '(int) to be set.'
    assert not (screenName and userID), 'Cannot set both screenName and userID.'

    params = {}
    if screenName:
        params['screen_name'] = screenName
    else:
        params['user_id'] = userID

    profile = APIConn.get_user(**params)

    return profile


def insertOrUpdateProfile(fetchedProfile):
    """
    Insert record in Profile table or update existing record if it exists.

    @param fetchedProfile: single profile, as tweepy profile object fetched from
        the Twitter API.

    @return profileRec: single profile, as SQLObject record in Profile table.
    """
    data = {
        'guid':           fetchedProfile.id,
        'screenName':     fetchedProfile.screen_name,
        'name':           fetchedProfile.name,
        'description':    fetchedProfile.description,
        'location':       fetchedProfile.location,
        'imageUrl':       fetchedProfile.profile_image_url_https,
        'followersCount': fetchedProfile.followers_count,
        'statusesCount':  fetchedProfile.statuses_count,
        'verified':       fetchedProfile.verified,
    }
    try:
        # Attempt to insert new row, assuming GUID or screenName do not exist.
        profileRec = db.Profile(**data)
    except DuplicateEntryError:
        profileRec = db.Profile.byGuid(data['guid'])
        data.pop('guid')
        # Replace values in existing record with those fetched from Twitter API,
        # assuming all values except the GUID can change.
        profileRec.set(**data)

    return profileRec


def insertOrUpdateProfileBatch(screenNames):
    """
    Get Twitter profile data from the Twitter API and store in the database.

    Profile records are created, or updated if they already exist.

    @param screenNames: list of user screen names as strings, to be fetched from
        the Twitter API.

    @return: None
    """
    APIConn = auth.getAPIConnection()

    for s in screenNames:
        try:
            fetchedProf = getProfile(APIConn, screenName=s)
        except TweepError as e:
            # The profile could be missing or suspended, so we log it
            # and then skip inserting or updating (since we have no data).
            print u'Could not fetch user: `{0}`. {1}. {2}'.format(
                s, type(e).__name__, str(e)
            )
        else:
            try:
                localProf = insertOrUpdateProfile(fetchedProf)
                # Represent log of followers count visually as repeated stars.
                followersStars = '*' * int(math.log10(localProf.followersCount))
                print u'Inserted/updated user: {0:20} - {1}'\
                    .format(localProf.screenName, followersStars)
            except StandardError as e:
                print u'Could not insert/update user: `{0}`. {1}. {2}'.format(
                    fetchedProf.screen_name, type(e).__name__, str(e)
                )


def getTweets(APIConn, screenName=None, userID=None, tweetsPerPage=200,
              pageLimit=1):
    """
    Get tweets of one profile from the Twitter API, for a specified user.

    Either screenName string or userID integer must be specified, but not both.
    The result of (tweetsPerPage)*(pageLimit) indicates the total number
    of tweets requested from the API on calling this function.

    @param APIConn: authenticated API connection object.
    @param screenName: Default None. The name of Twitter user to fetch, as
        a string.
    @param userID: Default None. The ID of the Twitter user to fetch, as an
        integer.
    @param tweetsPerPage: Default 200. Count of tweets to get on a page.
        The API''s limit is 200 tweets, but a lower value can be used.
        The `pageLimit` argument can be used to do additional calls
        to get tweets above the 200 limit - see `tweepy.Cursor` method.
    @param pageLimit: Default 1. Number of pages of tweets to get by doing
        a sequence of queries with a cursor. The number of tweets
        on each page is determined by `tweetsPerPage` argument.

    @return tweetsList: list of tweepy tweet objects for the requested user.
    """
    print 'Fetching tweets for user: {0}'.format(screenName if screenName
                                                 else userID)

    assert screenName or userID, 'Expected either screenName (str) or userID'\
        '(int) to be set.'
    assert not (screenName and userID), 'Cannot request both screenName and'\
                                        ' userID.'

    params = {'count': tweetsPerPage}
    if screenName:
        params['screen_name'] = screenName
    else:
        params['user_id'] = userID

    if pageLimit == 1:
        # Do a simple query without paging.
        tweets = APIConn.user_timeline(**params)
    else:
        tweets = []
        # Send the request parameters to Cursor object, with the page limit.
        for page in tweepy.Cursor(APIConn.user_timeline, **params)\
                .pages(pageLimit):
            tweets.extend(page)

    return tweets


def insertOrUpdateTweet(fetchedTweet, profileID, writeToDB=True):
    """
    Insert or update one record in the Tweet table.

    TODO: Write function to just update the fav and RT counts for an
        existing tweet. That would be useful for updating tweets which
        would not be updated when we get the most recent 200 for a user.
        However, this is a low priority as we expect most engagements
        within a day or two of tweet being posted.

    @param fetchedTweet: single tweet, as tweepy tweet object, as fetched from
        the Twitter API.
    @param profileID: The ID of the tweet's author, as an integer from
        the Profile ID column in the local db. This is used to set
        the Tweet object's foreign key.
    @param writeToDB: Default True. If True, write the fetched tweets
        to local database, otherwise print and discard them.

    @return data: Tweet attributes which were sent to a record in the
        database.
    """
    # Tweepy has already created a datetime string into a datetime object
    # for us, but it is unaware of the timezone. We know that the timezone
    # is always given as UTC+0000 regardless of where the tweet was made,
    # so we can set the tzinfo.
    awareTime = fetchedTweet.created_at.replace(tzinfo=pytz.UTC)

    data = {
        'guid':                 fetchedTweet.id,
        'profileID':            profileID,
        'createdAt':            awareTime,
        'message':              fetchedTweet.text,
        'favoriteCount':        fetchedTweet.favorite_count,
        'retweetCount':         fetchedTweet.retweet_count,
        'inReplyToTweetGuid':   fetchedTweet.in_reply_to_status_id,
        'inReplyToProfileGuid': fetchedTweet.in_reply_to_user_id,
    }
    if writeToDB:
        try:
            # Attempt to insert new row, assuming GUID does not exist.
            tweetRec = db.Tweet(**data)
        except DuplicateEntryError:
            tweetRec = db.Tweet.byGuid(data['guid'])
            # Update engagement stats on existing tweet, assuming other values
            # cannot change.
            tweetRec.set(favoriteCount=fetchedTweet.favorite_count,
                         retweetCount=fetchedTweet.retweet_count)

    return data


def insertOrUpdateTweetBatch(profileRecs, tweetsPerProfile=200, verbose=False,
                             writeToDB=True, acceptLang=['en', 'und']):
    """
    Get Twitter tweet data from the Twitter API for a batch of profiles
    and store their tweets in the database.

    The verbose and writeToDB flags can be used together to print tweet
    data which would be inserted into the database without actually inserting
    it. This can be used preview tweet data without increasing storage or using
    time to do inserts and updates.

    TODO: Write function to look up list of tweet IDs and then insert or update
        in local db. See tweepy's API.statuses_lookup docs. This can
        be used to update tweets not updated recently.

    @param profileRecs: list of Profile objects, to create or update
        tweets for. This might be a list from the Profile table which
        has been filtered based on a job schedule, or Profiles which
        match criteria such as high follower count.
    @param tweetsPerProfile: Default 200. Count of tweets to get for each
        profile, as an integer. If this is 200 or less, then page limit is
        left at 1 and the items per page count is reduced. If this is
        more than 200, then the items per page count is left at 200
        and page limit is adjusted to get a number of tweets as the
        next multiple of 200.
        e.g. 550 tweets needs 2 pages to get the first 400 tweets,
            plus a 3rd page to the additional 150 tweets.
            We simplify to get 200*3 = 600 tweets, to keep the count
            consistent on each query.

        Note that even if 200 tweets are requested, the API sometimes returns
        only 199 and the user may have posted fewer than the requested tweets.

        The limit for a single request to the API is 200, therefore any
        number up to 200 has the same rate limit cost. It may be useful to set
        a number here as 200 or less if we want to get through all the users
        quickly, as this takes fewer API queries and fewer db inserts
        or updates. Also, consider that a very low number may lead to deadtime,
        where the script is not processing tweets in the database but
        just waiting for the next rate limited window.
    @param verbose: Default False. If True, print the data used to created
        a local Tweet record. This data can be printed regardless of whether
        the data is written to the db record or not.
    @param writeToD: Default True. If True, write the fetched tweets
        to local database, otherwise print and discard them. This is useful
        when used in combination with verbose flag which prints the data.
    @param acceptLang: List of language codes. Only store tweet if their
        language property is in this list. See Twitter API's documentation for
        languages. Defaults to list with 'en' item for English and 'und'
        for undefined. Set to None to accept all languages.

    @return: None
    """
    APIConn = auth.getAPIConnection()

    if tweetsPerProfile <= 200:
        tweetsPerPage = tweetsPerProfile
        pageLimit = 1
    else:
        tweetsPerPage = 200
        # If tweetsPerProfile is not a multiple of tweetsPerPage, then we
        # have to add 1 page to the floor division calculation.
        remainderPage = 1 if tweetsPerProfile % tweetsPerPage else 0
        pageLimit = tweetsPerProfile / tweetsPerPage + remainderPage

    for p in profileRecs:
        try:
            fetchedTweets = getTweets(APIConn, userID=p.guid,
                                      tweetsPerPage=tweetsPerPage,
                                      pageLimit=pageLimit)
        except TweepError as e:
            print u'Could not fetch tweets for user: `{0}`. {1}. {2}'.format(
                p.screenName, type(e).__name__, str(e)
            )
        else:
            print u'User: {0}'.format(p.screenName)

            if writeToDB:
                print 'Inserting/updating tweets in db...'
            else:
                print 'Displaying tweets but not inserting/updating...'

            added = errors = skipped = 0
            for f in fetchedTweets:
                if acceptLang is None or f.lang in acceptLang:
                    try:
                        # On return, we get data dict used for the record.
                        # We do not get the record itself.
                        tweetData = insertOrUpdateTweet(f, profileID=p.id)
                        if verbose:
                            # Make createdAt value a string for JSON output.
                            tweetData['createdAt'] = str(tweetData['createdAt'])
                            print json.dumps(tweetData, indent=4)
                        added += 1
                    except Exception as e:
                        print u'Could not insert/update tweet `{0}` for user'\
                            ' `{1}`. {2}. {3}'.format(
                                f.id, p.screenName, type(e).__name__, str(e)
                            )
                        errors += 1
                else:
                    print 'Skipping tweet. Lang: {0}'.format(f.lang)
                    skipped += 1

                total = sum(added, errors, skipped)
                # Print stats on every 10 processed and on the last item.
                if total % 10 == 0 or f == fetchedTweets[-1]:
                    print 'Total: {0:2,d}. Added: {1:2,d}.'\
                          ' Errors: {2:2,d}. Skipped: {3:2,d}.'\
                          .format(total, added, errors, skipped)
