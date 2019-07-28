/*
These queries were used in development of topicStats query.
*/

SELECT SUM(isCountry), SUM(isTown)
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
    GROUP BY B.topic, B.date
)
;

/*
SELECT B.topic, B.date, COUNT(B.place_id) AS place_count
FROM (
    SELECT DISTINCT Trend.topic, DATE(Trend.timestamp) AS date, Trend.place_id
    FROM Trend
    INNER JOIN Town WHERE Town.ID = Trend.place_id
    ) AS B
GROUP BY B.topic, B.date
;
*/

