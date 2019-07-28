/**
 *  Hashtags vs Phrase query
 *
 * Count volume of trend records which are hashtags or phrases. This does
 * not attempt to remove any possible repeat records on a day for the same place.
 *
 * Note that although trend.hashtag is a boolean, it is stored as 1 or 0
 * as SQLite does not handle boolean values TRUE and FALSE.
 * But the shorthand version of CASE allows for an easy truthy check.
 */
SELECT
    CASE WHEN hashtag THEN 'hashtag' ELSE 'phrase' END AS topic_type,
    COUNT(*)
FROM trend
GROUP BY topic_type
