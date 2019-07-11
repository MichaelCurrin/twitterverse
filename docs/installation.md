# Installation

## Clone repo

```bash
$ # HTTPS
$ git clone https://github.com/MichaelCurrin/twitterverse.git
$ # or SSH
$ git clone git@github.com:MichaelCurrin/twitterverse.git
$ cd twitterverse
```

## Install System Packages


Linix (Debian/Ubuntu) instructions below.


```bash
sudo apt update
```

```bash
$ sudo apt python2 virtualenv
```

Install SQLite. This is recommended for interacting with the SQLite3 database directly, but not required. See also the [sqliteTips](/docs/sqliteTips.md) docs.

```bash
$ sudo apt install sqlite3 libsqlite3-dev
```


### Install Local Project Packages

The following Python packages are used by the app. The latest versions were used at time of developing this app. 

* **Python** - this repo has only been tested on version `2.7` so far.
* **SQLObject** for ORM wrapper of the SQLite3 database.
* **tweepy** - for access to Twitter API.
* **BeautifulSoup4** - for scraping Twitter influencers from a certain website's listings.
* **lxml** - for parsing html pages in BeautifulSoup4.

See pinned versions in [requirements.txt](/requirements.txt). 

Install packages into a new virtual environment created for the project.

```
$ <PATH_TO_PROJECT>
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Run all python scripts in this repo within the activated virtual environment.


### Configure

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


### Setup Database

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
