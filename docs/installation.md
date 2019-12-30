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

Install SQLite. This is recommended for interacting with the SQLite3 database directly, but not required.

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

See pinned versions in [requirements.txt](https://github.com/MichaelCurrin/twitterverse/blob/master/requirements.txt).

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

Remember to always run all Python scripts in this repo within the virtual environment **activated**.


### Twitter credentials

#### 1. Register a new Twitter account (optional)

You may wish to register a new Twitter account just for accessing the Twitter API. This is recommended to preserve an existing personal account. Since if in the unlikely event that an account is used to abuse API limits (such persistently trying to do requests after a rate limit error), that account will be blocked.

#### 2. Login

1. Login to your Twitter account.
2. Go to [developer.twitter.com](https://developer.twitter.com/).
3. Go _Apps_ tab.

#### 3. Apply for developer account

Apply for a developer account if you don't have one already. In your application you will have to explain your usecase and wait for approval from Twitter. When I did this a second time, it took a few days and I had to add additional details in an email response.

#### 4. Setup API credentials

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

See help.

```bash
$ ./utils/db_manager.py --help
```

#### SQL console

Open a SQL console for the configured main DB.

```bash
$ make sql
```
