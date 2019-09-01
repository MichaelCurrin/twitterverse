# Twitterverse
> Explore the Twitter conversations through users and their tweets and countries and their trending topics.

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

No warranty is provided for use of the tools or your ability to store data (especially high volume data).

## Requirements

- Twitter dev account and API credentials.
- Python and SQLite
- Data which you want to follow on Twitter e.g. trends for some of all places, tweets matching a search query or tweets by certain users.

## Features

Access to the project is all through command-line tools. Use the project for any of the features below to fetch data from the Twitter API and print or store. None of the utilities actually post data to Twitter.

### Fetch tweets

Use the _tweets_ section of this project.

Lookup tweets from the Twitter API.

#### Timeline

Get the tweet timeline of watched users or yourself. There is a tool which also helps with this by getting usernames from a site which lists the most popular Twitter accounts.

Use the category manager utility to create and update categories which are lists of twitter users.

#### Search

Search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window. Specify how many pages of tweets you default - each page has 100 tweets and you can fetch thousands of tweets if the script runs for a high-volume search.

Use the campaign manager utility to create and update tweet campaigns - search queries which have convenient names. You can easily rerun the same search queries daily (or a few times a week if you need to always be up to date).

Print the tweets to the screen, or use the main functionality of storing tweets and users to the DB along with metadata like user category or tweet campaign.

You can use the [search and store tweets](/app/utils/insert/search_and_store_tweets.py) utility to add tweets directly to the DB, using the ORM.

There are **in-progress** _extract_ tools to handle saving to a CSV and later importing the CSV also with the ORM, to make fetching data faster. This means that searches on Twitter are shorter and therefore you can do more searches in a period, you can handle volumes of thousands of tweets easier.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

There 62 countries and over 400 cities that Twitter provides trending data for. This project supports getting for all of them and groups places by country and continent.

Use the job manager tool in this project to get data just for the places you need,

Run the trending tool as a daily cron job. Then you have a history of trend data for places in the database and can create reports using your recent or historical data.

### Stream

Do a live stream of a search query and print out the tweets to the console.


## History

This project has been worked on and used for over 2 years so the ORM and command-line tools have been added to and improved a lot.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

Refactoring has been done to be more in line with PEP-8. Also, linting with PyCharm picked up some errors across the project which were fixed.

The command-line tools could be refactored to be more consistent and easier to use.


## Future

The plan is to upgrade this project to Python 3 by 2020.

For separation of concerns. The project could be split into a tweet project, a trending project and a smaller project which handles common logic like authentication. This would make it easier to maintain the project as the tweet and trend data does not overlap match, yet the utils use some common scripts and configs which means a problem in one could affect the whole project.

The ORM could be replaced with SQLAlchemy.
