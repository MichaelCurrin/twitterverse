/*
 * World trend query.
 *
 * Get trending data for the world with volume and time data.
 *
 * Ignores possible duplicate values on recorded over the same day by picking
 * the first one and the volume for that record. Timestamp is used to get the
 * earliest for the day but then ignored at the outer query.
 */

SELECT
    date,
    volume,
    topic
FROM (
    SELECT
        DATE(GlobalTrends.timestamp) AS date,
        MIN(GlobalTrends.timestamp),
        volume,
        topic
    FROM (
        SELECT
            Trend.timestamp,
            Trend.volume,
            Trend.topic
        FROM Trend
        INNER JOIN Place ON Place.id = Trend.place_id
        WHERE Place.woeid = 1
        -- TODO: Check if this is needed. See link to min timestamp and apply throughout this directory.
        ORDER BY Trend.timestamp ASC
    ) AS GlobalTrends
    WHERE date > DATE('NOW', '-2 DAYS')
    GROUP BY date, topic
)
ORDER BY volume, date DESC
;
