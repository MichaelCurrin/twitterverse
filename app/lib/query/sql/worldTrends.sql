/*
World trend query.

Get trending data for the world with volume and time data.
Ignores possible duplicate values on recorded over the same day by 
picking the first one and the volume for that record. Timestamp is used to get the earliest for the day but then ignored at the outer query.
*/

SELECT date, volume, topic
FROM (
    SELECT DATE(A.timestamp) AS date, MIN(A.timestamp), volume, topic
    FROM (
        SELECT Trend.timestamp, Trend.volume, Trend.topic
        FROM Trend
        INNER JOIN Place ON Place.id = Trend.place_id
        WHERE Place.woeid = 1
        ORDER BY Trend.timestamp ASC
    ) A
    GROUP BY date, topic
);

