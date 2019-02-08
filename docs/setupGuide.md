# Setup Guide


## Packages

Overview of package requirements.

### Virtual environment

* **Python** - this repo has only been tested on version `2.7` so far.
* **SQLObject** for ORM wrapper of the SQLite3 database.
* **tweepy** - for access to Twitter API.
* **BeautifulSoup4** - for scraping Twitter influencers from a website's lists.
* **lxml** - for parsing html pages in BeautifulSoup4.

See [requirements.txt](/app/requirements.txt).

The latest versions were used at time of developing this app.


### Global

The following should be installed outside of the virtualenv to avoid getting errors.

* **SQLite** - this is recommended for interacting with the SQLite3 database directly, but not required. Version `3.16.2` was used for the development of this repo. Then commands can be performed for example as `$ sqlite3 db.sqlite .tables`.


## Installation

### Environment

Get your environment setup.

```bash
$ sudo apt-get python2 virtualenv
```

```bash
$ # HTTPS
$ git clone https://github.com/MichaelCurrin/twitterverse.git
$ # or SSH
$ git clone git@github.com:MichaelCurrin/twitterverse.git
$ cd twitterverse
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Run all python scripts in this repo within the activated virtual environment.


### Config

Create local app configuration file `app/etc/app.local.conf`

The following are recommended to be set:

```
# Unversioned local configuration file to override values set in `app.conf`.

# Twitter API credentials
[TwitterAuth]
consumerKey: ...
consumerSecret: ...
accessKey: ...
accessSecret: ..

[TwitterAccount]
handle: ...
```

Optionally, also configure your DB name here (fixed to being created in var directory). This can be useful for switching to a test database without worrying about messing up data or tables. See the base [app.conf](/app/etc/app.conf) file for more details.

```
[SQL]
dbPath: %(dbDir)s/custom_db_name.sqlite
```


### Database

View the instructions for setting up your database. 

```bash
$ cd app
$ python -m lib.database --help
```

Follow usage guide shown in the help message, using the `--summary` flag to see the effect after each step. The `--create` flag will create all necessary tables but leave them empty. Therefore the `--populate` flag is recommended after it, to add Place table records which can be used for fetching trend data. 

When using the create flag, a SQLite database file will be accessed in the configured location (see `--path` flag) and created if it does not yet exist.

Then, you can access the database directly in SQLite.

```bash
$ sqlite3 var/db.sqlite
```

Now see the app usage instructions in the docs of this rep.
