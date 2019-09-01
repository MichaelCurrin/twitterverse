# Twitterverse
> Explore the Twitter conversations through users and their tweets and countries and their trending topics.

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

This project will be upgraded to _Python 3_.

## Features

Use the project for any of the features below.

### Fetch tweets

Use the _tweets_ section of this project.

Lookup tweets from the Twitter API. Get the tweet timeline of watched users. Or search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window.

Use the database to store and update search queries, you can easily rerun the same queries daily (or a few times a week if you need to always be up to date).

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

There 62 countries and over 400 cities that Twitter provides trending data for. This project supports getting for all of them and groups places by country and continent.

Use the job manager tool in this project to get data just for the places you need,

Run the trending tool as a daily cron job. Then you have a history of trend data for places in the database and can create reports using your recent or historical data.

### Stream

Do a live stream of a search query and print out the tweets to the console.

## Documentation

Get started using these guides:

- [Installation](installation.md)
- [Usage](usage.md)

Use the menu sidebar for more details.
