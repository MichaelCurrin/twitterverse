/**
 * Get distinct place and topic combinations per day, ignoring multiple
 * records on a day.
 */

SELECT DISTINCT
    DATE(timestamp) AS date,
    topic,
    place_id
FROM Trend
;
