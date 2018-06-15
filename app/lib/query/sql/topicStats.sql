/*
Usage:
    $ cd app/lib/query/sql
    $ sqlite3 ../../../var/db.sqlite -header < topicStats.sql

Select all trend topics, with place and volume stats by day.

Calc to get volume
    See subquery X. Get the earliest record for a topic on a day (ignoring
    later records or records for other places) and use an inner join to filter
    to these records. Then we can use the volume. This repeats for all topics.

    We assume the scheduled cron job should start early in the day and we ignore
    any records later in the day. Therefore insertion jobs run later in the day
    automatically or by a user will NOT affect the stats earlier in the day.
    Note that the volume is for the previous 24 hours, so a record around
    midnight will actually be for the previous day.

    Use subquery for min timestamp based on this article.
        https://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/

Calc to get place count
    See subqueries Y and Z. Get distinct place IDs for a day then count the
    places for that day. Repeats for all topics.

    The distinct subquery WITHIN Y makes place only appear once on a day
    for a topic. We don't care which timestamp we use on a date since we don't
    need to tie to volume here.

    Instead of counting place IDs, we evaluate ID as a Country with 1 or 0 and
    add that column for count of countries, then do the same for Town.
    The high level group by does not need to consider volume aggregation
    method, since from the first inner join we've made sure there will only
    be one volume value for date and topic combination.

The overall results of the query have been tested by applying the following:
    SELECT SUM(countryCount), SUM(townCount)
    FROM (normalQuery);
*/

SELECT
    DATE(T.timestamp) AS date,
    T.topic AS topic,
    SUM(C.isCountry) AS country_count,
    SUM(C.isTown) AS town_count,
    T.volume AS global_volume
FROM Trend AS T
INNER JOIN (
    SELECT
        id,
        topic,
        DATE(timestamp),
        MIN(timestamp) AS min_timestamp
    FROM Trend
    GROUP BY topic, DATE(timestamp)
    ) AS A ON T.id = A.id
INNER JOIN (
    SELECT
        B.topic,
        B.date,
        CASE
            WHEN Country.id IS NOT NULL
            THEN 1
            ELSE 0
        END AS isCountry,
        CASE
            WHEN Country.id IS NULL
            THEN 1
            ELSE 0
        END AS isTown
    FROM (
        SELECT DISTINCT
            Trend.topic,
            DATE(Trend.timestamp) AS date,
            Trend.place_id
        FROM Trend
    ) AS B
    LEFT JOIN Country ON B.place_id = Country.id
) AS C ON T.topic = C.topic
      AND DATE(T.timestamp) = C.date
GROUP BY
    date,
    T.Topic
ORDER BY
    date,
    T.topic
