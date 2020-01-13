# Twitterverse
> Store and report on Twitter conversations, from tweets to trending topics.

[![Actions status](https://github.com/MichaelCurrin/twitterverse/workflows/Python%20application/badge.svg)](https://github.com/MichaelCurrin/twitterverse/actions)
[![Dependencies Tweepy](https://img.shields.io/badge/Dependencies%20-Tweepy-blue.svg)](https://www.tweepy.org/)
[![Dependencies SQLObject](https://img.shields.io/badge/Dependencies%20-SQLObject-blue.svg)](http://sqlobject.org/)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/twitterverse.svg)](https://GitHub.com/MichaelCurrin/twitterverse/tags/)

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

NB. This project requires **Twitter API credentials** (see [installation](installation.md#twitter-credentials)) which takes time and effort to setup, but they are available for free.


## Features

This project works best if you have an aim to follow and explore certain data on Twitter. Such as:

This project allows you to fetch data related to the above. The default behavior for most is to store though some have flags to print only.

Note: You cannot actually post a tweet with this project. But the [tweepy](http://docs.tweepy.org/en/latest/) website covers that well.

Access to the project is all through command-line utilities.


### Get tweets and profiles

Lookup tweets and profiles from the Twitter API. A search can be done for tweets matching a query. Profiles and their tweets can also be looked up by handle.

If you store the data in the DB, you can do a report on the tweets and profiles.

Input required is one of the following:
- Search query to match against tweets messages.
- IDs of tweets.
- Handles of Twitter profiles.

### Stream tweets

You can also do a live stream of a search query and print out the tweets to the console. This is not a core part of this project and so no tweets are printed to the console but note stored in the DB.

Input required:
- Search query to match against tweet messages.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

Reports can be done on the stored trending data.

Input required:
- Names of countries or towns places to get trending topic data for.


## Setup

Follow the [installation](installation.md) guide to setup the application locally, including config setup.

## Usage

### API

This project has an API (not a web API) which allows you to use the configured application, _without_ writing any code or using a Python console. Access the API through scripts covered in these sections.

- [Tweets](tweets/)
- [Trends](trends/)

See the docs menu for development, console use and other advanced functionality.

### Scheduling

If you are interested in scheduling jobs around tweets and trends but are not familiar with `crontab`, I recommended researching how to use it before following the usage docs.

See the [Scheduling](https://github.com/MichaelCurrin/learn-to-code/tree/master/Shell/Scheduling) of my _Learn To Code_ project.

### Makefile

Run the following in the project for useful shortcuts through the `make` command. These are used in the sections above.

```bash
$ make help
```

Or the [Makefile](https://github.com/MichaelCurrin/twitterverse/blob/master/Makefile) on Github.

## Project history

This project has been worked on and used for over 2 years so the ORM and command-line tools have been added to and improved a lot.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

Refactoring has been done to be more in line with PEP-8. Also, linting with PyCharm picked up some errors across the project which were fixed.

The command-line tools could be refactored to be more consistent and easier to use.


## License

This project is license with an [MIT License](https://github.com/MichaelCurrin/twitterverse/blob/master/LICENSE). Feel free to use this project for non-commercial use. You can fork the project and modify it too.

No liability or warranty is provided. Responsibility lies with you for managing your database data.

See the [Twitter Policies](twitter_api_docs/policies.md) page for info on fair use of the Twitter API and the returned data.


## Credits

- Cover image by <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@stereophototyp?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from Sara Kurfeß"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">Sara Kurfeß</span></a>
- This docs site uses the _dark_ theme of [Docsify](docsify.js.org).
