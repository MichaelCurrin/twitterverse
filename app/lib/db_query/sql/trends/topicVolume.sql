/*
    Show each trending topic by day, with it's global volume for that day.

    Uses the earliest recorded volume for the day to avoid duplication.
    Volume from Twitter API is for stated the past 24 hours and is globally.
    The volume in the report may be null if it was below the threshold
    (around 10,000 tweets).

    We do not care about the place for this query, since the global volume
    value is almost identical same when getting volume for a topic for
    any location.
*/

SELECT
    B.topic,
    B.date,
    A.volume
FROM (
    SELECT
        id,
        topic,
        DATE(timestamp) AS date,
        MIN(timestamp) AS min_timestamp
    FROM Trend
    GROUP BY topic, date
) AS B
INNER JOIN Trend AS A ON A.id = B.id
ORDER BY B.topic, B.date
;
