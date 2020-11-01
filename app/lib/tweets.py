"""
Tweets lib application file.

Handle fetching and storing of profile and tweet data.

Fetch profile or tweet data from the Twitter API using tweepy. Then insert the
data into the Tweet and Profile tables of the local database (see
models/tweets.py file). Also apply Campaign and Category labels.

That is done here either using the ORM (custom classes to represent tables
in the database) or by build and executing native SQL statements which will be
several times faster.

For a user interface on fetching and inserting data, see the utils directory.

Steps required to get profiles and their tweets:
 1. Start with a Twitter screen name or screen names, read as
    list in the command-line arguments or read from a text file.
 2. Get the Profile data for the users and store in the database, either
    creating the record or updating if record exists in Profile table.
 3. Get tweets from the timeline of the user and store in Tweets table, with a
    link back to the Profile record. Repeat for all profiles of interest.
"""
import json
import math

import tweepy
from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError
from sqlobject.sqlbuilder import Insert, LIKE
from tweepy.error import TweepError

import lib
import lib.text_handling
from lib import database as db
from lib.twitter_api import authentication

# This null character is invisible but appears sometimes such in profile
# description from Twitter and cannot be inserted due to SQLite execute error.
NULL = "\x00"
# TODO Can this be done as an override for all fields when inserting into the
# model? Like for init / update or similar.


def clean(v):
    return v.replace(NULL, "")


def _parse_tweepy_profile(fetchedProfile):
    """
    :param tweepy.User fetchedProfile: User data as fetched from Twitter API.

    :return: Simplified user data, as a dict.
    """
    return {
        "guid": fetchedProfile.id,
        "screenName": fetchedProfile.screen_name,
        "name": fetchedProfile.name,
        "description": clean(fetchedProfile.description),
        "location": fetchedProfile.location,
        "imageUrl": fetchedProfile.profile_image_url_https,
        "followersCount": fetchedProfile.followers_count,
        "statusesCount": fetchedProfile.statuses_count,
        "verified": fetchedProfile.verified,
    }


def _parse_tweepy_tweet(fetchedTweet, profileID):
    """
    :param tweepy.Status fetchedTweet: Tweet data as fetched from the Twitter
        API.
    :param int profileID: ID of the Profile record in the database which
        is the tweet author.

    :return tweetData: Simplified tweet data, as a dict.
    """
    # Assume extended mode (as set on the API request), otherwise fall back to
    # standard mode.
    try:
        text = fetchedTweet.full_text
    except AttributeError:
        text = fetchedTweet.text

    return {
        "guid": fetchedTweet.id,
        "profileID": profileID,
        "createdAt": fetchedTweet.created_at,
        "message": text,
        "favoriteCount": fetchedTweet.favorite_count,
        "retweetCount": fetchedTweet.retweet_count,
        "inReplyToTweetGuid": fetchedTweet.in_reply_to_status_id,
        "inReplyToProfileGuid": fetchedTweet.in_reply_to_user_id,
    }


def _getProfile(APIConn, screenName=None, userID=None):
    """
    Get data of one profile from the Twitter API, for a specified user.

    Either screenName string or userID integer must be specified, but not both.

    :param APIConn: authenticated API connection object.
    :param screenName: The name of Twitter user to fetch, as a string.
    :param userID: The ID of the Twitter user to fetch, as an integer.
        Cannot be set if screenName is also set.

    :return tweepy.User: instance for requested Twitter user.
    """
    assert (
        screenName or userID
    ), "Expected either screenName (str) or userID (int) to be set."
    assert not (
        screenName and userID
    ), "Cannot set both screenName ({screenName}) and userID ({userID}).".format(
        screenName=screenName, userID=userID
    )

    if screenName:
        print("Fetching user: @{screenName}".format(screenName=screenName))
        params = {"screen_name": screenName}
    else:
        print("Fetching user ID: {userID}".format(userID=userID))
        params = {"user_id": userID}

    return APIConn.get_user(**params)


