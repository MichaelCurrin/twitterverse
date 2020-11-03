/**
 * Select all places and trending topic data for those places, broken down by
 * date.
 *
 * WOEID is used to separate places which may have the same name (as some towns
 * do).
 *
 */

SELECT
    B.child_name AS place_type,
    B.woeid,
    B.name AS place_name,
    A.date,
    A.topic
FROM (
    SELECT DISTINCT
        DATE(timestamp) AS date,
        topic,
        place_id
    FROM Trend
) AS A
INNER JOIN Place AS B ON (B.id = A.place_id)
;
