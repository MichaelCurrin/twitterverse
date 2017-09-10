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
 3. Get tweet from the timeline of user and store in Tweets table, with link
    back to the Profile record. Repeat for watched users.
"""
import os
import sys

from sqlobject.dberrors import DuplicateEntryError
import tweepy
from tweepy.error import TweepError

# While experimenting with tables not yet imported into db script,
# use the tweets model file. The connection file also needs to be updated.
# from lib import database as db
from models import tweets as db
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


def insertOrUpdateProfile(profile):
    """
    Insert record in Profile table or update existing record if it exists.

    @param profile: tweepy profile object for one Twitter user.

    @return profileRec: SQLObject Profile table record.
    """
    data = {
        'guid': profile.id,
        'screenName': profile.screen_name,
        'name': profile.name,
        'description': profile.description,
        'location': profile.location,
        'imageUrl': profile.profile_image_url_https,
        'followersCount': profile.followers_count,
        'statusesCount': profile.statuses_count,
        'verified': profile.verified,
    }
    try:
        # Attempt to insert new row, assuming GUID or screenName do not exist.
        profileRec = db.Profile(**data)
    except DuplicateEntryError:
        profileRec = db.Profile.byGuid(data['guid'])
        data.pop('guid')
        # Replace values in existing record with those fetched from Twitter API.
        profileRec.set(**data)

    return profileRec


def insertOrUpdateProfileBatch(screenNames):
    """
    Get Twitter profile data from the Twitter API and store in the database.

    # TODO: Consider handling of printing of special chars.

    @param screenNames: list of user screen names as strings, to be fetched from
        the Twitter API then added or updated in the local database.

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
                print u'Inserted/updated user: `{0}`'\
                    .format(localProf.screenName)
            except StandardError as e:
                print u'Could not insert/update user: `{0}`. {1}. {2}'.format(
                    fetchedProf.screen_name, type(e).__name__, str(e)
                )


def getTweets(APIConn, screenName=None, userID=None, tweetsPerPage=200,
              pageLimit=1):
    """
    Get tweets of one profile from the Twitter API, for a specified user.

    Either screenName string or userID integer must be specified, but not both.
    Calculate (tweetsPerPage)*(pageLimit) to get total number of tweets
    requested from the API.

    @param APIConn: authenticated API connection object.
    @param screenName: Default None. The name of Twitter user to fetch, as
        a string.
    @param userID: Default None. The ID of the Twitter user to fetch, as an
        integer.
    @param tweetsPerPage: Default 200. Count of tweets to get on a page.
        The limit is 200 tweets, but a lower value can be used.
        The `pageLimit` argument can be used to get tweets above the 200 limit.
    @param pageLimit: Default 1. Number of pages of tweets to get by doing
        a sequence of queries with a cursor. Where the number of tweets
        on each page is determined by `tweetsPerPage`.

    @return tweetsList: list of tweepy tweet objects for the requested user.
    """
    print 'Fetching tweets for user: {0}'.format(screenName if screenName
                                                 else userID)

    assert screenName or userID, 'Expected either screenName (str) or userID'\
        '(int) to be set.'
    assert not (screenName and userID), 'Cannot set both screenName and userID.'

    params = {'count': tweetsPerPage}
    if screenName:
        params['screen_name'] = screenName
    else:
        params['user_id'] = userID

    if pageLimit == 1:
        tweets = APIConn.user_timeline(**params)
    else:
        tweets = []
        # Send the request and parameters to Cursor object, with page limit.
        for page in tweepy.Cursor(APIConn.user_timeline, **params)\
                .pages(pageLimit):
            tweets.extend(page)

    return tweets


def main(args):
    """
    Function to run when excecuting directly, fetching list of screen names,
    either from arguments list or read from a specified text file.

    @param args: command-line arguments as a list of strings. See
        the usage help message below.

    @return: None
    """
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage:'
        print '$ python -m lib.tweets [-f|--file FILEPATH] [SCREENNAME, ...]'\
            ' [-h|--help]'
        print
        print 'Options and arguments:'
        print '--help    : Show this help output.'
        print '--file    : Read in the following argument as path to text file,'
        print '            instead of expecting list of screen names.'
        print 'FILEPATH  : If used with --file flag, indicates the path to a'
        print '            text file, which has one screen name per row and no'
        print '            header or other data.'
        print 'SCREENNAME: Supply a list of one or more Twitter screen names'
        print '            to search for and add to the database. Cannot be'
        print '            used with the --file flag.'
    else:
        if args[0] in ('-f', '--file') and len(args) == 2:
            filename = args[1]

            assert os.access(filename, os.R_OK), 'Unable to read path `{0}`'\
                                                 .format(filename)
            # Read text file and split by newline characters.
            with open(filename, 'rb') as reader:
                screenNames = reader.read().splitlines()
        else:
            # We got no flags so we use the args list as screen names.
            screenNames = args

        insertOrUpdateProfileBatch(screenNames)


if __name__ == '__main__':
    main(sys.argv[1:])
