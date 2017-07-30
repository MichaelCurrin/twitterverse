/*
There were issues moving this to topic stats because doing two
inner joins in a row doesn't look right and it's not natural to do count
of countries and towns separately when using distinct.
*/


/*
Join on Country table which necessarily filters to countries only but means
we can't use name without doing a join on Place too.
*/
SELECT Trend.topic, Country.id
FROM Trend
INNER JOIN Country ON Country.id = Trend.place_id
LIMIT 10;

SELECT '' AS '--';


SELECT Trend.topic, Town.id
FROM Trend
INNER JOIN Town ON Town.id = Trend.place_id
LIMIT 10;

SELECT '' AS '--';

/*
#####################
*/

/*
Select trends for Town.
*/
SELECT Trend.topic, Place.id, Place.name, Place.child_name
FROM Trend
INNER JOIN Place ON Place.id = Trend.place_id
WHERE Place.child_name = 'Town'
LIMIT 10;

SELECT '' AS '--';


/*
Select trends for Country.
*/
SELECT Trend.topic, Place.id, Place.name, Place.child_name
FROM Trend
INNER JOIN Place ON Place.id = Trend.place_id
WHERE Place.child_name = 'Country'
LIMIT 10;


/*
Subquery

SELECT *
FROM Trend
WHERE place_id IN (
    SELECT id
    FROM Place
    WHERE child_name = 'Country'
    )
LIMIT 10;
*/

SELECT '' AS '--';


/*
#####################
*/

/*
Basic
*/

/*
SELECT id
FROM Place
WHERE child_name = 'Country'
LIMIT 10;

SELECT '' AS '--';

SELECT *
FROM Place
WHERE child_name = 'Town'
LIMIT 10;
*/
