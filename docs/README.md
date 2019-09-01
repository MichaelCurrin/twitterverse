# Twitterverse
> Explore the Twitter conversations through users and their tweets and countries and their trending topics.

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

## Future

This project has been worked on and used for over 2 years so the ORM and command-line tools have been added to and improved a lot.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

The command-line tools could be refactor to be more consistent and easier to use.

The plan is to upgrade this project to Python 3 by 2020.


## Features

Access to the project is all through command-line tools. Use the project for any of the features below.

### Fetch tweets

Use the _tweets_ section of this project.

Lookup tweets from the Twitter API. Get the tweet timeline of watched users. Or search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window.

Use the database to store and update search queries, you can easily rerun the same queries daily (or a few times a week if you need to always be up to date).

You can use the _insert_ tool to add tweets directly to the DB using the ORM. There are in-progress _extract_ tools to handle saving to a CSV and later importing the CSV, to make fetching data faster. This means that searches on Twitter are shorter and therefore you can do more searches in a period, you can handle volumes of thousands of tweets easier.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

There 62 countries and over 400 cities that Twitter provides trending data for. This project supports getting for all of them and groups places by country and continent.

Use the job manager tool in this project to get data just for the places you need,

Run the trending tool as a daily cron job. Then you have a history of trend data for places in the database and can create reports using your recent or historical data.

### Stream

Do a live stream of a search query and print out the tweets to the console.