def insertOrUpdateProfile(profile: [tweepy.User, dict]):
    """
    Insert record in Profile table or update existing record if it exists.

    Replace values in existing record with those fetched from Twitter
    API, assuming that any value (except the GUID) could change. Even if their
    screen name does change, we know that it is the same Profile based on the
    GUID and so can update the existing record instead of inserting a new one.

    :param [tweepy.User, dict] profile: Data for a Twitter user.

    :return models.tweets.Profile profileRec: Local record for tweet author.
    """
    if isinstance(profile, dict):
        profileData = profile
    else:
        profileData = _parse_tweepy_profile(profile)

    try:
        # Attempt to insert new row, assuming GUID or screenName do not exist.
        profileRec = db.Profile(**profileData)
    except DuplicateEntryError:
        guid = profileData.pop("guid")
        profileRec = db.Profile.byGuid(guid)
        profileRec.set(**profileData)

    return profileRec


def insertOrUpdateProfileBatch(screenNames):
    """
    Get Twitter profile data from the Twitter API and store in the database.

    Profile records are created, or updated if they already exist.

    :param screenNames: list of user screen names as strings, to be fetched
        from the Twitter API.

    :return successScreenNames: list of user screen names as strings, for the
        Profiles which were successfully fetched then inserted/updated in
        the db.
    :return failedScreenNames: list of user screen names as strings, for the
        Profiles which could not be fetched from the Twitter API and
        inserted/updated in the db.
    """
    APIConn = authentication.getAPIConnection()

    successScreenNames = []
    failedScreenNames = []

    for s in screenNames:
        try:
            fetchedProf = _getProfile(APIConn, screenName=s)
        except TweepError as e:
            # The profile could be missing or suspended, so we log it
            # and then skip inserting or updating (since we have no data).
            print(
                "Could not fetch user: @{name}. {error}. {msg}".format(
                    name=s, error=type(e).__name__, msg=str(e)
                )
            )
            failedScreenNames.append(s)
        else:
            try:
                localProf = insertOrUpdateProfile(fetchedProf)
                # Represent log of followers count visually as repeated stars,
                # sidestepping error for log of zero.
                logFollowers = (
                    int(math.log10(localProf.followersCount))
                    if localProf.followersCount
                    else 0
                )
                stars = "*" * logFollowers
                print(
                    "Inserted/updated user: {name:20} {stars}".format(
                        name=u"@" + localProf.screenName, stars=stars
                    )
                )
                successScreenNames.append(s)
            except Exception as e:
                print(
                    (
                        "Could not insert/update user: @{name}. {error}. {msg}".format(
                            name=s, error=type(e).__name__, msg=str(e)
                        )
                    )
                )
                failedScreenNames.append(s)

    return successScreenNames, failedScreenNames


def _getTweets(
    APIConn, screenName=None, userID=None, tweetsPerPage=200, pageLimit=1, extended=True
):
    """
    Get tweets of one profile from the Twitter API, for a specified user.

    Either screenName string or userID integer must be specified, but not both.
    The result of (tweetsPerPage)*(pageLimit) indicates the total number
    of tweets requested from the API on calling this function.

    :param APIConn: authenticated API connection object.
    :param screenName: Default None. The name of Twitter user to fetch, as
        a string.
    :param userID: Default None. The ID of the Twitter user to fetch, as an
        integer.
    :param tweetsPerPage: Default 200. Count of tweets to get on a page.
        The API''s limit is 200 tweets, but a lower value can be used.
        The `pageLimit` argument can be used to do additional calls
        to get tweets above the 200 limit - see `tweepy.Cursor` method.
    :param pageLimit: Default 1. Number of pages of tweets to get by doing
        a sequence of queries with a cursor. The number of tweets
        on each page is determined by `tweetsPerPage` argument.
    :param extended: If True, get the expanded tweet message instead of the
        truncated form.

    :return list tweetsList: list of tweepy tweet objects for the requested
        user.
    """
    print("Fetching tweets for user: {0}".format(screenName if screenName else userID))

    assert (
        screenName or userID
    ), "Expected either screenName (str) or userID (int) to be set."
    assert not (screenName and userID), "Cannot request both screenName and" " userID."

    params = {"count": tweetsPerPage}
    if extended:
        params["tweet_mode"] = "extended"

    if screenName:
        params["screen_name"] = screenName
    else:
        params["user_id"] = userID

    if pageLimit == 1:
        # Do a simple query without paging.
        tweets = APIConn.user_timeline(**params)
    else:
        tweets = []
        # Send the request parameters to Cursor object, with the page limit.
        for page in tweepy.Cursor(APIConn.user_timeline, **params).pages(pageLimit):
            tweets.extend(page)

    return tweets


