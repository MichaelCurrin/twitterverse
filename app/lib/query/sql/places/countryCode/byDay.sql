/**
 * Get daily topic stats for all topics which trended in a chosen country.
 * Includes counts for the country name and selected city names.
 *
 * A value is also shown to indicate if the topic also trended at the
 * Worldwide level that day.
 *
 * The country name and city names are hardcoded as values. Each Trend table
 * record has one-hot (1 or 0) encoding applied to it and then those are
 * aggregated to get counts across days.
 *
 * Row dimensions are combinations of date and topic - those pairs will be
 * unique in the output since a column for location name is omitted. The
 * results are ordered by most recent first and then by topic (ignoring the
 * possible leading hash symbol).
 *
 * The country code is set in a WHERE condition, so that the topics are limited
 * to those which trended in the selected country and/or one of its cities.
 * Otherwise, topics which trended in other places would be shown and the one-
 * hot encoded place names could be all zero for a row.
 *
 * The global volume in the past 24 hours at the time is shown for the date
 * and topic. If the record is just after midnight, the value actual pertains
 * to the previous date. Also consider that due to timezone differences,
 * midnight at GMT is 12pm on that day for the East and 12pm on the previous
 * day for the West. This is a blend of both days. The 24-hour values in the
 * global_volume column in the results can be added by day for a specific
 * topic to give a cumulative sum by day or a total for the period, because
 * of how the trend records are scraped and then selected here.
 *
 * If a topic is trending in multiple places and data is scraped across
 * those data within a few minutes, then the volume values should be almost
 * identical across the places. Therefore it doesn't matter which place is used
 * to get a volume value.
 */

SELECT
    DATE(T.timestamp) AS date,
    T.topic,
    CASE T.hashtag WHEN 1 THEN 'hashtag' ELSE 'phrase' END AS is_hashtag,
    T.volume AS global_volume,

    SUM(CASE Place.name WHEN 'Worldwide' THEN 1 ELSE 0 END) AS worldwide,
    SUM(CASE Place.name WHEN 'South Africa' THEN 1 ELSE 0 END) AS south_africa,
    SUM(
        CASE Place.name WHEN 'Pretoria' THEN 1 ELSE 0 END
      + CASE Place.name WHEN 'Johannesburg' THEN 1 ELSE 0 END
      + CASE Place.name WHEN 'Cape Town' THEN 1 ELSE 0 END
      + CASE Place.name WHEN 'Durban' THEN 1 ELSE 0 END
      + CASE Place.name WHEN 'Port Elizabeth' THEN 1 ELSE 0 END
    ) AS city_count,

    SUM(CASE Place.name WHEN 'Pretoria' THEN 1 ELSE 0 END) AS pta,
    SUM(CASE Place.name WHEN 'Johannesburg' THEN 1 ELSE 0 END) AS jhb,
    SUM(CASE Place.name WHEN 'Cape Town' THEN 1 ELSE 0 END) AS cpt,
    SUM(CASE Place.name WHEN 'Durban' THEN 1 ELSE 0 END) AS dbn,
    SUM(CASE Place.name WHEN 'Port Elizabeth' THEN 1 ELSE 0 END) AS pe
FROM Trend AS T
INNER JOIN (
    /**
     * In case there is more than one record for a location and topic pair
     * (due to fetching data more than once on a certain day), then get the
     * earlier record. So that when adding up volume across days we choose
     * the earliest record in the day (preferably close to midnight) and
     * and later records in the day which might overlap with the next day's
     * record are ignored.
     */
    SELECT
        id,
        topic,
        place_id,
        DATE(timestamp) AS date,
        MIN(timestamp) AS min_timestamp
    FROM Trend
    GROUP BY topic, place_id, date
    ) AS A ON T.id = A.id
INNER JOIN Place ON T.place_id = Place.id
LEFT JOIN Town ON (Place.child_name = 'Town' AND Place.id = Town.id)
LEFT JOIN Country ON (Place.child_name = 'Town' AND Country.id = Town.country_id)
                  OR (Place.child_name = 'Country' AND Place.id = Country.id)
WHERE Country.country_code IN ('ZA', NULL)
GROUP BY
    date,
    is_hashtag,
    T.topic
ORDER BY
    date DESC,
    CASE T.hashtag WHEN 1 THEN SUBSTR(T.Topic, 2) ELSE T.topic END
