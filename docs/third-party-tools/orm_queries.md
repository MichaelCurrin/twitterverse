# ORM queries

Examples of queries to report on data in the database using the Python ORM.

## Setup

Necessary import as the model names in the project are available on the database module.

```python
>>> from lib import database as db
```

## Get tweets

Get all tweets.

```python
>>> all_tweets = db.Tweets.select()
>>> all_tweets.count()
56789
```

Get tweets for a campaign. This uses the `Tweet`, `Campaign` and `TweetCampaign` tables in a convenient way.

```python
>>> foo = db.Campaign.byName('foo')
>>> foo.tweets.count()
12345
>>> for t in foo.tweets:
...     print(t)
...
<Tweet 8224 guid=1210581223770333185 profileID=5167 createdAt='datetime.datetime...)' ...>
...
```


## Get places

```python
>>> # Prepare query to get all Place reocrds.
>>> results = db.Place.select()
>>> print(results.count())
# => integer
>>> # Print first 10 items.
>>> for x in results.limit(10):
...     print(x)
>>>
# ... => Place objects shown.
```

```python
>>> # Get by ID.
>>> db.Country.get(120)

>>> # Get by WOEID, which is an alternate ID.
>>> db.Place.byWoeid(1)

>>> # Get by name. This is not an alternate ID.
>>> c = db.Country.selectBy(name='South Africa').getOne()
```

## Get trends

```python
>>> # If you have Trend data from a cronjob or other method, select it.
>>> t = db.Trend.select(db.Trend.q.volume > 10000)
>>> # View the SQL statement.
>>> str(t)
>>> # View the result objects returned. Apply list function to get all data from the generator.
>>> list(t)
```
