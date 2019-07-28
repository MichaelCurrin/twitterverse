/*

Select all Countries and their Continent parents, showing trending topic data
for those Countries, broken down by date.

WARNING: `WITH` statements are only possible in SQlite3 version 3.8.3+.
PythonAnywhere only has 3.8.2 at time of writing therefore it fails to
run there.
See https://stackoverflow.com/questions/27539139/why-cant-i-use-with-statement-in-sqlite3


The first CTE as distinct_trends is used for getting distinct topics
trending by day and place.

The country_trends CTE used the previous CTE to show trends in countries,
including additional country data looked up.

This is done again for town_trends.

The results of the last two CTEs are combined in a single output table
using UNION. One can then filter by place_type column to get only the
'country' or 'town' rows in the table.

Sub query notes:
* Parent name and place name come from table B, while date and topic come from
    table A.
* Table A is distinct combinations of trend records on a date for a place.
* Table B is the Country where the trend occurred, including the name of the
country and the name of its continent parent.

*/

WITH distinct_trends AS (
    SELECT DISTINCT
        DATE(timestamp) AS date,
        topic,
        place_id
    FROM Trend
),

country_trends AS (
    SELECT
        'country' AS place_type,
        place_name,
        parent_name,
        date,
        topic
    FROM distinct_trends AS A
    INNER JOIN (
        SELECT
            P.id,
            P.name AS place_name,
            P2.name AS parent_name
        FROM Country AS C
        INNER JOIN Place AS P ON (P.id = C.id)
        INNER JOIN Place AS P2 ON (P2.id = C.continent_id)
        ) AS B ON B.id  = A.place_id
    ORDER BY
        parent_name,
        place_name,
        date,
        topic
),

town_trends AS (
    SELECT
        'town' AS place_type,
        place_name,
        parent_name,
        date,
        topic
    FROM distinct_trends AS A
    INNER JOIN (
        SELECT
            P.id,
            P.name AS place_name,
            P2.name AS parent_name
        FROM Town AS T
        INNER JOIN Place AS P ON (P.id = T.id)
        INNER JOIN Place AS P2 ON (P2.id = T.country_id)
    ) AS B ON B.id  = A.place_id
    ORDER BY
        parent_name,
        place_name,
        date,
        topic
)

SELECT *
FROM country_trends

UNION

SELECT *
FROM town_trends;
