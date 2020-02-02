
SELECT
    Profile.screen_name AS author_screen_name,
    Profile.followers_count AS author_followers,
    DATE(Tweet.created_at) AS posted_date,
    Tweet.favorite_count,
    Tweet.retweet_count,
    target_prof.screen_name AS replied_to_profile
FROM Tweet
INNER JOIN Profile ON Profile.id = Tweet.profile_id
LEFT OUTER JOIN Profile AS target_prof ON target_prof.guid = Tweet.in_reply_to_profile_guid;
INNER JOIN tweet_campaign ON tweet.id = tweet_campaign.tweet_id
INNER JOIN campaign ON campaign.id = tweet_campaign.campaign_id
WHERE campaign.name = 'ENCA'