-- For topics which have trended at world level, how many countries have ever talked about them.

SELECT topic, COUNT(*) AS cnt_countries
FROM (
    SELECT topic, name
    FROM Trend
    INNER JOIN Place ON Place.id = Trend.place_id
    WHERE Place.child_name = 'Country'
)
GROUP BY topic
ORDER BY cnt_countries DESC;

