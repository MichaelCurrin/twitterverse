/**
 * Countries
 */
SELECT
    Place.name,
    Town.id
FROM Place
INNER JOIN Town ON Place.id = Town.id
ORDER BY name
