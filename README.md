# Twitterverse
> Explore the Twitter conversations through users and their tweets and countries and their trending topics.

_Author: Michael Currin_

Application to harvest data from the Twitter API (using `tweepy` package) and to make that data easy to navigate, search and make sense of.


## Features

Use the project for any of the following features. Except for Streaming, you can the database to store your queries to rerun each day or week and also to store the objects which are returned by queries.

### Fetch tweets

Use the tweets section of this project.
 
Lookup tweets from the Twitter API which users which you are interested in.

Or search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics. Run that on a daily cron job, then you can see a history of those topics over time. 

### Stream

Do a live stream of a search query and print out the tweets to the console.


## Documentation

- [Setup guide](docs/setupGuide.md)
- [App usage](docs/appUsage.md)
- [Docs directory](docs/) 
