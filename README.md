# Twitterverse
> Store and report on Twitter conversations, from tweets to trending topics.

[![Actions status](https://github.com/MichaelCurrin/twitterverse/workflows/Python%20application/badge.svg)](https://github.com/MichaelCurrin/twitterverse/actions)
[![Dependencies Tweepy](https://img.shields.io/badge/Dependencies%20-Tweepy-blue.svg)](https://www.tweepy.org/)
[![Dependencies SQLObject](https://img.shields.io/badge/Dependencies%20-SQLObject-blue.svg)](http://sqlobject.org/)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/twitterverse.svg)](https://GitHub.com/MichaelCurrin/twitterverse/tags/)


## Online docs

**:open_file_folder: [https://michaelcurrin.github.io/twitterverse](https://michaelcurrin.github.io/twitterverse)**


## Note

This project is not under active development. I mostly use it for search and trends work and there is work to be done to get the search CSV data back into the database (the performance benefit was only 50% speed reduction so the non-CSV approach could have been okay from the start too).

Some of the logic is not used anymore and the CLIs are inconsistent or messy, but they will stay like that. Any work to add to or clean-up or refactor this project or update dependencies will probably be put off and moved to work in a new repo.

But you are welcome to use this project as is for your projects, or use any relevant code as inspiration for your own projects.


## Follow a guide to Tweepy

If you want to learn to use Tweepy and the Twitter API, I added tutorials and resources to this project which I created in 2020, based on a modern version of Tweepy.

- [MichaelCurrin.github.io/python-twitter-guide](https://MichaelCurrin.github.io/python-twitter-guide)


## How to use this project

This project does a lot of things but its core is searching for tweets and getting daily trending data and storing results in a database or CSV. It uses the command-line to let you store hashtag searches and choose places to watch.

If you want to see how to see how this project does auth, search or streaming, have a look at this modul:

- [app/lib/twitter_api/](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/twitter_api)

You can clone and use the code locally or reference the code that you need for your own projects. Please provide a link back to this project. A copy of the license must be included with your code as well if you copy code directly from here.
