/*
    Get distinct place and topic combinations per day, ignoring multiple
    records on a day.
*/
SELECT DISTINCT place_id, DATE(timestamp) AS date, topic
FROM Trend;
