# twitterverse
Exploring the Twitterverse, by tweets, users, trends and countries.

Author: Michael Currin


## Setup


### Packages
Overview of package requirements:
* **Python 2.7** - this has not been tested on other versions of Python.
* **CherryPy** - for the web server
* **SQLObject** for ORM wrapper of the SQLite3 database
* **tweepy** - for access to Twitter API
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


### Installation

#### Debian

Get your environment setup.
```
$ git clone https://michaelcurrin.github.com/twitterverse
$ cd twitterverse

$ sudo apt-get virtualenv
$ virtualenv virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements.txt
```
Setting up the database.
```
$ cd app

$ python lib/database.py --help
# Now follow the usage guide to setup the database, with or without default data.

```
Get a summary of db stats.
```

$ python lib/dbQueries.py
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
Get cronjobs running to get Trend data in.
```
# To be completed.
````

Run the CherryPy web server.
```
# To be completed.
```
