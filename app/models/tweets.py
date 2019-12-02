# -*- coding: utf-8 -*-
"""
Tweets model application file.

SQL database tables which model the Tweets and Profiles of Twitter users,
the Category groupings of Profiles and Campaign groupings of Tweets.
"""
__all__ = ['Profile', 'Tweet', 'Category', 'ProfileCategory', 'Campaign',
           'TweetCampaign']

import sqlobject as so
from sqlobject import SQLObjectNotFound
from formencode.validators import URL

import lib.text_handling
from lib.validators import UnicodeValidator
from connection import conn

# Set this here to give all classes a valid _connection attribute for
# doing queries with.
so.sqlhub.processConnection = conn


class Profile(so.SQLObject):
    """
    Models a user profile on Twitter.

    Note that URL columns are named as 'Url', since SQLOlbject converts
    'imageURL' to db column named 'image_ur_l'.

    Notes on screen name:
    - This should not have unique restriction as users can edit their screen name.
     (But there is a migration complexity in doing this after it was added.)
      So over time, to accounts could both have used the same screen name a
      point. This was observed in the development of this project. It may or
      may not be the same person in real.
    - Twitter itself enforces uniqueness across case.
    - Twitter's limit is 20 characters, which is mirrored here. It should
      not contain spaces, but this is not enforced here.
    """

    # Profile's ID (integer), as assigned by Twitter when the Profile was
    # created. This is a global ID, rather than an ID specific to our local db.
    guid = so.IntCol(alternateID=True)

    # Profile screen name.
    # TODO Remove `alternateID=True` and do migrations.
    screenName = so.UnicodeCol(alternateID=True, validator=UnicodeValidator(max=20))

    # Profile display Name.
    name = so.UnicodeCol(notNull=True)

    # Description, as set in profile's bio.
    description = so.UnicodeCol(default=None)

    # Location, as set in profile's bio.
    location = so.UnicodeCol(default=None)

    # Link to the profile's image online. This will only be thumbnail size.
    imageUrl = so.UnicodeCol(default=None, validator=URL)

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

    # Get Category objects which this Profile has been assigned to, if any.
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

    def getFlatDescription(self):
        """
        Return the description with newline characters replaced with spaces.
        """
        if self.description is not None:
            return lib.text_handling.flattenText(self.description)

        return None

    def getProfileUrl(self):
        """
        Get link to the profile's page online.

        :return: Twitter profile's URL, as a string.
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

        :return: image URL using 400x400 size parameter, or None if value
            was not set.
        """
        if self.imageUrl:
            return self.imageUrl.replace('_normal', '_400x400')

        return None

    def prettyPrint(self):
        """
        Method to print the attributes of the Profile instance neatly.

        :return: dictionary of data which was printed.
        """
        output = u"""\
Screen name    : @{screenName}
Name           : {name}
Verified       : {verified}
Followers      : {followers:,d}
Statuses       : {statuses:,d}
DB tweets      : {tweetCount}
Description    : {description}
Profile URL    : {url}
Image URL      : {imageUrl}
Stats modified : {statsModified}
        """
        data = dict(
            screenName=self.screenName,
            name=self.name,
            verified=self.verified,
            followers=self.followersCount,
            statuses=self.statusesCount,
            tweetCount=len(self.tweets),
            description=self.getFlatDescription(),
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

    # Link to Tweet's author in the Profile table. Delete Tweet if
    # the Profile is deleted.
    profile = so.ForeignKey('Profile', notNull=True, cascade=True)
    profileIdx = so.DatabaseIndex(profile)

    # Date and time the tweet was posted.
    createdAt = so.DateTimeCol(notNull=True)
    createdAtIdx = so.DatabaseIndex(createdAt)

    # Tweet message text. Length is not validated since expanded tweets can
    # be longer than the standard 280 (previously 140) characters.
    message = so.UnicodeCol(notNull=True)

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

    # Date and time when favorite and retweet counts where last updated.
    modified = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)
    modifiedIdx = so.DatabaseIndex(modified)

    # Get Campaign objects which this Profile has been assigned to, if any.
    campaigns = so.SQLRelatedJoin('Campaign',
                                  intermediateTable='tweet_campaign',
                                  createRelatedTable=False)

    def set(self, **kwargs):
        """
        Update hook.

        Hook to automatically update the modified column's value when updating
        the favorite or retweet count columns.

        If modified field is already provided (such as on record creation), the
        provided modified value is not altered.
        """
        if 'modified' not in kwargs and ('favoriteCount' in kwargs or
                                         'retweetCount' in kwargs):
            kwargs['modified'] = so.DateTimeCol.now()
        super(Tweet, self).set(**kwargs)

    def getFlatMessage(self):
        """
        Return the message with newline characters replaced with spaces.
        """
        return lib.text_handling.flattenText(self.message)

    def getInReplyToTweet(self):
        """
        If this Tweet is a reply, get the original Tweet it was directed at.

        :return: single Tweet object. Return None if this is not a reply. Raise
            an error if the Tweet is not in the local db.
        """
        if self.inReplyToTweetGuid:
            try:
                return Tweet.byGuid(self.inReplyToTweetGuid)
            except SQLObjectNotFound as e:
                raise type(e)("Could not find Tweet in db with GUID: {0}"
                              .format(self.inReplyToTweetGuid))
        return None

    def getInReplyToProfile(self):
        """
        If this Tweet is a reply, get the Profile which it was directed at.

        :return: single Profile object. Return None if this is not a reply.
            Raise an error if the Tweet is not in the local db.
        """
        if self.inReplyToProfileGuid:
            try:
                return Profile.byGuid(self.inReplyToProfileGuid)
            except SQLObjectNotFound as e:
                raise type(e)("Could not find Profile in db with GUID: {0}"
                              .format(self.inReplyToProfileGuid))
        return None

    def getTweetURL(self):
        """
        Return URL for the tweet as a string, using tweet author's screen name
        and the tweet's GUID.
        """
        return 'https://twitter.com/{screenName}/status/{tweetID}'.format(
            screenName=self.profile.screenName,
            tweetID=self.guid
        )

    def prettyPrint(self):
        """
        Method to print the attributes of the Tweet instance neatly.

        :return: dictionary of data which was printed.
        """
        output = u"""\
Author            : @{screenName} - {name} - {followers:,d} followers
Created at        : {createdAt}
Message           : {message}
Favorites         : {favoriteCount:,d}
Retweets          : {retweetCount:,d}
Reply To User ID  : {replyProf}
Reply To Tweet ID : {replyTweet}
URL               : {url}
Stats modified    : {statsModified}
        """
        author = self.profile
        data = dict(
            screenName=author.screenName,
            createdAt=self.createdAt,
            name=author.name,
            followers=author.followersCount,
            message=self.getFlatMessage(),
            favoriteCount=self.favoriteCount,
            retweetCount=self.retweetCount,
            replyProf=self.inReplyToProfileGuid,
            replyTweet=self.inReplyToTweetGuid,
            url=self.getTweetURL(),
            statsModified=self.modified,
        )
        print output.format(**data)

        return data


