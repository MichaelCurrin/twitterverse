# App Usage

This readme includes instructions for using aspects of the app in this repo.

All code blocks start from the `twitterverse/app/` directory unless specified otherwise. Using `--help` on python scripts to see their usage instructions.

If you are not familar with running scheduled cron jobs with `crontab`, I recommended researching how to use it. See the cron tutorial in my [learn-bash](https://github.com/MichaelCurrin/learn-bash/tree/master/learn-bash) repo.


## Work with the database

Get a summary of db stats.

```bash
$ python -m lib.query.schema.tableCounts
$ python -m lib.query.schema.preview
```

How to select data from the database. 

Below are instructions for how to execute SQL queries in python - see the `lib.query` directory or [SQLObject documentation](http://www.sqlobject.org/) for more info.

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

Run a simple insert for trends of a single country and its towns with a bash script and an optional argument for a country to override the configured default. See instructions in [trendDefaultCountry.sh](/tools/cron/trendsDefaultCountry.sh). Run it manually or as a cron job.


### Advanced

Do trend queries for a managed queue of places, using PlaceJob table in [cronJobs.py](/app/models/cronJobs.py). Records in the table can be viewed and modified using the [job manager](/app/utils/manage/jobs.py). Follow the prompts to add configured data.

```bash
$ ./utils/manage/jobs.py -i
```

Then test the [PlaceJob scheduler](/app/utils/insert/runPlaceJobSchedule.py) manually.

```bash
$ ./utils/insert/runPlacejobSchedule.py
```

To run the python script above, add [trendsPlaceJob.sh](/tools/cron/trendsPlaceJob.sh) to your crontab as per usage instructions in that file. It has been written as a bash script in order simplify handling of virtualenv and logging the output.


## Utilities

_TODO: Split out utilities, tools and cron jobs between here and another file or files._


### Search tweets

Use the Twitter Search API and store results in the Tweet and Profile tables. Tweet records are assigned a configured campaign name to indicate they were added by a search.

Example

```bash
$ ./utils/insert/searchAndStoreTweets.py \
'to:pyconza OR from:pyconza OR pyconza OR pyconza17 OR za.pycon.org'
```

Or

```bash
$ TERMS='"MamaCity Improv" OR MCIF OR MamaCityImprovFest OR MamaCityIF'\
' OR mamacityimprovfestival.nutickets.co.za OR mamacityimprovfest.com'
$ ./utils/insert/searchAndStoreTweets.py "$TERMS"
```


### Lookup tweets

Fetch tweet objects from the API with known Twitter API tweet IDs (referred to as _GUIDs_ within this repo) and store in Tweet and Profile tables.

Example

```bash
$ ./utils/insert/lookupAndStoreTweets.py 1234566915281 125115773299 325882358325
```


## Create CSV reports

Execute SQL statements and store output as CSV file.

Use the `-csv` flag to get comma-separated values of rows and use `-header` to include the header.

Example

```bash
$ cat lib/query/sql/tweets/allTweets.sql | sqlite3 -csv -header var/db.sqlite \
    > var/reporting/fileName.csv
```

Or

```
$ sqlite3 -csv -header var/db.sqlite < lib/query/sql/tweets/allTweets.sql \
    > var/reporting/fileName.csv
```


## Setup Tweet cron jobs

Get tweet data for watched profiles, on schedule.

The focus of this area of this application is to identify the most influencial accounts on Twitter and to store data on Profiles and some of their Tweets. This data can be built up as historical data which can be filtered and visualised based on a requirement. Note that while search data has a limited 7-day window, it is possible to do a sequence of API requests to retrieve  Tweets for a single user going back a few years.


### 1. Create screen names list

Scrape popular Twitter account screen names from socialblade.com and add text files with appropriate names. This process takes a few seconds. It is described here as a manual process to be run once-off or occasionally, though it could be automated.

The source site has static HTML with the top screen names across four categories, allowing a view either top 10 or top 100. Note that some categories like most tweets include Twitter accounts which are tests (they have test in the same) or bots (they offer a service to send Tweets to use on request of on schedule).

```bash
$ ./utils/influencerScraper.py --help
```

Get 10 users in each category.

```bash
$ ./utils/influencerScraper.py short
Output dir: /PATH/TO/twitterverse/app/var/lib/influencerScraper
Wrote: followers-short-2017-12-03.txt
Wrote: following-short-2017-12-03.txt
Wrote: tweets-short-2017-12-03.txt
Wrote: engagements-short-2017-12-03.txt
```

The contents of the files are used as input for the next step. There may be duplication of users across files, but this is fine as the user can be added to the db under two Category labels.

The files can be created or maintained by hand as well.


### 2. Create Profile records

Use the generated text files of screen names to fetch data from Twitter API and create Profile records in the local db. The screen names are not case sensitive.

Use either the path to a file, or enter screen names as arguments.

```bash
$ ./utils/insert/fetchProfiles.py --help
```

```bash
$ # Preview the screen names input.
$ ./utils/insert/fetchProfiles.py --no-fetch --file var/lib/influencerScraper/following-short-2017-12-03.txt
6BillionPeople
ArabicBest
MixMastaKing
...
$ # Screen names from path to text file and assign to Category names.
$ ./utils/insert/fetchProfiles.py --file var/lib/influencerScraper/following-short-2017-12-03.txt \
    --influencers --category 'Top Following'
$ # Screen names as command-line list.
$ ./utils/insert/fetchProfiles.py --list 6BillionPeople ArabicBest MixMastaKing
```

View the results.

```bash
$ ./utils/manage/categories.py --profiles
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
```

### 3. Fetch Tweets by Profiles

Look up and store Tweets for Profiles within a Category, using Profile data created in previous step. The Category filter allows fetching Tweets for just a certain category (e.g. top influencers, an industry or a custom watch list), to avoid fetching unnecessary data for all Profiles in database.

This step can be done once off to get Tweets for specified users, but it is recommended to automated this in order to build up a history of activity of watched Profiles. 

```bash
$ ./utils/insert/fetchTweets.py --help

$ ./utils/insert/fetchTweets.py --categories _TOP_INFLUENCER --tweets-per-profile 25 --verbose
```

_TODO: write crontab instructions and possibly a .sh script for this section, covering tweets and optionally profiles (influencer scraping?). Profiles will be updated automatically when updating tweets, but a separate script to update Profiles for bio etc info is still useful and can be done for all Profiles cheaply in fetching and storing cost, compared with tweets for all profiles._

### 4. View the data

Scripts are available to get a sample of tweets and profiles in the database.

_TODO: Integrate these scripts as part of another utility or a main reporting utility. Consider if the limit should be made an optional flag for topProfiles and topTweets, so default can be used as with topWords_

```bash
$ python -m lib.query.tweets.topProfiles 5
$ python -m lib.query.tweets.topTweets 5

$ python -m lib.query.tweets.topWords --search 'phrase to search' --limit 20
$ python -m lib.query.tweets.topWords --search 'word' --filter
```

Use the category and campaign managers to see how Tweet or Profile data has been grouped.

```bash
$ ./utils/manage/categories.py --available
$ ./utils/manage/categories.py --profiles

$ ./utils/manage/campaigns.py --available
$ ./utils/manage/campaigns.py --tweets
```


## Web app

Run the CherryPy web server.

This has not been implemented yet.

```bash
# To be completed.
```
