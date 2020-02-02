SELECT
    DATE(Tweet.created_at) AS posted_date,
    COUNT(*)
FROM tweet
INNER JOIN tweet_campaign ON tweet.id = tweet_campaign.tweet_id
INNER JOIN campaign ON campaign.id = tweet_campaign.campaign_id
WHERE campaign.name = 'ENCA'
GROUP BY posted_date;
