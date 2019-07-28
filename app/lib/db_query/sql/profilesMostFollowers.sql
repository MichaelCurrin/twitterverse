/**
 * Twitter Profiles, ordered by highest followers first.
 */

SELECT
    screen_name,
    name,
    verified,
    followers_count,
    statuses_count,
    location,
    description
FROM Profile
ORDER BY followers_count DESC;
