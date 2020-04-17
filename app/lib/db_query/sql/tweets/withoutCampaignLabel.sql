/*
    Tweets without camapign labels.

    These would have been added using the query parameter of the search and no campaign name.
*/

SELECT Tweet.message
FROM Tweet
WHERE Tweet.id NOT IN  (
    SELECT tweet_campaign.tweet_id
    FROM Campaign
    INNER JOIN tweet_campaign ON tweet_campaign.campaign_id = Campaign.id
    WHERE Campaign.name != '_SEARCH_QUERY'
);

SELECT COUNT(*)
FROM Tweet
WHERE Tweet.id NOT IN  (
    -- Tweets which do have labels, other than base label.
    SELECT tweet_campaign.tweet_id
    FROM Campaign
    INNER JOIN tweet_campaign ON tweet_campaign.campaign_id = Campaign.id
    WHERE Campaign.name != '_SEARCH_QUERY'
);
