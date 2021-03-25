
## Fetch profile tweets
> Get tweets for watched profiles

Name one or more Categories and look up and store the Tweets.

First create a Category and profiles in the database using the [Watch influencers](tweets/watch-influencers.md) or [Watch profiles](tweets/watch-profiles.md) pages.

The Category filter allows fetching Tweets for just a certain category (e.g. top influencers, an industry or a custom watch list), to avoid fetching unnecessary data for all Profiles in database.

This step can be done once off to get Tweets for Profiles in certain Categories, perhaps with Tweets per Profile set to 1000 to get a few years of Tweets for each Profile. Then, this could be added to a crontab on a daily or weekly schedule so that reports will have recent Tweet data to work with.

How to fetch tweets by a given profile Category.

```bash
$ cd app/utils
```

```bash
$ insert/fetch_tweets.py --help

$ insert/fetch_tweets.py --categories 'My watchlist'
Fetching Tweets for 2 Profiles
...
```

Note that the script defaults to getting **200** most recent Tweets for each Profile (as this is one requested page of Tweets from the API). Even for Profiles which post 7 times a day, this would still give 4 weeks of activity. Therefore when the script runs at 200 Tweets per Profile, it will likely spend more time updating engagements on existing Tweets in the db than storing new Tweets, so the volume of Tweets stored locally will grow relatively slowly.
