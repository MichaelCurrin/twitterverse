-- Top 100 most retweeted tweets in the past 7 days, with user details.

SELECT
    Profile.screen_name,
    Profile.followers_count,
    Tweet.created_at,
    Tweet.favorite_count,
    Tweet.retweet_count,
    Tweet.message
FROM Tweet
INNER JOIN Profile ON Profile.id = Tweet.profile_id
WHERE DATE(Tweet.created_at) >= DATE('today', '-100 days')
ORDER BY Tweet.retweet_count DESC
LIMIT 100
