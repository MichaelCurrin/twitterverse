/**
 * Countries
 */
SELECT
    Place.name,
    Country.id
FROM Place
INNER JOIN Country ON Place.id = Country.id
ORDER BY name