def insertOrUpdateTweet(tweet, profileID, writeToDB=True, onlyUpdateEngagements=True):
    """
    Insert or update one record in the Tweet table.

    Attempt to insert a new tweet row, but if the GUID exists locally then
    retrieve and update the existing record.

    :param [tweepy.Status, dict] tweet: Data for a single Tweet as fetched
        from the Twitter API.
    :param profileID: The ID of the tweet's author, as an integer from
        the Profile ID column in the local db and NOT the Profile GUID.
        This is used to set the Tweet object's foreign key.
    :param writeToDB: Default True. If True, write the fetched tweets
        to local database, otherwise print and discard them.
    :param onlyUpdateEngagements: Default True to only update the favorite
        and retweet count of the tweet in the local db. If False, update
        other fields too. Those are expected to be static on the Twitter API,
        but if rules change on this repo then it is useful to apply them
        historically on existing Tweet records. This flag only affects
        existing records.

    :return dict data: Formatted Tweet data.
    :return tweetRec: If writeToDB is True, then return the Tweet record
        which was inserted or updated. Otherwise return None.
    """
    if isinstance(tweet, dict):
        tweetData = tweet
    else:
        tweetData = _parse_tweepy_tweet(tweet, profileID)

    tweetData["createdAt"] = lib.set_tz(tweetData["createdAt"])

    if writeToDB:
        try:
            tweetRec = db.Tweet(**tweetData)
        except DuplicateEntryError:
            guid = tweetData.pop("guid")
            tweetRec = db.Tweet.byGuid(guid)
            if onlyUpdateEngagements:
                tweetRec.set(
                    favoriteCount=tweetData["favoriteCount"],
                    retweetCount=tweetData["retweetCount"],
                )
            else:
                tweetRec.set(**tweetData)
    else:
        tweetRec = None

    return tweetData, tweetRec


