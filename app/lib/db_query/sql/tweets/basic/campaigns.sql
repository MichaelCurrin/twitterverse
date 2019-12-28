/*
    Campaigns summary. Includes campaigns with no tweets.
*/

SELECT
    Campaign.name,
    COUNT(*) AS tweets
FROM Campaign
LEFT OUTER JOIN tweet_campaign ON tweet_campaign.campaign_id = Campaign.id
GROUP BY name;
