# Setup Guide


## Packages
Overview of package requirements:


### Virtual environment
* **Python** - this repo has only been tested on version `2.7` so far.
* **CherryPy** - for the web server
* **SQLObject** for ORM wrapper of the SQLite3 database.
* **tweepy** - for access to Twitter API.
* **bpython** - for command line help and autocomplete functionality, instead of using IPython. This is for development and testing and not necessary for the app to function.

```
    Usage:
        $ bpython               # enter python commandline using bpython
        >>> import datetime
        >>> datetime.<tab>      # press tab to autocomplete
        >>> datetime.datetime(  # add open bracket for help on arguments
```
See `app/requirements.txt` for versions numbers and dependencies.

Latest versions were used at time of developing this app.


### Global

The following should be installed outside of the virtualenv to avoid getting errors.

* **SQLite** - this is recommended for interacting with the SQLite3 database directly. Version `3.16.2` was used for the development of this repo. Then commands can be performed for example as `$ sqlite3 db.sqlite .tables`.


## Installation

Get your environment setup.

```bash
$ git clone https://michaelcurrin.github.com/twitterverse
$ cd twitterverse

$ sudo apt-get virtualenv
$ virtualenv virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements.txt
```

Navigate to app directory. All steps below assume this as starting point.

```bash
$ cd app
```

Setting up the database.

```bash
$ python -m lib.database --help
# Now follow the usage guide to setup the database with tables and populate them with Place data.
```

## Use


Get a summary of db stats.

```bash
$ python -m lib.query.schema.tableCounts
$ python -m lib.query.schema.preview
```

Select data from the database.

```bash
$ python
>>> from lib import database as db
>>> # Get 10 Place records.
>>> res = db.Place.select()
>>> print res.count()

>>> for x in res.limit(10):
...     print x
>>>

>>> # Get country with ID 120.
>>> c = db.Country.get(120)

>>> # If you have Trend data from a cronjob or other method, select it.
>>> res = db.Trend.select(db.Trend.q.volume > 10000)
>>> # View the SQL statement.
>>> str(res)
>>> # View the result objects returned. Apply list function to get all data from the generator.
>>> list(res)
```

### Cron

Get cronjobs running to get Trend data in.


#### Simple

Run a simple insert for trends of a single country and its towns with a bash script and an optional argument for a country to override the configured default. See instructions in [trendDefaultCountry.sh](../tools/cron/trendsDefaultCountry.sh). Run it manually or as a cron job.


#### Advanced

Do trend queries for a managed queue of places, using PlaceJob table in [cronJobs.py](../app/models/cronJobs.py). Records in the table can be viewed and modified using the [job manager](../app/utils/jobManager.py). Follow the prompts to add configured data.

```bash
$ python utils/jobManager.py -i
```

Then test the [PlaceJob scheduler](../app/utils/insert/runPlacejobSchedule.py) manually.

```bash
$ python utils/insert/runPlacejobSchedule.py
```

To run the python script above, add [trendsPlaceJob.sh](../tools/cron/trendsPlaceJob.sh) to your crontab as per usage instructions in that file. It has been written as a bash script in order simplify handling of virtualenv and logging the output.


### Web app

Run the CherryPy web server.

```bash
# To be completed.
```
