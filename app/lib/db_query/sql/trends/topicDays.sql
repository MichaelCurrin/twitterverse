/**
 * Topics which trended at the country level in the past 7 days.
 * Within the same period, do a count of how places mentioned the topic
 * and how many days the trended in at least once place.
 * Sort by a combined total of the two measures.
 *
 * TODO: Min timestamp method
 */

SELECT
    topic,
    COUNT(DISTINCT(place_id)) AS place_cnt,
    COUNT(DISTINCT(date)) AS date_cnt
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
ORDER BY place_cnt + date_cnt DESC
;
