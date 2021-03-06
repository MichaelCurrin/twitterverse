/*
    Select all tweets and match with their authors.

    For replies, show the GUID of the target tweet and the screen name of the
    target profile.

    GUIDs are formatted as strings so they read as text rather than integers
    when parsed as a CSV file.

    DATETIME is used to remove microseconds from posted datetime.

    We replace '\n' and '\r' characters on message. While these new line
    characters are fine in normal CSV software but cause issues in
    Google Data Studio when importing, so are removed. From research, it is
    effective to use the CHAR values, otherwise the hex values have to be used.
*/

SELECT
    'ID_' || Profile.guid AS author_guid,

    '@' || Profile.screen_name AS screen_name,
    Profile.name AS name,

    Profile.image_url AS author_image_url,
    Profile.followers_count AS author_follower_count,
    Profile.location AS author_bio_location,

    'ID_' || Tweet.guid AS tweet_guid,
    DATE(Tweet.created_at) AS posted_date,
    DATETIME(Tweet.created_at) AS posted_datetime,

    Tweet.favorite_count AS favs,
    Tweet.retweet_count AS RTs,
    REPLACE(REPLACE(Tweet.message, CHAR(10), ' '), CHAR(13), ' ') AS message,

    'ID_' || Tweet.in_reply_to_tweet_guid AS replied_to_tweet_guid,
    '@' || target_prof.screen_name AS replied_to_prof_screen_name,
    target_prof.image_url AS replied_to_prof_image_url
FROM Tweet
INNER JOIN Profile ON Tweet.profile_id = Profile.id
LEFT OUTER JOIN Profile AS target_prof ON target_prof.guid = Tweet.in_reply_to_profile_guid
ORDER BY posted_datetime DESC;
