/**
 * Topics with how many days it was trending in at least one country, in the past 7 days.
 */

SELECT
    topic,
    COUNT(topic) AS days
FROM (
    SELECT
        topic,
        DATE(Trend.timestamp) AS date,
        place_id
    FROM Trend
    WHERE date >= DATE('now', '-7 days')
) AS B
INNER JOIN Country ON Country.id = B.place_id
GROUP BY topic
ORDER BY days ASC
;
