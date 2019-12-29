# Twitterverse
> Explore the Twitter conversations, from tweets to trending topics

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

See [License](#license) section.

Cover image by <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@stereophototyp?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from Sara Kurfeß"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">Sara Kurfeß</span></a>


## Requirements

- Twitter dev account and Twitter API credentials (these are covered in [installation](installation.md)).
- [Python](https://www.python.org/downloads/) 3.6+.
- [SQLite](https://www.sqlite.org/index.html).

This project works best if you have an aim to follow and explore certain data on Twitter. e.g. trends for some places, tweets matching a search query or tweets by certain users.

## Features

Use the project for any of the features below to fetch data from the Twitter API and print or store. Access to the project is all through command-line utilities. The [usage](usage.md) section covers these features in more detail.

Note that that you cannot actually create a tweet with this project, but _tweepy_ docs cover how do that well.

### Fetch tweets

Lookup tweets from the Twitter API.

#### Timeline

Get the tweet timeline of watched users or yourself. There is a tool which also helps with this by getting usernames from a site which lists the most popular Twitter accounts.

Use the category manager utility to create and update categories which are lists of twitter users.

#### Search

Search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window. Specify how many pages of tweets you default - each page has 100 tweets and you can fetch thousands of tweets if the script runs for a high-volume search.

Use the campaign manager utility to create and update tweet campaigns - search queries which have convenient names. You can easily rerun the same search queries daily (or a few times a week if you need to always be up to date).

Print the tweets to the screen, or use the main functionality of storing tweets and users to the DB along with metadata like user category or tweet campaign.

Use the _search and store tweets_ utility to add tweets directly to the DB, using the ORM.

There are **in-progress** _extract_ tools to handle saving to a CSV and later importing the CSV also with the ORM, to make fetching data faster. This means that searches on Twitter are shorter and therefore you can do more searches in a period, you can handle volumes of thousands of tweets easier.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

There 62 countries and over 400 cities that Twitter provides trending data for. This project supports getting for all of them and groups places by country and continent.

Use the job manager tool in this project to get data just for the places you need,

Run the trending tool as a daily cron job. Then you have a history of trend data for places in the database and can create reports using your recent or historical data.

See [Trends usage](usage_tips/trends.md) for more info.

### Stream

Do a live stream of a search query and print out the tweets to the console.


## History

This project has been worked on and used for over 2 years so the ORM and command-line tools have been added to and improved a lot.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

Refactoring has been done to be more in line with PEP-8. Also, linting with PyCharm picked up some errors across the project which were fixed.

The command-line tools could be refactored to be more consistent and easier to use.

## Installation

See the [installation](installation.md) page.

## Usage

See the [usage](usage.md) page.

See other related docs in the sidebar.

## Make

Run the following in the project for useful shortcuts through the `make` command. These are used in the sections above.

```bash
$ make help
```


## License

This project is license with an [MIT License](https://github.com/MichaelCurrin/twitterverse/blob/master/LICENSE).

Feel free to use this project for non-commercial use. You can fork the project and modify it too.

No liability or warranty is provided.

Responsibility lies with you for managing your database data.

See the [Twitter Policies](twitter_api_docs/policies.md) page for info on fair use of the Twitter API.
