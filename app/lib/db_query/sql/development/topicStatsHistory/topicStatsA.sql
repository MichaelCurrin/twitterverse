

/*
Use subquery for min timestamp based on this article.
    https://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/
*/

/*
inner part of next query
*/
SELECT id, topic, DATE(timestamp), MIN(timestamp) AS min_timestamp
FROM Trend
GROUP BY topic, DATE(timestamp);


SELECT T.topic, DATE(T.timestamp) AS date, T.volume
FROM Trend AS T
INNER JOIN (
        SELECT id, topic, DATE(timestamp), MIN(timestamp) AS min_timestamp
        FROM Trend
        GROUP BY topic, DATE(timestamp)
        ) AS X
    ON T.id = X.id
LIMIT 10;

/*
This has been simplied above to use IDs instead.

SELECT T.topic, DATE(T.timestamp) AS date, T.volume
FROM Trend AS T
INNER JOIN (
        SELECT topic, DATE(timestamp), MIN(timestamp) AS min_timestamp
        FROM Trend
        GROUP BY topic, DATE(timestamp)
        ) AS X
    ON T.topic = X.topic AND T.timestamp = X.min_timestamp
LIMIT 10;
*/

/* Alt style closer to article but not so easy to reuse.
SELECT T.topic, DATE(T.timestamp) AS date, T.volume
FROM (
    SELECT topic, DATE(T.timestamp), MIN(timestamp) AS min_timestamp
    FROM Trend
    GROUP BY topic, DATE(T.timestamp)
    ) AS Y
INNER JOIN Trend AS T ON T.topic = Y.topic AND T.timestamp = Y.min_timestamp
LIMIT 10;
*/

/*
Subquery makes place only appear once on a day for a topic.
We don't care which timestamp for date since we don't need
volume here.
But order by is useful for when doing the inner query alone.
*/
SELECT Y.topic, Y.date, COUNT(Y.place_id) AS place_count
FROM (
    SELECT DISTINCT topic, DATE(timestamp) AS date, place_id
    FROM Trend
    ORDER BY place_id, topic, date
    ) AS Y
GROUP BY Y.topic, Y.date
ORDER BY COUNT(Y.place_id) DESC
LIMIT 10;


