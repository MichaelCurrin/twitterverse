/**
 * Show towns and countries in one list. Only these will have trending records
 * against them, therefore other types are ignored here.
 * Includes the continent and country code for each result row.
 */

SELECT
    Place.woeid,
    Continent_Expanded.name AS continent,
    Country.country_code,
    Place.child_name AS type,
    Place.name
FROM Place
LEFT JOIN Town ON (Place.child_name = 'Town' AND Place.id = Town.id)
-- Effectively limits all rows to Town and Country records only.
INNER JOIN Country ON (Place.child_name = 'Town' AND Country.id = Town.country_id)
                   OR (Place.child_name = 'Country' AND Place.id = Country.id)
LEFT JOIN (
    SELECT
        Continent.id,
        Place.name
    FROM Place
    INNER JOIN Continent ON (Place.id = Continent.id)
) AS Continent_Expanded ON Country.continent_id = Continent_Expanded.id
