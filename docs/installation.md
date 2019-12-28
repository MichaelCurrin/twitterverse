# Installation

## Clone the repo

```bash
$ # HTTPS
$ git clone https://github.com/MichaelCurrin/twitterverse.git
$ # SSH
$ git clone git@github.com:MichaelCurrin/twitterverse.git
```
```bash
$ cd twitterverse
```

## Install System Packages

Linux (Debian/Ubuntu) instructions below.


```bash
sudo apt update
```

```bash
$ sudo apt install python3
```

Install SQLite. This is recommended for interacting with the SQLite3 database directly, but not required. See also the [sqliteTips](/docs/usage_tips/sqlite.md) docs.

```bash
$ sudo apt install sqlite3 libsqlite3-dev
```


### Install Local Project Packages

The following Python packages are used by this app. The latest versions were used at time of developing this app.

- **SQLObject** - an ORM wrapper for the SQLite database.
- **tweepy** - for access to the Twitter API.
- **BeautifulSoup4** - for scraping Twitter influencers from a certain website's listings.
- **lxml** - for parsing html pages in BeautifulSoup4.
- **requests** - for HTTP get requests of influencer listings from a website.

See pinned versions in [requirements.txt](/requirements.txt).

Setup virtual environment and activate it.

```bash
$ cd <PATH_TO_PROJECT>
$ python3 -m venv venv
$ source venv/bin/activate
```

Install packages into the virtual environment.

```bash
(venv) $ make install
(venv) $ make dev-install
```

Remember to always run all python scripts in this repo within the virtual environment **activated**.


### Twitter credentials

Login to your Twitter account then go to [developer.twitter.com/](https://developer.twitter.com/) and the _Apps_ section.

Apply for a developer account if you don't have one already. You will have to explain your usecase and wait for approval from Twitter.

When you account is approval, create an app in the _Apps_ section, with read permissions. The API credentials can be copied and used in the next section.


### Configure

1. Create and edit local app configuration file.
    ```bash
    $ (cd app/etc && cp app.template.conf app.local.conf && open app.local.conf)
    ```
2. You must fill in the Twitter auth section so the the application can do API requests.
3. You may fill in any optional values.

Once you've saved changes, you can continue.

### Setup Database


```bash
$ cd app
```

Check the path to DB file configured in the local config file.

```bash
$ ./utils/db_manager.py --path
```

Create a base DB with all tables and base labels.

```bash
$ ./utils/db_manager.py --create
```

Populate the database with location data.

```bash
$ ./utils/db_manager.py --populate --summary
```

See help.

```bash
$ ./utils/db_manager.py --help
```

#### Access DB directly

You can access the database directly in SQLite.

```bash
$ make sql
```
