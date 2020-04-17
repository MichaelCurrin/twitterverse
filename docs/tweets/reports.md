# Tweet and profile reports

Scripts are available to get a sample of tweets and profiles in the database.

<!-- TODO: Integrate these scripts as part of another utility or a main reporting utility. Consider if the limit should be made an optional flag for top_profiles and top_tweets, so default can be used as with top_words -->

```bash
$ cd app
```

## Available reports

See the [How to run reports](reports.md#how-to-run-reports) guide.

- ORM reports - [db_query/tweets/](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/db_query/tweets)
- SQL reports - [db_query/tweets/sql](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/db_query/sql/tweets)


## Example usage

```bash
$ python -m lib.db_query.tweets.top_profiles 5
$ python -m lib.db_query.tweets.top_tweets 5
```

```bash
$ python -m lib.db_query.tweets.top_words --search 'phrase to search' --limit 20
$ python -m lib.db_query.tweets.top_words --search 'word' --filter
```

## Category and campaign data

Use the category and campaign managers to see how Tweet or Profile data has been grouped.

```bash
$ ./utils/manage/categories.py --available
$ ./utils/manage/categories.py --profiles
```

```bash
$ ./utils/manage/campaigns.py --available
$ ./utils/manage/campaigns.py --tweets
```
