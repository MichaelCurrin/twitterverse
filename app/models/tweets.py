# -*- coding: utf-8 -*-
"""
Tweets model application file.

SQL database tables which model the tweets and profiles of Twitter users.
"""
__all__ = ['Profile', 'Tweet', 'Label', 'Category', 'ProfileLabel',
           'ProfileCategory']

from formencode import validators
import sqlobject as so
from sqlobject import SQLObjectNotFound

from connection import conn

# Set this here to setup all classes withthe connection
so.sqlhub.processConnection = conn


class Profile(so.SQLObject):
    """
    Models a user profile on Twitter.

    Note that URL columns ared named as 'Url', since SQLOlbject converts
    'imageURL' to db column named 'image_ur_l'.
    """

    # Profile's ID (integer), as assigned by Twitter when the Profile was
    # created. This is a global ID, rather than an ID specific to our local db.
    guid = so.IntCol(alternateID=True)

    # Username or screen name. This could change over time, but will still
    # be unique. Twitter's limit is 20 characters, but this can be longer
    # if using unicode characters.
    screenName = so.UnicodeCol(alternateID=True, length=60)

    # Name, as set in profile's bio. May include spaces.
    name = so.UnicodeCol(notNull=True, length=100)

    # Description, as set in profile's bio.
    description = so.UnicodeCol(length=255, default=None)

    # Location, as set in profile's bio.
    location = so.UnicodeCol(length=100, default=None)

    # Link to the profile's image online. This will only be thumbnail size.
    imageUrl = so.UnicodeCol(default=None, validator=validators.URL)

    # Count of profile's followers.
    followersCount = so.IntCol(notNull=True)

    # Count of profile's statuses (tweets) posted by this profile.
    statusesCount = so.IntCol(notNull=True)

    # Profile's verified status.
    verified = so.BoolCol(notNull=True, default=False)

    # Join the Profile with its created tweets in the Tweet table.
    tweets = so.MultipleJoin('Tweet')

    # Date and time when follower and status counts were last updated.
    modified = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)
    modifiedIdx = so.DatabaseIndex(modified)

    # Get Label objects which this Profile has been assigned to.
    labels = so.SQLRelatedJoin('Label',
                               intermediateTable='profile_label',
                               createRelatedTable=False)

    # Get Category objects which this Profile has been assigned to.
    categories = so.SQLRelatedJoin('Category',
                                   intermediateTable='profile_category',
                                   createRelatedTable=False)

    def set(self, **kwargs):
        """
        Hook to automatically update the modified column value when updating
        the follower count or status count columns.

        If modified field is already provided (such as on record creation), the
        provided modified value is not altered.
        """
        if 'modified' not in kwargs and ('followersCount' in kwargs or
                                         'statusesCount' in kwargs):
            kwargs['modified'] = so.DateTimeCol.now()
        super(Profile, self).set(**kwargs)

    def getProfileUrl(self):
        """
        Get link to the profile's page online.

        @return: Twitter profile's URL, as a string.
        """
        return 'https://twitter.com/{0}'.format(self.screenName)

    def getLargeImageUrl(self):
        """
        Get link to a large version profile's image, based on thumbnail URL.

        The image URL comes from the API as '..._normal.jpeg', but
        from API calls on loading a twitter.com page, it is possible to
        see that the image media server allows variations of the last part,
        to return a large image. Such as
         - '..._bigger.jpeg' (which is not much bigger than the normal
                thumbnail)
         - '..._400x400.jpeg' (which is much bigger).

        @return: image URL using 400x400 size parameter, or None if value
            was not set.
        """
        if self.imageUrl:
            return self.imageUrl.replace('_normal', '_400x400')
        else:
            return None

    def prettyPrint(self):
        """
        Method to print the attributes of the Profile instance neatly.

        We replace the newline characters '\n' in the description with
        empty character, to flatten to a single line. But we also have to
        replace the carriage return '\r',to stop the first part the row
        from being overwritten.

        @return: dictionary of data which was printed.
        """
        output = u"""\
Screen name: @{profSN}
Name       : {profName}
Followers  : {followers:,d}
Statuses   : {statuses:,d}
DB tweets  : {tweetCount}
Description: {description}
Profile URL: {url}
Image URL  : {imageUrl}
Stats      : {statsModified}
        """
        data = dict(
            profSN=self.screenName,
            profName=self.name,
            followers=self.followersCount,
            statuses=self.statusesCount,
            tweetCount=len(self.tweets),
            description=self.description.replace('\n', '').replace('\r', ''),
            url=self.getProfileUrl(),
            imageUrl=self.getLargeImageUrl(),
            statsModified=self.modified,
        )

        print output.format(**data)

        return data