class Category(so.SQLObject):
    """
    Model a Category, which can be assigned to Profiles.

    Group similar profiles in a category. See docs/models.md document.
    """

    class sqlmeta:
        defaultOrder = 'name'

    # Category name can be any case and may have spaces.
    name = so.UnicodeCol(alternateID=True, validator=UnicodeValidator(max=50))

    createdAt = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)

    # Get Profile objects assigned to the Category.
    profiles = so.SQLRelatedJoin('Profile',
                                 intermediateTable='profile_category',
                                 createRelatedTable=False)


class ProfileCategory(so.SQLObject):
    """
    Model the many-to-many relationship between Profile and Category records.

    Attributes are based on a recommendation in the SQLObject docs.
    """

    profile = so.ForeignKey('Profile', notNull=True, cascade=True)
    category = so.ForeignKey('Category', notNull=True, cascade=True)
    uniqueIdx = so.DatabaseIndex(profile, category, unique=True)


class Campaign(so.SQLObject):
    """
    Model a Campaign, which can be assigned to Tweets.

    Used to group Tweets which are added to the db because they matched
    the same campaign, such as a search topic. See docs/models.md document.
    """

    class sqlmeta:
        defaultOrder = 'name'

    # Campaign name can be any case and may have spaces.
    name = so.UnicodeCol(alternateID=True, validator=UnicodeValidator(max=50))

    # Query string to use on Twitter API search, whether manually or on
    # schedule. This is optional, to allow campaigns which are not searches.
    searchQuery = so.UnicodeCol(default=None)

    createdAt = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)

    # Link to Tweet objects assigned to the Campaign.
    tweets = so.SQLRelatedJoin('Tweet',
                               intermediateTable='tweet_campaign',
                               createRelatedTable=False)

    @classmethod
    def getOrCreate(cls, campaignName, query=None):
        """
        Get a campaign otherwise create and return one.

        Query may be empty as in some cases like a utility's campaign label
        the campaign is a label for grouping rather than searching.
        """
        try:
            return cls.byName(campaignName)
        except SQLObjectNotFound:
            return cls(
                name=campaignName,
                searchQuery=query
            )

    @classmethod
    def getOrRaise(cls, campaignName):
        """
        Get campaign by name otherwise raise an error, with instructions.
        """
        try:
            return cls.byName(campaignName)
        except SQLObjectNotFound as e:
            raise type(e)("Use the campaign manager to create the Campaign"
                          " as name and search query. Name not found: {!r}"
                          .format(campaignName))


class TweetCampaign(so.SQLObject):
    """
    Model the many-to-many relationship between Tweet and Campaign records.

    Attributes are based on a recommendation in the SQLObject docs for doing
    this relationship.
    """

    tweet = so.ForeignKey('Tweet', notNull=True, cascade=True)
    campaign = so.ForeignKey('Campaign', notNull=True, cascade=True)
    uniqueIdx = so.DatabaseIndex(tweet, campaign, unique=True)