def insertOrUpdateTweetBatch(
    profileRecs,
    tweetsPerProfile=200,
    verbose=False,
    writeToDB=True,
    campaignRec=None,
    onlyUpdateEngagements=True,
):
    """
    Get Twitter tweet data from the Twitter API for a batch of profiles
    and store their tweets in the database.

    The verbose and writeToDB flags can be used together to print tweet
    data which would be inserted into the database without actually inserting
    it. This can be used preview tweet data without increasing storage or using
    time to do inserts and updates.

    :param profileRecs: list of Profile objects, to create or update
        tweets for. This might be a list from the Profile table which
        has been filtered based on a job schedule, or Profiles which
        match criteria such as high follower count.
    :param tweetsPerProfile: Default 200. Count of tweets to get for each
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
        where the script takes a fixed time to get 200 or 1 tweets and
        now that is has processed the 1 requested and the window limit is
        hit, it has no Tweet processing to do while waiting for the next rate
        limited window. Thought a low value will mean less storage space
        is required.
    :param verbose: Default False. If True, print the data used to created
        a local Tweet record. This data can be printed regardless of whether
        the data is written to the db record or not.
    :param writeToDB: Default True. If True, write the fetched tweets
        to local database, otherwise print and discard them. This is useful
        when used in combination with verbose flag which prints the data.
    :param campaignRec: Campaign record to assign to the local Tweet records.
        Default None to not assign any Campaign.
    :param onlyUpdateEngagements: Default True to only update the favorite
        and retweet count of the tweet in the local db. If False, update
        other fields too. Those are expected to be static on the Twitter API,
        but if rules change on this repo then it is useful to apply them
        historically on existing Tweet records. This flag only affects
        existing records.

    :return: None
    """
    APIConn = authentication.getAPIConnection()

    if tweetsPerProfile <= 200:
        tweetsPerPage = tweetsPerProfile
        pageLimit = 1
    else:
        tweetsPerPage = 200
        # Round up to get the last page which might have fewerb items
        pageLimit = math.ceil(tweetsPerProfile / tweetsPerPage)

    for p in profileRecs:
        try:
            fetchedTweets = _getTweets(
                APIConn, userID=p.guid, tweetsPerPage=tweetsPerPage, pageLimit=pageLimit
            )
        except TweepError as e:
            print(
                "Could not fetch tweets for user: @{screenName}."
                " {type}. {msg}".format(
                    screenName=p.screenName, type=type(e).__name__, msg=str(e)
                )
            )
        else:
            print("User: {0}".format(p.screenName))

            if writeToDB:
                print("Inserting/updating tweets in db...")
            else:
                print("Displaying tweets but not inserting/updating...")

            added = errors = 0
            for f in fetchedTweets:
                try:
                    data, tweetRec = insertOrUpdateTweet(
                        tweet=f,
                        profileID=p.id,
                        writeToDB=writeToDB,
                        onlyUpdateEngagements=onlyUpdateEngagements,
                    )
                    if tweetRec and campaignRec:
                        try:
                            campaignRec.addTweet(tweetRec)
                        except DuplicateEntryError:
                            # Ignore error if Tweet was already assigned.
                            pass
                    if verbose:
                        if tweetRec:
                            tweetRec.prettyPrint()
                        else:
                            # No record was created, so use data dict.
                            m = data["message"]
                            created = data["createdAt"]
                            data["message"] = lib.text_handling.flattenText(m)
                            data["createdAt"] = str(lib.set_tz(created))
                            # TODO: Check if this will raise an error
                            # on unicode symbols in message.
                            print(json.dumps(data, indent=4))
                    added += 1
                except Exception as e:
                    print(
                        "Could not insert/update tweet `{id}` for user"
                        " @{screenName}. {type}. {msg}".format(
                            id=f.id,
                            screenName=p.screenName,
                            type=type(e).__name__,
                            msg=str(e),
                        )
                    )
                    errors += 1

                total = added + errors
                # Print stats on every 10 processed and on the last item.
                if total % 10 == 0 or f == fetchedTweets[-1]:
                    print(
                        "Total: {total:2,d}. Added: {added:2,d}. "
                        "Errors: {errors:2,d}.".format(
                            total=total, added=added, errors=errors
                        )
                    )


def lookupTweetGuids(APIConn, tweetGuids, onlyUpdateEngagements=True):
    """
    Lookup tweet GUIDs and store entire tweets and authors in the database.

    Receive a list of tweet GUIDs (IDs in the Twitter API), break them into
    chunks (lists of up to 100 GUIDs), look them up from the API and then
    insert or update the tweets and their authors in the database.

    Note that tweet_mode='extended' is not available in tweeypy for
    statuses_lookup, though it is used on the other endpoints.
    See https://github.com/tweepy/tweepy/issues/785.

    :param APIConn: authorised tweepy.API connection.
    :param tweetGuids: list of Twitter API tweet GUIDs, as integers or strings.
        The list will be a split into a list of chunks each with a max
        count of 100 items. The Cursor approach will not work because the
        API endpoints limits the number of items be requested and since there
        is only ever one page of results.
    :param onlyUpdateEngagements: Default True to only update the favorite
        and retweet count of the tweet in the local db. If False, update
        other fields too. Those are expected to be static on the Twitter API,
        but if rules change on this repo then it is useful to apply them
        historically on existing Tweet records. This flag only affects
        existing records.

    :return: None
    """
    chunks = [
        tweetGuids[i : (i + 100)] for i in range(0, len(tweetGuids), 100)  # noqa: E203
    ]

    for chunk in chunks:
        fetchedTweetList = APIConn.statuses_lookup(chunk)

        for t in fetchedTweetList:
            profileRec = insertOrUpdateProfile(profile=t.author)
            data, tweetRec = insertOrUpdateTweet(
                tweet=t,
                profileID=profileRec.id,
                onlyUpdateEngagements=onlyUpdateEngagements,
            )
            tweetRec.prettyPrint()


