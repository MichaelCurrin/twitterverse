/**
 *  Filter places query.
 *
 *  Select place data for countries matching given country filter or
 *  towns which have the filtered countries as parents.
 */


WITH selected_countries AS (
    SELECT
        Place.child_name,
        Place.name,
        Country.id AS place_id
    FROM Place
    INNER JOIN Country ON Place.id = Country.id
    WHERE Place.name IN ('South Africa')
),

selected_towns AS (
    SELECT
        Place.child_name,
        Place.name,
        Town.id AS place_id
    FROM Place
    INNER JOIN Town ON Place.id = Town.id
    INNER JOIN selected_countries ON Town.country_id = selected_countries.place_id
)

SELECT *
FROM selected_countries
UNION
SELECT *
FROM selected_towns
