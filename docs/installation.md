# Installation


## Project requirements

- Twitter API credentials - covered later under [Twitter credentials](#twitter-credentials).
- [Python](https://www.python.org/) 3.6+.
- [SQLite](https://www.sqlite.org/index.html).


## Install OS-level dependencies


### macOS

Install [brew](https://brew.sh/).

Install packages with `brew`.

```bash
$ brew install sqlite3 libsqlite3-dev
```

### Ubuntu/Debian

Install packages with `apt` if you have it, otherwise `apt-get` can be used instead.

```bash
$ sudo apt update && sudo apt install sqlite3 libsqlite3-dev
```

## Install project dependencies

### Python packages used

- **SQLObject** - An ORM wrapper for the **SQLite** database.
- **tweepy** - For access to the Twitter API.
- **BeautifulSoup4** - For scraping Twitter influencers from a certain website's listings.
- **lxml** - For parsing html pages in **BeautifulSoup4**.
- **requests** - For HTTP get requests of influencer listings from a website.

See pinned versions in [requirements.txt](https://github.com/MichaelCurrin/twitterverse/blob/master/requirements.txt).

### Setup Python environment

It is usually best-practice in _Python_ projects to install into a sandboxed _virtual environment_, This will be locked to a specific Python version and contain only the _Python_ libraries that you install into it, so that your _Python_ projects do not get affected.

If you need details on installing Python and a virtual environment, see [Setup a Python 3 Virtual Environment](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7). Otherwise continue below.

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


### Setup Twitter credentials

#### 1. Register a new Twitter account (optional)

You may wish to register a new Twitter account just for accessing the Twitter API. This is recommended to preserve an existing personal account. Since if in the unlikely event that an account is used to abuse API limits (such persistently trying to do requests after a rate limit error), that account will be blocked.

#### 2. Login

1. Login to your Twitter account.
2. Go to [developer.twitter.com](https://developer.twitter.com/).
3. Go _Apps_ tab.

#### 3. Apply for developer account

Apply for a developer account if you don't have one already. In your application you will have to explain your usecase and wait for approval from Twitter. When I did this a second time, it took a few days and I had to add additional details in an email response.

#### 4. Setup API credentials

When you account is approval, create an app in the _Apps_ section, with read permissions.

The API credentials can be copied and used [Configure](#configure) section of this guide.

### Configure

_Note: The Twitter API credentials must kept secret. Therefore this project lets to store your details in a file ignored by `git`, to prevent the credentials from accidentally being added to version control._

1. Create local app config from template.
    ```bash
    $ (cd app/etc && cp app.template.conf app.local.conf)
    ```
2. Edit the file.
    ```bash
    $ open app/etc/app.local.conf
    ```
3. Fill in the Twitter auth section with your Twitter credentials. These are needed for application to do API requests.
4. You may fill in any optional values.

Once you have saved changes, you can continue.


### Setup Database

```bash
$ cd app/utils
```

You may read the help for the DB manager utility before continuing.

```bash
$ ./db_manager.py --help
```

Check the path to DB file configured in the local config file.

```bash
$ ./db_manager.py --path
```

Create a base DB with all tables and base labels.

```bash
$ ./db_manager.py --create
```

View a list of tables and row counts.

```bash
$ ./db_manager.py --summary
```

**Use with caution.** To drop and recreate a database (losing all data), run this command.

```bash
$ ./db_manager.py --drop --create --summary
```

### SQL console

Open a SQL console for the configured main DB.

```bash
$ cd app
$ make sql
```
