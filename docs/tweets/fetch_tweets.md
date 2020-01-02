# Fetch tweets
> Use search query or tweet IDs to fetch and store tweets.

`Tweet` records are never stored alone in the DB - they must reference a profile that exists in the `Profile` table.

## Search tweets

Fetch tweets matching a search query. This can be setup to run on schedule.

```bash
$ cd app
```

Without knowing any Twitter handles, you can do a query against Search API.

- Use the _Search and Store Tweets_ utility for this.
    ```bash
    $ ./insert/search_and_store_tweets.py -h
    ```
- Or use the extract search utility, which only writes to a CSV. This is detailed in the [Scale](#scale) section.


### Ad hoc query

Example

```bash
$ ./insert/search_and_store_tweets.py \
    'to:pyconza OR from:pyconza OR pyconza OR pyconza17 OR za.pycon.org'
```

Or

```bash
$ TERMS='"MamaCity Improv" OR MCIF OR MamaCityImprovFest OR MamaCityIF'\
' OR mamacityimprovfestival.nutickets.co.za OR mamacityimprovfest.com'
$ ./insert/search_and_store_tweets.py "$TERMS"
```

View the logs for more verbose output.

Use the `--no-persist` flag to not store data to the database and print the simplified tweet data (count, handle and message) to the terminal.

### Store and use query

Add a search query to the database to make it easy to reuse. See instructions below.

View store campaigns with counts of locally stored tweets.

    $ ./manage/campaign.py --all
        Campaign                  |  Tweets | Query
    1. Black Friday               |   1,234 | #BlackFriday
    2. ...

Create or update a campaign.

    $ ./manage/campaign.py --campaign 'Foo bar' \
        --query '"Foo Bar" OR #FooBar OR @Baz'
    Created Campaign: Foo bar | "Foo Bar" OR #FooBar OR @Baz

Search tweets matching a campaign's query. Tweets are stored agains the campaign.

    $ ./insert/search_and_store_tweets.py \
        --campaign 'Foo bar' --pages 1000
    Search query: #foo OR #bar
    Generating Application-Only Auth...
    [START] searchStoreAndLabel
    Starting Search. Expected pages: 100,000. Expected tweets: 10,000,000.
    Stored so far: 100
    Stored so far: 200

### Scale

The [insert/search_and_store_tweets.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/insert/search_and_store_tweets.py) utility script can fetch and store hundreds of tweets in a few seconds, depending on your machine and internet speed course. This method uses the ORM - multiple insert and get queries are made to get a single tweet into the DB. This does not scale well though as it adds to the total time of the query. This is inconvenient especially if you have a lot of separate and high volume searches to do regularly (such as daily or several times a day).

The [extract/search.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/extract/search.py) utility script is faster as it writes data out to a CSV at intervals. The logic to insert that data into the DB using a single SQL statement in a transaction (to rollback on failure) must still be created and documented here.

Note that there is still an upper limit on the number of tweets to be fetched in 15 min period, due to the API rate limits. So even if you use the more efficient method, you might find that you hit the API limit and the script has to wait a few minutes before it can retry, which is similar to just running slower and more continuously. The tradeoffs still have to be investigated.

## Lookup tweets
> Fetch tweets by ID.

Fetch and store tweet objects from the API by providing _tweet IDs_, either from a previous API query or by looking at the ID of a tweet in the browser. Note that this ID is called a _GUIDs_ within the model.

```bash
$ cd app/utils
```

View help.

```bash
$ ./insert/lookup_and_store_tweets.py --help
```

Example

```bash
$ ./insert/lookup_and_store_tweets.py 1234566915281 125115773299 325882358325
```
