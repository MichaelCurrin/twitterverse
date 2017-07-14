#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Testing modeling of a tweet and user.

This is an incomplete file used for testing. Its components can be moved to model.py sometime.
"""
import sqlobject as so
from sqlobject.inheritance import InheritableSQLObject

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from connection import conn


class Tweet(so.SQLObject):
    """
    Models a tweet from Twitter.
    """
    # Tweet ID as set by Twitter.
    guid = so.IntCol(AlternateID=True)

    # Creator of the tweet.
    profile = so.ForeignKey('Profile', default=None)

    # Message.
    text = so.UnicodeCol(length=200)

    # Count of favourites.
    favouriteCount = so.IntCol()

    # Tweet object this tweet is replying to, as looked up from reply to status ID. This references the ID col of this table.
    inReplyToTweet = so.ForeignKey("Tweet", default=None)

    # Profile object this tweet is reply to, as lookuped from reply to user ID.
    inReplyToProfile = so.ForeignKey("Profile", default=None)

    # perhaps store as tweepy object in pickeled col? Or as JSON col from tweepy _json?


class Profile(so.SQLObject):
    """
    Models a user profile on Twitter.
    """
    # User ID as set by Twitter.
    guid = so.IntCol(AlternateID=True)

    # User name.
    name = so.UnicodeCol(length=50)

    # Profile description. Confirm length?
    description = so.UnicodeCol(length=255, notNull=False, default=None)

    # Number of followers.
    followerCount = so.intCol()

    location = so.UnicodeCol(length=255, notNull=False, default=None)

    # Select all tweets posted by this profile.
    tweets = so.MultipleJoin('Tweet')


class ProfileCategory(so.SQLObject):
    """
    Mapping to Twitter profile to a Category grouping. A profile can exist in multiple groups.
    """
    pass


class Category(so.SQLObject):
    """
    Grouping of Twitter profile such as by industry.
    """
    pass