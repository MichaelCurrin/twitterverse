/*
The following was used to test the source of a bug in aggretation.
A group by was moved to the appropriate level.
*/

SELECT DISTINCT Trend.topic, DATE(Trend.timestamp) AS date, Trend.place_id
    FROM Trend
 ;

SELECT topic, date, SUM(isCountry), SUM(isTown)
FROM (
    SELECT B.topic,
           B.date,
           CASE WHEN B.place_id IN (
                    SELECT id
                    FROM Country
                    )
                THEN 1
                ELSE 0
           END AS isCountry,
           CASE WHEN B.place_id NOT IN (
                    SELECT id
                    FROM Country
                    )
                THEN 1
                ELSE 0
           END AS isTown
    FROM (
        SELECT DISTINCT Trend.topic, DATE(Trend.timestamp) AS date, Trend.place_id
        FROM Trend
        ) AS B
    )
GROUP BY topic, date
;
