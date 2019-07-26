# -*- coding: utf-8 -*-
"""
Extract library writer module.

Write out Twitter data to a CSV.

There are multiple functions here write out a CSV to a required location,
based on the data required to be written. The path is variable and the
filename part is expected to be descriptive of the method of fetching
from the API.

Rows are appended so that the data can be continuously added to an existing
file. This for when stopping and resuming the extract process, switching
between various search queries, or when periodically writing out data every 15
minutes (to reduce the number of tweets held in memory at a time which would
slow performance and be a risk of losing data on the extract script aborting).

To flatten pages of tweets into a flat list of tweets, see how to make a flat
list out of a list of lists:
    https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python

Handling universal newlines in Python 3:
    https://softwareengineering.stackexchange.com/questions/298677/why-is-universal-newlines-mode-deprecated-in-python
"""
import csv
import datetime
import logging
import os

import lib


logger = logging.getLogger("lib.extract.writer")

PROFILE_COLUMNS = (
    'profileGuid',
    'screenName',
    'name',
    'description',
    'location',
    'imageUrl',
    'followersCount',
    'statusesCount',
    'verified',
)
TWEET_COLUMNS = (
    'tweetGuid',
    'createdAt',
    'message',
    'favoriteCount',
    'retweetCount',
    'inReplyToTweetGuid',
    'inReplyToProfileGuid'
)
METADATA_COLUMNS = (
    'campaignName',
    'modified'
)


def convertToOutRow(campaignName, modified, fetchedProfile=None,
                    fetchedTweet=None):
    """
    Convert fetched Twitter data and metadata as a row for a CSV writer.

    Supply one or both of the `fetchTweet` and `fetchProfile` parameters to
    include the input data in the returned dict.

    @param campaignName: Name of the campaign associated with tweet. If this
        is given as `None`, then it is written as an empty string.
    @param modified: Fetch time of the data, as a datetime.datetime object.
    @param fetchedProfile: Optional tweepy tweet author object as fetched
        from the Twitter API. If provided, add to response dict.
    @param fetchedTweet: Optional tweepy tweet object as fetched from the
        Twitter API. If provided, add to response dict.

    @return: dict object of fields around a profile and/or profile object.
        All unicode values are converted to str, since the csv.DictWriter
        object only handles str types.
    """
    outData = {}

    if fetchedProfile:
        profileData = {
            'profileGuid':    fetchedProfile.id,
            'screenName':     fetchedProfile.screen_name,
            'name':           fetchedProfile.name,
            'description':    fetchedProfile.description,
            'location':       fetchedProfile.location,
            'imageUrl':       fetchedProfile.profile_image_url_https,
            'followersCount': fetchedProfile.followers_count,
            'statusesCount':  fetchedProfile.statuses_count,
            'verified':       fetchedProfile.verified,
        }
        outData.update(profileData)

    if fetchedTweet:
        awareTime = lib.set_tz(fetchedTweet.created_at)

        # Assume extended mode was requested from the API and the full_text
        # field will be returned, but fall back to standard mode.
        try:
            text = fetchedTweet.full_text
        except AttributeError:
            text = fetchedTweet.text

        tweetData = {
            'tweetGuid':            fetchedTweet.id,
            'createdAt':            str(awareTime),
            'message':              text,
            'favoriteCount':        fetchedTweet.favorite_count,
            'retweetCount':         fetchedTweet.retweet_count,
            'inReplyToTweetGuid':   fetchedTweet.in_reply_to_status_id,
            'inReplyToProfileGuid': fetchedTweet.in_reply_to_user_id
        }
        outData.update(tweetData)

    metaData = {
        'campaignName': campaignName,
        'modified':     str(modified)
    }
    outData.update(metaData)

    return {k: (v.encode('utf-8') if type(v) is unicode else v)
            for k, v in outData.iteritems()}


def writeProfilesAndTweets(outPath, outPages, campaignName=None,
                           modified=None):
    """
    Format received pages of Twitter data and append rows of data to a CSV.

    The "\r" character has caused issues before outside of quoted string,
    therefore quotes are used on all values.

    @param outPath: Path of CSV file to write to.
    @param outPages: Pages of tweepy tweet objects to be written out.
    @param campaignName: Optional name of campaign to associate tweet record
        with. By default, this will be written as an empty string value in the
        output CSV.
    @param modified: Optional fetch time of the data, as a datetime.datetime
        object. If not specified, the time at the start of this function
        will be used in all rows.

    @return count: Count of rows written out.
    """
    startTime = datetime.datetime.now()

    if modified is None:
        modified = datetime.datetime.now()

    # TODO: Write in logic here to use different iteration and arguments
    # depending on the requirements, for when it is not tweets and authors.
    outRows = [
        convertToOutRow(
            campaignName,
            modified,
            fetchedTweet=tweet,
            fetchedProfile=tweet.author
        )
        for page in outPages for tweet in page
    ]

    isNewFile = not os.path.exists(outPath)
    with open(outPath, 'a') as fOut:
        # TODO: Write in logic to determine this based on arguments.
        fieldNames = PROFILE_COLUMNS + TWEET_COLUMNS + METADATA_COLUMNS
        csvWriter = csv.DictWriter(
            fOut,
            fieldNames,
            quote=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        if isNewFile:
            csvWriter.writeheader()
        csvWriter.writerows(outRows)

    count = len(outRows)
    filename = os.path.basename(outPath)
    duration = datetime.datetime.now() - startTime

    logger.info(
        "Wrote {count:,d} rows to: {filename} in {duration:3,.2f}s"
        .format(
            count=count,
            filename=filename,
            duration=duration.total_seconds()
        )
    )

    return count
