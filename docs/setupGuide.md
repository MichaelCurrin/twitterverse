# Setup Guide


## Packages
Overview of package requirements:

### Virtual environment
* **Python** - this repo has only been tested on verrsion `2.7` so far.
* **CherryPy** - for the web server TO BE 
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
```
$ git clone https://michaelcurrin.github.com/twitterverse
$ cd twitterverse

$ sudo apt-get virtualenv
$ virtualenv virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements.txt
```

Navigate to app directory. All steps below assume this as starting point.
```
$ cd app
```

Setting up the database.
```
$ python -m lib.database --help
# Now follow the usage guide to setup the database with tables and populate them with Place data.
```

Get a summary of db stats.
```
$ python -m lib.query.schema.tableCounts
$ python -m lib.query.schema.preview
```

Select data from the database.
```
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

## Cron

Get cronjobs running to get Trend data in.
```
# See scripts in utils/ for adding Trend data to the database.

# To be completed.
```

## Web app

Run the CherryPy web server.
```
# To be completed.
```
