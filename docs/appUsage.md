# App Usage

This readme includes instructions for using aspects of the app in this repo.

All code blocks start from the `twitterverse/app/` directory unless specified otherwise. Using `--help` on python scripts to see their usage instructions.

If you are not familar with running scheduled cron jobs with `crontab`, I recommended researching how to use it. See the cron tutorial in my [learn-bash](https://github.com/MichaelCurrin/learn-bash/tree/master/learn-bash) repo.


## Work with the database.

Get a summary of db stats.

```bash
$ python -m lib.query.schema.tableCounts
$ python -m lib.query.schema.preview
```

How to select data from the database. 

Below are instructions for how to execute SQL queries in python - see the `lib.query` directory or SQLObject documentation for more info.

```python
$ cd app
$ python
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

Run a simple insert for trends of a single country and its towns with a bash script and an optional argument for a country to override the configured default. See instructions in [trendDefaultCountry.sh](../tools/cron/trendsDefaultCountry.sh). Run it manually or as a cron job.


### Advanced

Do trend queries for a managed queue of places, using PlaceJob table in [cronJobs.py](../app/models/cronJobs.py). Records in the table can be viewed and modified using the [job manager](../app/utils/jobManager.py). Follow the prompts to add configured data.

```bash
$ ./utils/jobManager.py -i
```

Then test the [PlaceJob scheduler](../app/utils/insert/runPlacejobSchedule.py) manually.

```bash
$ ./utils/insert/runPlacejobSchedule.py
```

To run the python script above, add [trendsPlaceJob.sh](../tools/cron/trendsPlaceJob.sh) to your crontab as per usage instructions in that file. It has been written as a bash script in order simplify handling of virtualenv and logging the output.


## Utilities

TODO: Split out utilities, tools and cron jobs between here and another file or files.


### Search tweets

Example

```bash
$ TERMS='to:pyconza OR from:pyconza OR pyconza OR pyconza17 OR za.pycon.org'
$ # another example to search.
$ TERMS='"MamaCity Improv" OR MCIF OR MamaCityImprovFest OR MamaCityIF OR mamacityimprovfestival.nutickets.co.za OR mamacityimprovfest.com'
$ ./utils/insert/searchAndStoreTweets.py $TERMS
```


### Lookup tweets

Fetch tweet objects from the API with known Twitter API tweet IDs, referred to as GUIDs within this repo.

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
# OR
$ sqlite3 -csv -header var/db.sqlite < lib/query/sql/tweets/allTweets.sql \
    > var/reporting/fileName.csv

```


## Setup Tweet cron jobs

Get tweet data for watched profiles, on schedule.

### 1. Create screen names list

Scrape popular Twitter account screen names from a site and add to a text file with today's date in filename. This will take but a second. This part can be done manually and infrequently, but provides a lot of info for the next steps.

```bash
$ TODAY=$(date +'%Y-%m-%d')
$ ./utils/influencerScraper.py --short > var/lib/influencers-short-$TODAY.txt
$ ./utils/influencerScraper.py --long > var/lib/influencers-long-$TODAY.txt
```

The names in the short file (max 40 rows) will also be in the long file (max 400 rows), but it is useful to start off with the short file to make the next steps quicker with fewer profiles to process.

Alternatively, write a text file by hand, with one screen name per row. No `@` symbols are required.

### 2. Create Profile records

Use the input text file of screen names.

```bash
$ cd utils/insert/
$ # Confirm the names, without processing.
$ ./fetchProfiles.py --preview --file var/lib/myFile.txt
$ # Create or update a record in Profile table for each name.
$ ./fetchProfiles.py --file var/lib/myFile.txt
```

You can also input the names by hand, if you want to track screen names which are not covered in the text files. The input is case insensitive.

```bash
$ ./fetchProfiles.py --list handleA anotherHandleB someHandleC_123
```

One of the fetch profile lines can be added to a cron job with `crontab -e`, so you can get the latest data for names in the text file. If follower counts and status counts are not important to you and you are not creating a new text file input, this does not have to be automated.

### 3. Create Tweet records

It is important for this step to be automated in order to harvest new tweets for watch profiles regularly.

```bash
$ cd utils/insert/
$ # Set the --help message to understand the number argument.
$ ./fetchTweets.py 200
```

_TODO: write crontab instructions and possibly a .sh script for this section, covering tweets and optionally profiles._

### 4. View the data

Scripts are available to get a sample of tweets and profiles in the database.

```bash
$ python -m lib.query.tweets.topProfiles [LIMIT N]
$ python -m lib.query.tweets.topTweets [LIMIT N]
```


## Web app

Run the CherryPy web server.

This has not been implemented yet.

```bash
# To be completed.
```
