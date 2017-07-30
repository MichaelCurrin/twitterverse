/*
Usage:
    $ sqlite3 ../../../var/db.sqlite -header < topicStats.sql

Select all trend topics, with place and volume stats by day.

Calc to get volume    
    See subquery X. Get the earliest record for a topic on a day (ignoring
    later records or records for other places) and use an inner join to filter 
    to these records. Then we can use the volume. This repeats for all topics.
    
    We assume the scheduled cron job should start early in the day and we ignore
    any records later in the day. Therefore insertion jobs run later in the day
    automatically or by a user will NOT affect the stats earlier in the day.
    Note that the volume is for the previous 24 hours, so a record around
    midnight will actually be for the previous day.
    
    Use subquery for min timestamp based on this article.
        https://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/

Calc to get place count
    See subqueries Y and Z. Get distinct place IDs for a day then count the
    places for that day. Repeats for all topics.
   
    The distinct subquery WITHIN Y makes place only appear once on a day 
    for a topic. We don't care which timestamp we use on a date since we don't
    need to tie to volume here.
*/

/*This counts towns and countries equally*/

SELECT T.topic, DATE(T.timestamp) AS date, Z.place_count, T.volume
FROM Trend AS T
INNER JOIN (
        SELECT id, topic, DATE(timestamp), MIN(timestamp) AS min_timestamp
        FROM Trend
        GROUP BY topic, DATE(timestamp)
        ) AS X
    ON T.id = X.id
INNER JOIN (
        SELECT Y.topic, Y.date, COUNT(Y.place_id) AS place_count
        FROM (
            SELECT DISTINCT topic, DATE(timestamp) AS date, place_id
            FROM Trend
            ORDER BY date
            ) AS Y
        GROUP BY Y.topic, Y.date
    ) AS Z
    ON T.topic = Z.topic AND DATE(T.timestamp) = Z.date;

