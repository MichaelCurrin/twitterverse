/*
 Select tweets and their authors. For tweets which are replies, show which tweet
 and profile they were directed at.
 
 Optionally filter to only replies with
 WHERE Tweet.in_reply_to_profile_guid IS NOT NULL
 
 We do left outer join and not an inner join, to show gaps where Profile GUID is
 set but Profile screen name is missing because the Profile is not in the db
 yet.
 */
SELECT
  Profile.screen_name AS author_screen_name,
  Profile.followers_count AS author_followers,
  DATE(Tweet.created_at) AS posted_date,
  Tweet.favorite_count,
  Tweet.retweet_count,
  target_prof.screen_name AS replied_to_profile
FROM
  Tweet
  INNER JOIN Profile ON Profile.id = Tweet.profile_id
  LEFT OUTER JOIN Profile AS target_prof ON target_prof.guid = Tweet.in_reply_to_profile_guid;
