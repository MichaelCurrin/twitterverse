-- or allow null but set null last
SELECT topic, volume, DATE(timestamp)
FROM Trend
WHERE place_id = 1 AND volume IS NOT NULL
ORDER BY DATE(timestamp) DESC, volume DESC
LIMIT
50;

-- possibly count days topic has been trending and most recent day it is trending.
-- most consecutive days? most recent streak?
