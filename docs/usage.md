# Usage

This readme includes instructions for using aspects of the app in this repo.

All code blocks start from the `app` directory unless specified otherwise.

```bash
$ cd <PATH_TO_REPO>/app/
```

Using `--help` on python scripts to see their usage instructions.

If you are not familiar with running scheduled cron jobs with `crontab`, I recommended researching how to use it. See the cron tutorial in my [learn-bash](https://github.com/MichaelCurrin/learn-bash/tree/master/learn-bash) repo.


## Work with the database

Get a summary of DB stats.

```bash
$ python -m lib.query.schema.tableCounts
$ python -m lib.query.schema.preview
```

How to select data from the DB.

Below are instructions for how to execute SQL queries in python - see the [lib.query](/lib/db_query) directory or [SQLObject documentation](http://www.sqlobject.org/) for more info.

```python
>>> from lib import database as db
>>> # Prepare query to get all Place reocrds.
>>> res = db.Place.select()
>>> print res.count()
# => integer
>>> # Print first 10 items.
>>> for x in res.limit(10):
...     print x
>>>
# => Place objects

>>> # Get country with ID 120.
>>> c = db.Country.get(120)

>>> # If you have Trend data from a cronjob or other method, select it.
>>> res = db.Trend.select(db.Trend.q.volume > 10000)
>>> # View the SQL statement.
>>> str(res)
>>> # View the result objects returned. Apply list function to get all data from the generator.
>>> list(res)
```


## Setup Trend cron jobs

One of the main benefits of this app is getting tweet data on schedule, so that queries can be performed against them. This section deals with setting that up at the Trend level, to get trending topic data for watched places.

### Simple

Run a simple insert for trends of a single country and its towns with a bash script and an optional argument for a country to override the configured default. See instructions in [trends_default_country.sh](https://github.com/MichaelCurrin/twitterverse/blob/master/tools/cron/trends_default_country.sh). Run it manually or as a cron job.

### Advanced

Do trend queries for a managed queue of places, using PlaceJob table in [models/cron_jobs.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/cron_jobs.py). Records in the table can be viewed and modified using the [manager/jobs.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/manage/jobs.py) script. Follow the prompts to add configured data.

```bash
$ ./utils/manage/jobs.py -i
```

Then test the [PlaceJob scheduler](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/insert/run_place_job_schedule.py) manually.

```bash
$ ./utils/insert/run_place_job_schedule.py
```

To run the python script above, add [tools/trends_place_job](https://github.com/MichaelCurrin/twitterverse/blob/master/tools/cron/trends_place_job.sh) to your crontab, as per usage instructions in that file.


## Utilities

See the [utils](https://github.com/MichaelCurrin/twitterverse/tree/master/app/utils) directory for scripts to run from the terminal.

_TODO: Split out utilities, tools and cron jobs between here and another file or files._


### Search tweets

Use the Twitter Search API and store results in the Tweet and Profile tables. Tweet records are assigned a configured campaign name to indicate they were added by a search.


#### Ad hoc query

Example

```bash
$ ./utils/insert/search_and_store_tweets.py \
'to:pyconza OR from:pyconza OR pyconza OR pyconza17 OR za.pycon.org'
```

Or

```bash
$ TERMS='"MamaCity Improv" OR MCIF OR MamaCityImprovFest OR MamaCityIF'\
' OR mamacityimprovfestival.nutickets.co.za OR mamacityimprovfest.com'
$ ./utils/insert/search_and_store_tweets.py "$TERMS"
```

View the logs for more verbose output.

Use the `--no-persist` flag to not store data to the database and print the simplified tweet data (count, handle and message) to the terminal.

#### Stored query

Add a search query to the database to make it easy to reuse. See instructions below.

View store campaigns with counts of locally stored tweets.

    $ ./utils/manage/campaign.py --all
        Campaign                  |  Tweets | Query
    ------------------------------+---------+-------------------------
    1. Black Friday               |   1,234 | #BlackFriday
    2. ...

Create or update a campaign.

    $ ./utils/manage/campaign.py --campaign 'Foo bar' \
        --query '"Foo Bar" OR #FooBar OR @Baz'
    Created Campaign: Foo bar | "Foo Bar" OR #FooBar OR @Baz

Search tweets matching a campaign's query. Tweets are stored agains the campaign.

    $ ./utils/insert/search_and_store_tweets.py \
        --campaign 'Foo bar' --pages 1000
    Search query: #foo OR #bar
    Generating Application-Only Auth...
    [START] searchStoreAndLabel
    Starting Search. Expected pages: 100,000. Expected tweets: 10,000,000.
    Stored so far: 100
    Stored so far: 200

#### Scale

The [insert/search_and_store_tweets.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/insert/search_and_store_tweets.py) utility script can fetch and store hundreds of tweets in a few seconds, depending on your machine and internet speed course. This method uses the ORM - multiple insert and get queries are made to get a single tweet into the DB. This does not scale well though as it adds to the total time of the query. This is inconvenient especially if you have a lot of separate and high volume searches to do regularly (such as daily or several times a day).

The [extract/search.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/extract/search.py) utility script is much faster as it writes data out to a CSV at intervals. The logic to insert that data into the DB using a single SQL statement in a transaction (to rollback on failure) must still be created and documented here.

Note that there is still an upper limit on the number of tweets to be fetched in 15 min period, due to the API rate limits. So even if you use the more efficient method, you might find that you hit the API limit and the script has to wait a few minutes before it can retry, which is similar to just running slower and more continuously. The tradeoffs still have to be investigated.

### Lookup tweets

Fetch and store tweet objects from the API by providing _tweet IDs_, either from a previous API query or by looking at the ID of a tweet in the browser. Note that this ID is called a _GUIDs_ within the model.

Example

```bash
$ ./utils/insert/lookup_and_store_tweets.py \
    1234566915281 125115773299 325882358325
```


## Create CSV reports

Execute SQL statements and store output as CSV file.

Use the `-csv` flag to get comma-separated values of rows and use `-header` to include the header.

Examples:

-   ```bash
    $ cat lib/query/sql/tweets/allTweets.sql | sqlite3 -csv -header \
        var/db.sqlite > var/reporting/fileName.csv
    ```
-   ```
    $ sqlite3 -csv -header var/db.sqlite < lib/query/sql/tweets/allTweets.sql \
        > var/reporting/fileName.csv
    ```


## Setup Tweet cron jobs

Get tweet data for watched profiles, on schedule.

The focus of this area of this application is to identify the most influential accounts on Twitter and to store data on Profiles and some of their Tweets. This data can be built up as historical data which can be filtered and visualized based on a requirement. Note that while search data has a limited 7-day window, it is possible to do a sequence of API requests to retrieve  Tweets for a single user going back a few years.


### 1. Create screen names in text files

If you prefer to compile a list of handles using the command-line instead, skip to step 2.

Scrape popular Twitter account screen names from [socialblade.com](https://socialblade.com) and add text files with appropriate names. This process takes a few seconds. It is described here as a manual process to be run once-off or occasionally, though it could be automated.

The source site has static HTML with the top screen names across four categories, allowing a view either top 10 or top 100. Note that some categories like most tweets include Twitter accounts which are tests (they have test in the same) or bots (they offer a service to send Tweets to use on request of on schedule).

There will be some overlap in Twitter profiles appearing across the 4 lists, so even if you lookup four lists of 100 you will probably get slightly less than 400 unique profiles stored in your Profile table.

```bash
$ ./utils/influencer_scraper.py --help
```

Get 10 users in each category.

```bash
$ ./utils/influencer_scraper.py short
```

    Output dir: <PATH_TO_REPO>/app/var/lib/influencer_scraper
    Wrote: followers-short-2017-12-03.txt
    Wrote: following-short-2017-12-03.txt
    Wrote: tweets-short-2017-12-03.txt
    Wrote: engagements-short-2017-12-03.txt

The contents of the files are used as input for the next step. There may be duplication of users across files, but this is fine as the user can be added to the DB under two Category labels.

The files can be created or maintained by hand as well.

_TODO: Add sample file or steps to hand compile text file._

### 2. Create Profile records

Use the generated text files of screen names from above, or input handles by hand.

In one command, the following steps happen:

1. Lookup profile data on the Twitter API using given handles.
2. Create Profile records in the DB.
3. Assign Category labels to the Profile records.

Tips:

- The screen names provided to the API are not case-sensitive.
- Note the the `--no-fetch` command if you want to experiment and print without storing data. See help:
    ```bash
    $ ./utils/insert/fetch_profiles.py --help
    ```

Fetch a list of profiles and assign categories, using the fetch profiles utility. A Category is a list of Profiles which makes them easier to fetch tweets for and to report on. You can have as many Category groups as you like.

- Provide handles in text file. An example file path is used below.
    ```bash
    $ # Preview.
    $ ./utils/insert/fetch_profiles.py --no-fetch --file var/lib/influencer_scraper/following-short-2017-12-03.txt
    6BillionPeople
    ArabicBest
    MixMastaKing
    ...
    ```
    ```bash
    $ # Assign custom category (created if it does not exist) and the system influencers label.
    $ ./utils/insert/fetch_profiles.py --file var/lib/influencer_scraper/following-short-2017-12-03.txt \
        --category 'Top Following' --influencers
    ```
- Provide handles as arguments.
    ```bash
    $ # Screen names as command-line list.
    $ ./utils/insert/fetch_profiles.py --category 'My watchlist' --list foo bar bazz
    ```

View the results using the _Category Manager_ utility. A category of thousands of profiles may take a few seconds to read and print.

```bash
$ ./utils/manage/categories.py view --profiles
1. Top Following   10 profiles
   - @6BillionPeople       | MarQuis Trill | Bitcoin Ethereum Litecoin Investor
   - @ArabicBest           | الاكثر تاثيرا
   - @MixMastaKing         | MEGAMIX CHAMPION
   ...

2. _TOP_INFLUENCER 10 profiles
   - @6BillionPeople       | MarQuis Trill | Bitcoin Ethereum Litecoin Investor
   - @ArabicBest           | الاكثر تاثيرا
   - @MixMastaKing         | MEGAMIX CHAMPION
   ...

3. My watchlist        2 profiles
   - @foo             | Foo
   - @bar             | Mr Bar
   - @bazz            | bazz
...
```

### 3. Fetch Tweets

Fetch and store Tweets in the db, using one of two methods.

Lookup by Profile vs doing a Search - note that if you know a Twitter user's handle or ID, you can get all their tweets historically, back to some years ago. And if you know a tweet's ID, you can fetch that tweet to create or update it locally. But, if you use the Search API to find tweets by a user or about a topic, Twitter limits you to only get tweets created in the _past week_.

#### Fetch Profiles in Categories

Look up and store Tweets for Profiles within a Category, using fetched Profiles and assigned Categories from the previous step. The Category filter allows fetching Tweets for just a certain category (e.g. top influencers, an industry or a custom watch list), to avoid fetching unnecessary data for all Profiles in database.

This step can be done once off to get Tweets for Profiles in certain Categories, perhaps with Tweets per Profile set to 1000 to get a few years of Tweets for each Profile. Then, this could be added to a crontab on a daily or weekly schedule so that reports will have recent Tweet data to work with.


```bash
$ ./utils/insert/fetch_tweets.py --help

$ ./utils/insert/fetch_tweets.py --categories 'My watchlist'
Fetching Tweets for 2 Profiles
...

$ # Get default number of tweets (200) for each Profile, for given Categories.
$ ./utils/insert/fetch_tweets.py -c 'Top Engagements' 'Top Followers'
Fetching Tweets for 197 Profiles
...

$ ./utils/insert/fetch_tweets.py --categories _TOP_INFLUENCER --tweets-per-profile 25 --verbose
Fetching Tweets for 364 Profiles
...
```

Note the script defaults to getting 200 most recent Tweets for each Profile (as this is one requested page of Tweets from the API). Even for Profiles which post 7 times a day, this would still give 4 weeks of activity. Therefore when the script runs at 200 Tweets per Profile, it will likely spend more time updating engagements on existing Tweets in the db than storing new Tweets, so the volume of Tweets stored locally will grow relatively slowly.

_TODO: write/improve crontab instructions in full. The influecer scraper is not a good candiate for crontab since it is best used when manually labelling new Profiles in the top 100 and the top 10 will likely be changing often but still in the added top 100. Consider updating all profiles with crontab, so bios and followers are kept up to date weekly, since the calls are inexpensive when not getting Tweets_

#### Fetch Tweets matching Search Query

See the Search Tweets section under Utilities.

Without knowing any Twitter handles, you can do a query against Search API.

- Use the _Search and Store Tweets_ utility for this.
    ```bash
    $ ./utils/insert/search_and_store_tweets.py -h
    ```
- Or use the extract search utility, which only writes to a CSV. This is detailed in the [Scale](#scale) section.


### 4. View the data

Scripts are available to get a sample of tweets and profiles in the database.

_TODO: Integrate these scripts as part of another utility or a main reporting utility. Consider if the limit should be made an optional flag for top_profiles and top_tweets, so default can be used as with top_words_

```bash
$ python -m lib.query.tweets.top_profiles 5
$ python -m lib.query.tweets.top_tweets 5

$ python -m lib.query.tweets.top_words --search 'phrase to search' --limit 20
$ python -m lib.query.tweets.top_words --search 'word' --filter
```

Use the category and campaign managers to see how Tweet or Profile data has been grouped.

```bash
$ ./utils/manage/categories.py --available
$ ./utils/manage/categories.py --profiles

$ ./utils/manage/campaigns.py --available
$ ./utils/manage/campaigns.py --tweets
```


## Streaming

If you just want to do a live stream of tweets to the console without storing data, then run the `stream.py` script.

You do not need the database setup steps. Just ensure you have your Twitter credentials setup in `app.local.conf`.

```bash
$ cd app
$ # See instructions on search query values.
$ ./utils/stream.py --help
```
