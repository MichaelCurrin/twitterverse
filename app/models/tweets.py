# -*- coding: utf-8 -*-
"""
Tweets model application file.

SQL database tables which model the tweets and profiles of Twitter users.
"""
__all__ = ['Profile', 'Tweet']

import sqlobject as so
from formencode import validators

from connection import conn


class Profile(so.SQLObject):
    """
    Models a user profile on Twitter.

    Note that URL columns ared named as 'Url', since SQLOlbject converts
    'imageURL' to db column named 'image_ur_l'.
    """

    _connection = conn

    # User ID as set by Twitter. This will never change.
    guid = so.IntCol(alternateID=True)

    # Username or screen name. This could change over time, but will still
    # be unique. Twitter's limit is 20 characters but this can be longer
    # if using unicode characters.
    screenName = so.UnicodeCol(alternateID=True, length=60)
    screenNameIdx = so.DatabaseIndex(screenName)

    # Name as set in profile's bio. May include spaces.
    name = so.UnicodeCol(notNull=True, length=100)

    # Description as set in profile's bio.
    description = so.UnicodeCol(length=255, default=None)

    # Location as set in profile's bio..
    location = so.UnicodeCol(length=100, default=None)

    # Link to the profile's image online.
    # Image comes from API as '..._normal.jpeg' but from inspecting
    # Twitter their image server also allows '..._bigger.jpeg' (which is
    # not much bigger) as a '..._400x400.jpeg' (which is very usable).
    imageUrl = so.UnicodeCol(default=None, validator=validators.URL)

    # Count of profile's followers.
    followersCount = so.IntCol(notNull=True)

    # Count of profile's statuses in their lifetime.
    statusesCount = so.IntCol(notNull=True)

    # Profile's verified status.
    verified = so.BoolCol(notNull=True, default=False)

    # Join Profile to all its tweets in the Tweet table.
    tweets = so.MultipleJoin('Tweet')

    def getProfileUrl(self):
        """
        Get link to the profile's page online.

        @return: Twitter profile's URI, as a string.
        """
        return 'https://twitter.com/{0}'.format(self.screenName)


class Tweet(so.SQLObject):
    """
    Models a tweet on Twitter.
    """

    _connection = conn

    # Tweet ID as set by Twitter.
    guid = so.IntCol(alternateID=True)

    # Creator of the tweet.
    profile = so.ForeignKey('Profile', default=None)

    # Message. Allow more than 140 characters because of unicode encoding.
    text = so.UnicodeCol(length=200)

    # Count of favourites.
    favouriteCount = so.IntCol()

    # Tweet object this tweet is replying to, as looked up from reply to
    # status ID. This references the ID col of this table.
    inReplyToTweet = so.ForeignKey('Tweet', default=None)

    # Profile object this tweet is reply to, as looked up from reply to user ID.
    inReplyToProfile = so.ForeignKey('Profile', default=None)


class Category(so.SQLObject):
    """
    Grouping of Twitter profiles such as by industry.
    """
    _connection = conn


class ProfileCategory(so.SQLObject):
    """
    Mapping of Twitter profile to a Category grouping. A profile can exist in
    multiple categories.
    """
    _connection = conn


def test():
    for m in [Profile]:
        m.dropTable(ifExists=True)
        m.createTable()

        p = Profile(guid=123, screenName='abc', name='my name',
                    followersCount=1, statusesCount=2),
        print p


if __name__ == '__main__':
    test()
