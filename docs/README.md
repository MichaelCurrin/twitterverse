# Twitterverse
> Store and report on Twitter conversations, from tweets to trending topics.

[![Actions status](https://github.com/MichaelCurrin/twitterverse/workflows/Python%20application/badge.svg)](https://github.com/MichaelCurrin/twitterverse/actions)
[![Dependencies Tweepy](https://img.shields.io/badge/Dependencies%20-Tweepy-blue.svg)](https://www.tweepy.org/)
[![Dependencies SQLObject](https://img.shields.io/badge/Dependencies%20-SQLObject-blue.svg)](http://sqlobject.org/)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/twitterverse.svg)](https://GitHub.com/MichaelCurrin/twitterverse/tags/)

Application to harvest data from the Twitter API (using Python `tweepy` package) and to make that data easy to navigate, search and make sense of. SQLite is used for storage, with `SQLObject` as the ORM.

!> NB. This project requires **Twitter API credentials** (see [installation](installation.md#twitter-credentials)) which takes time and effort to setup, but they are available for free.


## How to use this project

This project does a lot of things but its core is searching for tweets and getting daily trending data and storing results in a database or CSV. It uses the command-line to let you store hashtag searches and choose places to watch.

If you want to see how to see how this project does auth, search or streaming, have a look at this module.

- [app/lib/twitter_api](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/twitter_api)

You can clone and use the code locally or reference the code that you need for your own projects. Please provide a link back to this project. A copy of the license must be included with your code as well if you copy code directly from here.


## Follow a guide to Tweepy

If you want to learn to use Tweepy and the Twitter API, I added tutorials and resources here.

- https://MichaelCurrin.github.io/python-twitter-guide


## Features

This project works best if you have an aim to follow and explore certain data on Twitter. Such as:

This project allows you to fetch data related to the above. The default behavior for most is to store though some have flags to print only.

Note: You cannot actually post a tweet with this project. But the [tweepy](http://docs.tweepy.org/en/latest/) website covers that well.

Access to the project is all through command-line utilities.


### Get tweets and profiles

Lookup tweets and profiles from the Twitter API. The focus of this project is searching for tweets (and getting their profiles at the same time) using a search query. If you lookup a profile directly, you can get stats, bio and their tweets.

The input needed depends on the API query type, as below:

API query | Input required | Equivalent browser URL
---  | ---   | ---
Tweet search | Search query to match against tweet messages | `twitter.com/search?q=QUERY` for phrase which may contain hashtag or spaces, OR `twitter.com/hashtag/HASHTAG` for a single hashtag.
Tweet lookup | ID of a tweet | `twitter.com/HANDLE/status/TWEET_ID`
Profile lookup | Handle or ID of the Twitter user. | `twitter.com/HANDLE`

The browser URL is useful for testing a query on a small scale or to check an object exists before doing an API query for it.

If you store the data in the DB, you can then do a report on the tweets and profiles.


### Stream tweets

You can also do a live stream of a search query and print out the tweets to the console. This is not a core part of this project and so no tweets are printed to the console but note stored in the DB.

Input required:

- Search query to match against tweet messages.

### Get trending topics

Using the trends scripts to find what topics are trending in your country or town at the current moment. See what other places are also talking about this topics.

Reports can be done on the stored trending data.

Input required:
- Names of countries or towns places to get trending topic data for. Twitter allows lookup for Worldwide, 62 countries and abou 400 towns/cities.

There is no browser URL equivalent of looking up a trend, but on the right menu on twitter.com you can see a list of trends in your area and you can click through from there to do a search for tweets about that topic. Format: `twitter.com/search?q=QUERY`.


## Setup

Follow the [Installation](installation.md) guide to setup the application locally, including config setup.


## Usage

### API

This project has a command-line interface which allows you to use the configured application, _without_ writing any code or using a Python console. Access the API through scripts covered in these sections.

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

Or see the [Makefile](https://github.com/MichaelCurrin/twitterverse/blob/master/Makefile) on Github.


## Project history

This project started in 2017 out of a desire to get tweet and trend data at scale so it can be explored as reports and graphs. I find topics of interest of myself and friends. Hopefully this can be used for businesses to use to understand their campaigns or brand mentions. It has turned out to be useful for tracking social and political data too, such as the Cape Town Water Crisis and elections.

The project has been adapted to manager higher volumes of data.

Unit tests have been added but a lot more could be added.

The command-line tools could be refactored to be more consistent and easier to use.


## License

This project is license with an [MIT License](https://github.com/MichaelCurrin/twitterverse/blob/master/LICENSE). Feel free to use this project for non-commercial use. You can fork the project and modify it too.

No liability or warranty is provided. Responsibility lies with you for managing your database data.

See the [Twitter Policies](twitter_api_docs/policies.md) page for info on fair use of the Twitter API and the returned data.


## Credits

- Cover image by <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@stereophototyp?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from Sara Kurfeß"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-2px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M10 9V0h12v9H10zm12 5h10v18H0V14h10v9h12v-9z"></path></svg></span><span style="display:inline-block;padding:2px 3px">Sara Kurfeß</span></a>
- This docs site uses the _dark_ theme of [Docsify](docsify.js.org).
