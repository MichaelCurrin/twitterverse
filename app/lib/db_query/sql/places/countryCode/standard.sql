/**
 * Get trending topic by day data for towns, countries and the world.
 *
 * Includes volume for the past 24 hours on the time the record was created.
 *
 * Country code is matched against each record, whether a town or country. The
 * records are then filtered by country code. If no country code value filter
 * is set or this is set to NULL, then Worldwide values from the Supername
 * table are included in the results. This is because the LEFT JOINs on Town
 *  and Country do not exclude the Supername IDs in the Place table.
 */

SELECT
    DATE(T.timestamp) AS date,
    Country.country_code,
    Place.child_name AS location_type,
    Place.name AS location_name,
    T.topic,
    CASE T.hashtag WHEN 1 THEN 'hashtag' ELSE 'phrase' END AS trend_type,
    T.volume AS global_volume
FROM Trend AS T
INNER JOIN (
    /**
     * In case there is more than one record for a location and topic pair
     * (due to fetching data more than once on a certain day), then get the
     * earlier record. So that when adding up volume across days we choose
     * the earliest record in the day (preferably close to midnight) and
     * and later records in the day which might overlap with the next day's
     * record are ignored.
     * If using PSQL then it would be shorter to use DISTINCT ON and
     * order by timestamp.
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
INNER JOIN Place ON (T.place_id = Place.id)
LEFT JOIN Town ON (Place.child_name = 'Town' AND Place.id = Town.id)
LEFT JOIN Country ON (Place.child_name = 'Town' AND Country.id = Town.country_id)
                  OR (Place.child_name = 'Country' AND Place.id = Country.id)
WHERE Country.country_code = 'ZA'
/**
 * For a small number of places within a country code, it is more readable
 * to arrange topics on the same day together, rather than looking at all
 * topics for each location.
 */
ORDER BY
    date,
    T.topic,
    location_type,
    location_name