def updateTweetEngagements(APIConn, tweetRecSelect):
    """
    Update engagements of local tweet records.

    Expect a select results of Tweets in the db, extract their GUIDs, get the
    latest favorite and retweet from the API and then store the updated values.
    If any of the looked up Tweet GUIDs are not returned from the API
    (deleted/private/reported) then we do not have anything to save for it.

    It is necessary to split the records into chunks or pages of up to 100
    items, since that is the maxinum number of tweet IDs which the statuses
    lookup endpoint allows.

    TODO: Instead of expecting tweet record select results, This could be more
    efficient by doing a set filtered to where GUID is t.id, provided the
    record is there, rather than getting the object and then setting. This can
    be even more efficient by fetching of tweets from the API then
    doing a single UPDATE query using native SQL, instead of using the ORM.

    :param APIConn: API Connection.
    :param tweetRecSelect: SQLObject select results for model.Tweet instances,
        or simply a list of the instances.

    :return: None
    """
    # Use list() to  get all the records at once, so only one fetch query
    # is done. Also, its not possible to do .count() on sliced select results
    # and we need to know the total before splitting into chunks of 100 items.
    guids = [t.guid for t in list(tweetRecSelect)]
    chunks = [guids[i : (i + 100)] for i in range(0, len(guids), 100)]  # noqa: E203

    for chunk in chunks:
        fetchedTweets = APIConn.statuses_lookup(chunk)

        for t in fetchedTweets:
            tweetRec = db.Tweet.byGuid(t.id)
            oldEngagements = (tweetRec.favoriteCount, tweetRec.retweetCount)
            tweetRec.set(favoriteCount=t.favorite_count, retweetCount=t.retweet_count)
            print(
                "Updated tweet GUID: {guid}, fav: {fav:3,d} ({oldFav:3,d}),"
                " RT: {rt:3,d} ({oldRt:3,d})".format(
                    guid=t.id,
                    fav=t.favorite_count,
                    oldFav=oldEngagements[0],
                    rt=t.retweet_count,
                    oldRt=oldEngagements[1],
                )
            )


def assignProfileCategory(categoryName, profileRecs=None, screenNames=None):
    """
    Assign Categories to Profiles.

    Fetch Category or create it if it does not exist. Put Profiles in the
    Category but ignore if link exists already. An error is raised
    if a Profile does not exist, but previous Profiles in the list still
    have been allocated already before the error occurred.

    :param categoryName: String. Get a category by name and create it
        if it does not exist yet. If Profile records or Profile screen names
        are provided, then assign all of those Profiles to the category.
        Both Profile inputs can be left as not set to just create the
        Category.
    :param profileRecs: Default None. List of db Profile records to be
        assigned to the category. Cannot be empty if screenNames is also empty.
    :param screenNames: Default None. List of Profile screen names to be
        assigned to the category. The screen names should exist as Profiles
        in the db already (matching on exact case), otherwise an error will
        be raised. The screenNames argument cannot be empty if profileRecs
        is also empty.

    :return tuple of new and existing counts.
        - newCnt: Count of new Profile Category links created.
        - existingCnt: Count of Profile Category links not created because
            they already exist.
    """
    newCnt = 0
    existingCnt = 0

    try:
        categoryRec = db.Category.byName(categoryName)
    except SQLObjectNotFound:
        categoryRec = db.Category(name=categoryName)
        print("Created category: {0}".format(categoryName))

    if profileRecs or screenNames:
        if profileRecs is None:
            # Use screen names to populate an empty profileRecs list.
            profileRecs = []
            for screenName in screenNames:
                profile = db.Profile.select(
                    LIKE(db.Profile.q.screenName, screenName)
                ).getOne(None)

                if not profile:
                    raise SQLObjectNotFound(
                        "Cannot assign Category since Profile screen name"
                        " is not in db: {0}".format(screenName)
                    )
                profileRecs.append(profile)

        for profileRec in profileRecs:
            try:
                categoryRec.addProfile(profileRec)
                newCnt += 1
            except DuplicateEntryError:
                existingCnt += 1

    return newCnt, existingCnt


