-- Compare this against topic volume query to see that it aggregates
-- from data here.

SELECT id, topic, DATE(timestamp) AS date, timestamp, volume
FROM Trend
ORDER BY topic, timestamp
;
