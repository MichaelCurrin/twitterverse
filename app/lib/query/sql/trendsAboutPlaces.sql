/*
Select places talking about other places.
*/

-- Count unique place and topic combinations, ignoring time.
-- Self references as a boolean as sorted for true first.
SELECT place_name, 
       topic, 
       COUNT(*) AS cnt,
       CASE WHEN place_name = topic THEN 1 ELSE 0 END AS is_self_reference
FROM (
    SELECT DISTINCT
        Place.name AS place_name,
        Trend.topic,
        DATE(Trend.timestamp) AS date      
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    WHERE topic IN (SELECT name FROM Place)
) A
GROUP BY place_name, topic
ORDER BY is_self_reference DESC, cnt DESC
LIMIT 10;


-- Count how many times as place appeared as a topic in a place, regardless of time.
SELECT topic, COUNT(*) AS cnt
FROM (
    SELECT DISTINCT 
        Place.name AS place_name,
        Trend.topic,
        DATE(Trend.timestamp) AS date      
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    WHERE topic IN (SELECT name FROM Place)
) A
GROUP BY topic
ORDER BY cnt DESC
LIMIT 10;


-- By date.
SELECT *
FROM (
    SELECT DISTINCT Place.name AS place_name, Trend.topic, DATE(Trend.timestamp) AS date
           
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    WHERE topic IN (SELECT name FROM Place)
) B
LIMIT 10;


-- Count of days that place was mentioned by a place.
SELECT place_name, topic, COUNT(*) AS cnt
FROM (
    SELECT DISTINCT Place.name AS place_name, Trend.topic, DATE(Trend.timestamp) AS date
           
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    WHERE topic IN (SELECT name FROM Place)
) C
GROUP BY place_name, topic
ORDER BY cnt DESC
LIMIT 10;

