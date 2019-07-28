-- TODO: This can be used as reference or possibly split into separate files
-- if needed individually.

/*
    Includes profiles which do not have categories.
    A profile is repeated for each category it is in.
*/

SELECT category.name, profile.screen_name
FROM profile
LEFT OUTER JOIN profile_category ON profile.id = profile_category.profile_id
LEFT OUTER JOIN category ON profile_category.category_id = category.id
ORDER BY category.name, profile.name;

/*
    Includes profiles which do not have categories.
    A profile and tweet pair is repeated for each category the profile is in.
*/
SELECT
    category.name AS category_name,
    profile.screen_name AS profile_screen_name,
    tweet.message AS message
FROM tweet
LEFT OUTER JOIN profile ON tweet.profile_id = profile.id
LEFT OUTER JOIN profile_category ON profile.id = profile_category.profile_id
LEFT OUTER JOIN category ON profile_category.category_id = category.id
ORDER BY category.name, profile.name;


/*
    Count of tweets in each category.
*/
SELECT
    category.name AS category_name,
    COUNT(DISTINCT(tweet.message)) AS message
FROM tweet
LEFT OUTER JOIN profile ON tweet.profile_id = profile.id
LEFT OUTER JOIN profile_category ON profile.id = profile_category.profile_id
LEFT OUTER JOIN category ON profile_category.category_id = category.id
GROUP BY category_name
ORDER BY category.name;

/*
    Profiles with no category assigned.
*/

SELECT profile.id
FROM profile
WHERE profile.id NOT IN (SELECT profile_id FROM profile_category);
