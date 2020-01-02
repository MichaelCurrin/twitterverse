# Watch profiles
> Fetch the tweets of selected profiles.

Steps are to identify handles of Twitter profiles of interest, add them to the DB, then add them using a utility. Optionally add this as a daily cron to get the recent tweets.

This data can be built up as historical data which can be filtered and visualized based on a requirement.

Note that while a search for tweets using the Twitter Search API data has a limited 7-day window, it is possible to do a sequence of API requests to easily retrieve Tweets for a single user going back a few months or years.

The application uses the `Category` class to assign a label to a `Profile`.

```bash
$ cd app/utils
```

## Load profiles

Use the Fetch Profiles utility to add one or more handles from a file or command-line input.

```bash
$ insert/fetch_profiles.py --help
```

Specify a new or existing category and one or more handles (excluding `@` symbols).

```bash
$ insert/fetch_profiles.py --category 'My watchlist' --list foo bar bazz
```

## View watchlist

Use the Category utility.

```bash
$ ./manage/categories.py --help
```

```bash
$ ./manage/categories.py view --profiles
1. My watchlist        3 profiles
   - @foo             | Foo
   - @bar             | Mr Bar
   - @bazz            | bazz
```