class Tweet(so.SQLObject):
    """
    Models a tweet on Twitter.

    If we are inserting the Tweet in our db, we expect to always have the
    author's profile in the Profile table. If the tweet is a reply, we will have
    references to the target Profile and original Tweet as GUID integers.
    But we are unlikely to have those object stored in our db. Use
    the `.getInReplyToTweet` and `.getInReplyToProfile` methods to see if those
    exist in the db, otherwise use the GUIDs to look up data from the
    Twitter API and then store them locally as db records.

    For relating a Tweet to its author Profile with a foreign key, a
    `setProfileByGuid` method could be implemented to set the profile
    foreign key using a given GUID, but that would require doing a search
    each time. So, when creating a Tweet object or multiple objects for one
    Profile, it is preferable to get the Profile object's ID once
    and then repeately pass that in as an argument for each Tweet object
    that is created for that Profile.

    For ordering, the '-guid' syntax is here is preferred, since
    'guid DESC' results in an error when getting tweets of a Profile object,
    even though doing a query on Tweet class itself is fine.
        `AttributeError: 'Tweet' object has no attribute 'guid DESC'`
    The error is also raised for multiple names e.g. '-guid, message'.
    """

    class sqlmeta:
        # Show recent Tweets (with higher GUID values) first.
        defaultOrder = '-guid'

    # Tweet ID (integer), as assigned by Twitter when the Tweet was posted.
    # This is a global ID, rather than specific to our local db.
    guid = so.IntCol(alternateID=True)

    # Link to Tweet's creator in the Profile table.
    profile = so.ForeignKey('Profile', notNull=True)

    # Date and time the tweet was posted.
    createdAt = so.DateTimeCol(notNull=True)

    # Tweet message text. We allow more than 140 characters because of unicode
    # encoding.
    message = so.UnicodeCol(length=200, notNull=True)

    # Count of favorites on this Tweet.
    favoriteCount = so.IntCol(notNull=True)

    # Count of retweets of this Tweet.
    retweetCount = so.IntCol(notNull=True)

    # If the tweet is a reply, the GUID of the Tweet which the reply is
    # directed at (from reply_to_status_id field). This does not require
    # the Tweet to be in the local db.
    inReplyToTweetGuid = so.IntCol(default=None)

    # If the tweet is a reply, the GUID of the Profile which the reply is
    # directed at (from reply_to_user_id field). This does not require
    # the Tweet to be in the local db.
    inReplyToProfileGuid = so.IntCol(default=None)

    # Date and time when favorie and retweet counts where last updated.
    modified = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)
    modifiedIdx = so.DatabaseIndex(modified)

    def set(self, **kwargs):
        """
        Hook to automatically update the modified column value when updating
        the favorite or retweet count columns.

        If modified field is already provided (such as on record creation), the
        provided modified value is not altered.
        """
        if 'modified' not in kwargs and ('favoriteCount' in kwargs or
                                         'retweetCount' in kwargs):
            kwargs['modified'] = so.DateTimeCol.now()
        super(Tweet, self).set(**kwargs)

    def getInReplyToTweet(self):
        """
        If this Tweet is a reply, get the original Tweet it was directed at.

        @return: single Tweet object. Return None if this is not a reply. Raise
            an error if the Tweet is not in the local db.
        """
        if self.inReplyToTweetGuid:
            try:
                return Tweet.byGuid(self.inReplyToTweetGuid)
            except SQLObjectNotFound as e:
                raise type(e)('Could not find Tweet in db with GUID {0}'
                              .format(self.inReplyToTweetGuid))
        else:
            return None

    def getInReplyToProfile(self):
        """
        If this Tweet is a reply, get the Profile which it was directed at.

        @return: single Profile object. Return None if this is not a reply.
            Raise an error if the Tweet is not in the local db.
        """
        if self.inReplyToProfileGuid:
            try:
                return Profile.byGuid(self.inReplyToProfileGuid)
            except SQLObjectNotFound as e:
                raise type(e)('Could not find Profile in db with GUID {0}'
                              .format(self.inReplyToProfileGuid))
        else:
            return None

    def getTweetURL(self):
        """
        Return URL for the tweet as a string, using tweet author's screen name
        and the tweet's GUID.
        """
        return 'https://twitter.com/{screenName}/status/{tweetID}'.format(
            screenName=self.profile.screenName, tweetID=self.guid
        )

    def prettyPrint(self):
        """
        Method to print the attributes of the Tweet instance neatly.

        @return: dictionary of data which was printed.
        """
        output = u"""\
Author           : @{profSN} - {profName} - {followers:,d} followers
Message          : {message}
Favorites        : {favoriteCount:,d}
Retweets         : {retweetCount:,d}
Reply To User ID : {replyProf}
Reply To Tweet ID: {replyTweet}
URL              : {url}
Stats modified   : {statsModified}
        """
        author = self.profile
        data = dict(
            profSN=author.screenName,
            profName=author.name,
            followers=author.followersCount,
            message=self.message.replace('\n', ''),
            favoriteCount=self.favoriteCount,
            retweetCount=self.retweetCount,
            replyProf=self.inReplyToProfileGuid,
            replyTweet=self.inReplyToTweetGuid,
            url=self.getTweetURL(),
            statsModified=self.modified,
        )

        print output.format(**data)

        return data


