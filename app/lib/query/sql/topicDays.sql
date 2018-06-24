/**
 * Topics which trended at the country level in the past 7 days, with a
 * count of how many days it trended.
 *
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
    WHERE date >= DATE('NOW', '-7 DAYS')
) AS T
INNER JOIN Country ON Country.id = T.place_id
GROUP BY topic
ORDER BY days ASC
;
