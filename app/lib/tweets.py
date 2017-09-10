# -*- coding: utf-8 -*-
"""
Tweets lib application file.

Interfaces with the tweet-related table in the database. See the tweets file
in models dir.

These are the overall steps, which can be automated:
 1. Start with a Twitter username or usernames, possibly read as usernames
    in the command-line arguments or read from a text file.
 2. Get the Profile data for the users and store in the database, either
    creating the record or updating if record exists in Profile table.
 3. Get tweet from the timeline of user and store in Tweets table, with link
    back to the Profile record. Repeat for watched users.
"""
import os
import sys

from sqlobject.dberrors import DuplicateEntryError
from tweepy.error import TweepError

# While experimenting with tables not yet imported into db script,
# use the tweets model file. The connection file also needs to be updated.
# from lib import database as db
from models import tweets as db
from lib.twitter import auth


def getProfile(APIConn, username=None, userID=None):
    """
    Get data of one profile from the Twitter API, for a specified user.

    Either username string or userID integer must be specified, but not both.

    @param APIConn: authenticated API connection object.
    @param username: Default None. The name of Twitter user to fetch, as
        a string.
    @param userID: Default None. The ID of the Twitter user to fetch, as an
        integer.

    @return profile: tweepy profile object of requested user.
    """
    print 'Fetching user: {0}'.format(username if username else userID)

    assert username or userID, 'Expected either username (str) or userID (int)'\
        ' to be set.'
    assert not (username and userID), 'Cannot set both username and userID.'

    params = {}
    if username:
        params['screen_name'] = username
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
        # Attempt to insert new row, assuming GUID or username do not exist.
        profileRec = db.Profile(**data)
    except DuplicateEntryError:
        profileRec = db.Profile.byGuid(data['guid'])
        data.pop('guid')
        # Replace values in existing record with those fetched from Twitter API.
        profileRec.set(**data)

    return profileRec


def getTweets():
    pass


def insertOrUpdateProfileBatch(usernames):
    """
    Get Twitter profile data from the Twitter API and store in the database.

    # TODO: Consider handling of printing of special chars.

    @param usernames: list of username as strings, to be fetched from
        the Twitter API then added or updated in the local database.

    @return: None
    """
    APIConn = auth.getAPIConnection()

    for u in usernames:
        try:
            fetchedProf = getProfile(APIConn, username=u)
        except TweepError as e:
            # The profile could be missing or suspended, so we log it
            # and then skip inserting or updating (since we have no data).
            print u'Could not fetch user: `{0}`. {1}. {2}'.format(
                u, type(e).__name__, str(e)
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


def main(args):
    """
    Function to run when excecuting directly, fetching list of usernames
    either from arguments list or read from a specified text file.

    @param args: command-line arguments as a list of strings. See
        the usage help message below.

    @return: None
    """
    if not args or set(args) & set(('-h', '--help')):
        print 'Usage:'
        print '$ python -m lib.tweets [-f|--file FILEPATH] [USERNAME, ...]'\
            ' [-h|--help]'
        print
        print 'Options and arguments:'
        print '--help  : Show this help output.'
        print '--file  : Read in the following argument as path to text file,'
        print '          instead of expecting list of usernames.'
        print 'FILEPATH: If used with --file flag, indicates the path to a'
        print '          text file, which has one username per row and no'
        print '          header or other data.'
        print 'USERNAME: Supply a list of one or more Twitter usernames'
        print '          to search for and add to the database. Cannot be'
        print '          used with the --file flag.'
    else:
        if args[0] in ('-f', '--file') and len(args) == 2:
            filename = args[1]

            assert os.access(filename, os.R_OK), 'Unable to read path `{0}`'\
                                                 .format(filename)
            # Read text file and split by newline characters.
            with open(filename, 'rb') as reader:
                usernames = reader.read().splitlines()
        else:
            # We got not flags so we use the args list as usernames.
            usernames = args

        insertOrUpdateProfileBatch(usernames)


if __name__ == '__main__':
    main(sys.argv[1:])
