/*
    Select all tweets and match them with their authors.
*/

SELECT
    Profile.guid AS profile_guid,
    '@' || Profile.screen_name AS screen_name,
    Profile.followers_count,
    Tweet.guid AS tweet_guid,
    DATE(Tweet.created_at) AS posted_date,
    Tweet.favorite_count,
    Tweet.retweet_count,
    Tweet.message
FROM Tweet
INNER JOIN Profile ON Tweet.profile_id = Profile.id;
