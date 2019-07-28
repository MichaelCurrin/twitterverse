/*
    Report for getting topics with count of towns or countries mentioning
    them, broken down by date.

    This is an alternative to part of the calc in topicStats which
    could be faster by not using CASE. Though may be less accurate with the
    limited joining method. Also this has not been tested as part of the full
    topicStats query.
*/


-- Get count of places by topic and date for the place types.
WITH A AS (
    SELECT Trend.topic, DATE(Trend.timestamp) as date, Place.child_name, COUNT(DISTINCT(Trend.place_id)) AS cnt
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    GROUP BY topic, date, child_name
)

/*  
    Use query A and split into Town and Country but combine overlapping date
    and topic rows.

    FULL OUTER JOIN is not supported in SQLite, so we use town as a starting
    point (since something can trend in a town without trending in a country)
    and then add countries.
*/

SELECT B.date, B.topic, COALESCE(C.cnt, 0) AS country_count, COALESCE(B.cnt, 0) AS town_count
FROM (
    SELECT * 
    FROM A
    WHERE child_name = 'Town'
) AS B
LEFT OUTER JOIN (
    SELECT * 
    FROM A
    WHERE child_name = 'Country'
) AS C ON C.topic = B.topic AND C.date = B.date
ORDER BY B.date DESC, B.topic
;
