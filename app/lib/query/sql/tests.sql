/*
SELECT topic,
     place_id,
     COUNT(place_id)
FROM Trend
GROUP BY topic, place_id
HAVING COUNT(place_id) > 1
ORDER BY topic;
*/

/*
SELECT Trend.topic
       ,MIN(Trend.timestamp) as Date
       ,Trend.volume
FROM Trend
ORDER BY Trend.timestamp;
*/


/*

SELECT Z.topic, COUNT(Z.date)
FROM (
	SELECT X.topic, X.date, COUNT(X.place_id)
	FROM (
	    SELECT DISTINCT topic, DATE(timestamp) AS date, place_id
	    FROM Trend
	    ORDER BY place_id, topic, date
	    ) AS X
	GROUP BY X.topic, X.date
	ORDER BY COUNT(X.place_id) DESC
)
AS Z
GROUP BY Z.topic
HAVING COUNT(Z.date) > 1;
*/