def assignTweetCampaign(campaignRec, tweetRecs=None, tweetGuids=None):
    """
    Assign Campaigns to Tweets using the ORM.

    Fetch a Campaign and assign it to Tweets, ignoring existing links
    and raising an error on a Campaign which does not exist. For large
    batches of inserts, rather use bulkAssignTweetCampaign.

    Search query is not considered here and should be set using the
    campaign manager utility or the ORM directly.

    :param campaignRec: Campaign record to assign to all Tweet
        records indicated with tweetRecs or tweetGuids inputs.
        Both Tweet inputs can be left as not set to just create the
        Campaign. Note that the assignProfileCategory function expects
        a Category name because it can be created there, but here the actual
        Campaign record is expected because creation must be handled with the
        Campaign manager utility instead because of the search query field.
    :param tweetRecs: Default None. List of db Tweet records to be
        assigned to the campaign. Cannot be empty if tweetGuids is also empty.
    :param tweetGuids: Default None. List of Tweet GUIDs to be assigned
        to the campaign. The GUIDs should exist as Tweets in the db already,
        otherwise an error will be printed and ignored. The tweetGuids
        argument cannot be empty if tweetRecs is also empty.

    :return newCnt: Count of new Tweet Campaign links created.
    :return existingCnt: Count of Tweet Campaign links not created because
        they already exist.
    """
    newCnt = 0
    existingCnt = 0

    if not tweetRecs:
        # Use GUIDs to populate tweetRecs list.
        tweetRecs = []
        for guid in tweetGuids:
            try:
                tweet = db.Tweet.byGuid(guid)
            except SQLObjectNotFound:
                raise SQLObjectNotFound(
                    "Cannot assign Campaign as Tweet"
                    " GUID is not in db: {0}".format(guid)
                )
            tweetRecs.append(tweet)

    for tweet in tweetRecs:
        try:
            campaignRec.addTweet(tweet)
            newCnt += 1
        except DuplicateEntryError:
            existingCnt += 1

    return newCnt, existingCnt


def bulkAssignProfileCategory(categoryID, profileIDs):
    """
    Assign Categories to a batch of Profiles using a single INSERT statement.

    This function assumes the Category ID and the Profile IDs are for existing
    values in the db. Any existing profile_category links which raise a
    duplicate error are allowed to fail silently using INSERT OR IGNORE syntax.

    :param categoryID: Category record ID to assign to Profile records.
    :param profileIDs: Iterable of Profile ID records which must be a linked to
        a Category record.

    :return SQL: Multi-line SQL statement which was executed.
    """
    insert = Insert(
        "profile_category",
        template=["category_id", "profile_id"],
        valueList=[(categoryID, profileID) for profileID in profileIDs],
    )
    SQL = db.conn.sqlrepr(insert)
    SQL = SQL.replace("INSERT", "INSERT OR IGNORE")
    db.conn.query(SQL)

    return SQL


def bulkAssignTweetCampaign(campaignID, tweetIDs):
    """
    Assign Campaigns to a batch of Tweets using a single INSERT statement.

    This function assumes the Campaign ID and the Tweet IDs are for existing
    values in the db. Any existing tweet_campaign links which raise a
    duplicate error are allowed to fail silently using INSERT OR IGNORE syntax.

    See SQLite INSERT documentation diagram syntax:
        http://www.sqlite.org/lang_insert.html

    A single INSERT statement is done here, since a mass-insertion using
    the ORM is inefficient:
        http://www.sqlobject.org/FAQ.html#how-to-do-mass-insertion

    The links in tweet_campaign are relatively simple and require validation
    at the schema level rather than the ORM level, therefore it is safe to
    use a native SQL statement through sqlbuilder. The implementation is
    based on an example here:
        http://www.sqlobject.org/SQLBuilder.html#insert

    :param campaignID: Campaign record ID to assign to Tweet records.
    :param tweetIDs: Iterable of Tweet ID records which must be a linked to
        a Campaign record.

    :return SQL: Multi-line SQL statement which was executed.
    """
    insert = Insert(
        "tweet_campaign",
        template=["campaign_id", "tweet_id"],
        valueList=[(campaignID, tweetID) for tweetID in tweetIDs],
    )
    SQL = db.conn.sqlrepr(insert)
    SQL = SQL.replace("INSERT", "INSERT OR IGNORE")
    db.conn.query(SQL)

    return SQL
