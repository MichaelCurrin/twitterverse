SELECT
    '@' || profile.screen_name AS screen_name,
    profile.name,
    profile.followers_count,
    profile.location,
    profile.image_url,
    COUNT(*) AS cnt
FROM tweet
INNER JOIN profile ON tweet.profile_id = profile.id
INNER JOIN tweet_campaign ON tweet.id = tweet_campaign.tweet_id
INNER JOIN campaign ON campaign.id = tweet_campaign.campaign_id
WHERE campaign.name = 'ENCA'
    -- AND followers_count > 100000
GROUP BY screen_name
-- HAVING cnt > 10
ORDER BY cnt DESC
