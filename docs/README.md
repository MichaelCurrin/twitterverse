# Twitterverse
> Explore the Twitter conversations, from tweets to trending topics

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

See [License](#license) section.

Cover image by <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@stereophototyp?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from Sara Kurfeß"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">Sara Kurfeß</span></a>

This project works best if you have an aim to follow and explore certain data on Twitter. e.g. trends for some places, tweets matching a search query or tweets by certain users.


## Requirements

- Twitter dev account plus Twitter API credentials (both are covered in [installation](installation.md)).
- [Python](https://www.python.org/downloads/) 3.6+.
- [SQLite](https://www.sqlite.org/index.html).


## Features

Use the project for any of the features below to fetch data from the Twitter API and print or store. Access to the project is all through command-line utilities. The [usage](usage.md) section covers these features in more detail.

Note that that you cannot actually create a tweet with this project, but _tweepy_ docs cover how do that well.

### Get tweets and profiles

Lookup tweets and profiles from the Twitter API. A search can be done for tweets matching a query. Profiles and their tweets can also be looked up by handle.

If you store the tweets in the DB, you can do a report on the data.

See [Tweets](tweets/) page.


### Stream tweets

You can also do a live stream of a search query and print out the tweets to the console. This is not a core part of this project.

See [Streaming](tweets/streaming.md) page.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

Reports can be done on the stored trending data.

See [Trends](trends/) page.


## Installation

See the [installation](installation.md) page.

## Usage

- [Tweets](tweets/)
- [Trends](trends/)

See also other related docs in the site menu.


Run the following in the project for useful shortcuts through the `make` command. These are used in the sections above.

```bash
$ make help
```


## Project history

This project has been worked on and used for over 2 years so the ORM and command-line tools have been added to and improved a lot.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

Refactoring has been done to be more in line with PEP-8. Also, linting with PyCharm picked up some errors across the project which were fixed.

The command-line tools could be refactored to be more consistent and easier to use.


## License

This project is license with an [MIT License](https://github.com/MichaelCurrin/twitterverse/blob/master/LICENSE).

Feel free to use this project for non-commercial use. You can fork the project and modify it too.

No liability or warranty is provided.

Responsibility lies with you for managing your database data.

See the [Twitter Policies](twitter_api_docs/policies.md) page for info on fair use of the Twitter API.