class Label(so.SQLObject):
    """
    Model a label which can be assigned to a Profile.

    A label indicates the reason the Twitter user or their tweets were added
    to the db. They could be around events, brands or campaigns when
    doing a tweet search. Or a label could be "influencer" or "watch"
    based on how or why the Twitter user was added as a Profile record.
    A label could be assigned to a batch of Profiles when they are added to
    the db from a Twitter screen naeme list, or when the Profile is added
    to the db because one of tweets matches the search criteria given to
    the API.

    Labels assigned to Profiles are useful when routinely fetching new tweets
    for watched Twitter users in the Profile table, since filtering can be
    done on one label to reduce the number of Profiles to look up.
    A label can also be used when reporting on existing Profile or Tweet
    records.
    """

    class sqlmeta:
        defaultOrder = 'name'

    # Label name can be any case and may have spaces.
    name = so.UnicodeCol(alternateID=True, length=50)

    # Get Profile objects assigned to the Label.
    profiles = so.SQLRelatedJoin('Profile',
                                 intermediateTable='profile_label',
                                 createRelatedTable=False)

class Category(so.SQLObject):
    """
    Model a category which can be assigned to a Profile.

    A category indicates the nature of the Twitter user in real life or the
    content of their tweets and therefore should be allocated by hand
    rather than as a batch. Some useful categories are sports, politics,
    arts & culture or music.

    For reporting, categories can be used when to filter Profile or Tweet
    records so as to compare records within or across categories.
    """

    class sqlmeta:
        defaultOrder = 'name'

    # Category name can be any case and may have spaces.
    name = so.UnicodeCol(alternateID=True, length=50)

    # Get Profile objects assigned to the Category.
    profiles = so.SQLRelatedJoin('Profile',
                                 intermediateTable='profile_category',
                                 createRelatedTable=False)


class ProfileLabel(so.SQLObject):
    """
    Model the many-to-many relationship between Place and Label records.
    """

    profile = so.ForeignKey('Profile', notNull=True, cascade=True)
    label = so.ForeignKey('Label', notNull=True, cascade=True)
    unique = so.DatabaseIndex(profile, label, unique=True)


class ProfileCategory(so.SQLObject):
    """
    Model the many-to-many relationship between Place and Category records.
    """

    profile = so.ForeignKey('Profile', notNull=True, cascade=True)
    category = so.ForeignKey('Category', notNull=True, cascade=True)
    unique = so.DatabaseIndex(profile, category, unique=True)
