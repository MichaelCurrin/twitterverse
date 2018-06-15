/**
 *  Aggregate stats for topics in South Africa for entire available date range.
 *
 *  International stats uses all locations available but excludes South Africa.
 *  The local stats only uses South African locations.
 *
 *  In the result, international stats are shown against the list of topics
 *  already filtered to those which have trended in South Africa.
 *
 * Date difference in SQLite based on calculation here:
 *   http://greladesign.com/blog/2011/01/09/sqlite-calculate-difference-between-datetime-fields/
 */

WITH Place_Expanded AS (
    SELECT
        Place.id,
        Country.country_code,
        Place.child_name AS type,
        Place.name,
        -- 1 or 0 since no boolean.
        (Country.country_code = 'ZA') AS is_local
    FROM Place
    LEFT JOIN Town ON (Place.child_name = 'Town' AND Place.id = Town.id)
    -- Effectively limits all rows to Town and Country records only.
    INNER JOIN Country ON (Place.child_name = 'Town' AND Country.id = Town.country_id)
                       OR (Place.child_name = 'Country' AND Place.id = Country.id)
),

International_Stats AS (
    SELECT
        Trend.topic,
        DATE(MAX(Trend.timestamp)) AS intl_last_trended,
        DATE(MIN(Trend.timestamp)) AS intl_first_trended,
        COUNT(DISTINCT(DATE(Trend.timestamp))) AS intl_days_mentioned,
        MAX(Trend.volume) AS intl_highest_volume
    FROM Trend
    INNER JOIN Place_Expanded ON (Trend.place_id = Place_Expanded.id AND
                                  Place_Expanded.is_local = 0)
    GROUP BY Trend.topic
),

Local_Stats AS (
    SELECT
        Trend.topic,
        Trend.hashtag,
        DATE(MAX(Trend.timestamp)) AS local_last_trended,
        DATE(MIN(Trend.timestamp)) AS local_first_trended,
        COUNT(DISTINCT(DATE(Trend.timestamp))) AS local_days_mentioned,
        MAX(Trend.volume) AS local_highest_volume
    FROM Trend
    INNER JOIN Place_Expanded ON (Trend.place_id = Place_Expanded.id AND
                                  Place_Expanded.is_local = 1)
    GROUP BY Trend.topic
)

SELECT
    Local_Stats.topic,
    CASE Local_Stats.hashtag WHEN 1 THEN 'hashtag' ELSE 'phrase' END AS is_hashtag,

    CASE
        WHEN International_Stats.intl_last_trended IS NULL
        THEN 'local only'
        WHEN Local_Stats.local_last_trended = International_Stats.intl_last_trended
        THEN 'same time'
        WHEN Local_Stats.local_last_trended > International_Stats.intl_last_trended
        THEN 'local last'
        ELSE 'intl last'
    END AS stopped_trending,
    CAST(
         STRFTIME('%s', Local_Stats.local_last_trended) - STRFTIME('%s', International_Stats.intl_last_trended)
        AS REAL
    )/60/60/24 AS local_relative_stop_in_days,
    Local_Stats.local_last_trended,
    International_Stats.intl_last_trended,

    CASE
        WHEN International_Stats.intl_first_trended IS NULL
        THEN 'local only'
        WHEN Local_Stats.local_first_trended = International_Stats.intl_first_trended
        THEN 'same time'
        WHEN Local_Stats.local_first_trended < International_Stats.intl_first_trended
        THEN 'local first'
        ELSE 'intl first'
    END AS started_trending,
    CAST(
         STRFTIME('%s', Local_Stats.local_first_trended) - STRFTIME('%s', International_Stats.intl_first_trended)
        AS REAL
    )/60/60/24 AS local_relative_start_in_days,
    Local_Stats.local_first_trended,
    International_Stats.intl_first_trended,

    Local_Stats.local_days_mentioned,
    International_Stats.intl_days_mentioned,

    MAX(Local_Stats.local_highest_volume,
        International_Stats.intl_highest_volume) AS highest_volume
FROM Local_Stats
LEFT JOIN International_Stats ON (Local_Stats.topic = International_Stats.topic)
WHERE International_Stats.intl_first_trended IS NOT NULL
ORDER BY
    Local_Stats.local_last_trended DESC,
    CASE Local_Stats.hashtag
        WHEN 1 THEN SUBSTR(Local_Stats.topic, 2) ELSE Local_Stats.topic
    END
