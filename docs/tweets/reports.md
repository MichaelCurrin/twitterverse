# Tweet and profile reports

Scripts are available to get a sample of tweets and profiles in the database.

<!-- TODO: Integrate these scripts as part of another utility or a main reporting utility. Consider if the limit should be made an optional flag for top_profiles and top_tweets, so default can be used as with top_words -->

```bash
$ python -m lib.db_query.tweets.top_profiles 5
$ python -m lib.db_query.tweets.top_tweets 5

$ python -m lib.db_query.tweets.top_words --search 'phrase to search' --limit 20
$ python -m lib.db_query.tweets.top_words --search 'word' --filter
```

Use the category and campaign managers to see how Tweet or Profile data has been grouped.

```bash
$ ./utils/manage/categories.py --available
$ ./utils/manage/categories.py --profiles

$ ./utils/manage/campaigns.py --available
$ ./utils/manage/campaigns.py --tweets
```
