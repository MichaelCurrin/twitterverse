# Twitterverse 🌍 🐦 🐍
> Store and report on Twitter conversations, from tweets to trending topics

[![Actions status](https://github.com/MichaelCurrin/twitterverse/workflows/Python%20application/badge.svg)](https://github.com/MichaelCurrin/twitterverse/actions)
[![Known Vulnerabilities](https://snyk.io/test/github/MichaelCurrin/twitterverse/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/MichaelCurrin/twitterverse?targetFile=requirements.txt)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/twitterverse?include_prereleases=&sort=semver)](https://github.com/MichaelCurrin/twitterverse/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![dependency - tweepy](https://img.shields.io/badge/tweepy-3-blue?logo=twitter&logoColor=white)](https://www.tweepy.org/ "Go to Tweepy homepage")
[![dependency- SQLObject](https://img.shields.io/badge/SQLObject-3-blue)](http://sqlobject.org/ "Go to SQLite homepage")


## Note 

This repo is no longer maintained. The Twitter API or project dependencies might have changed so much that some functionality no longer works.


## Documentation

<div align="center">

[![View - Documentation](https://img.shields.io/badge/View-Online_docs-2ea44f?style=for-the-badge)](https://michaelcurrin.github.io/twitterverse/ "Go to online docs")

</div>


## Note

You are welcome to use this project as is for your projects, or use any relevant code as inspiration for your own projects. Though, this project is not under active development. 

I mostly use it for search and trends work and there is work to be done to get the search CSV data back into the database (the performance benefit was only 50% speed reduction so the non-CSV approach could have been okay from the start too).

Some of the logic is not used anymore and the CLIs are inconsistent or messy, but they will stay like that. Any work to add to or clean-up or refactor this project or update dependencies will probably be put off and moved to work in a new repo.

As a more modern alternative, see this project of mine:

- [![MichaelCurrin - python-twitter-lib](https://img.shields.io/static/v1?label=MichaelCurrin&message=python-twitter-lib&color=blue&logo=github)](https://github.com/MichaelCurrin/python-twitter-lib)

That doesn't care about making database and schema choices for you - it just get data out of Twitter in a more convenient way than learning all the intricacies of Tweepy and the Twitter API.



## Follow a guide to Tweepy

If you want to learn to use Tweepy and the Twitter API, I added tutorials and resources to this project which I created in 2020, based on a modern version of Tweepy.

<div align="center">
  
[![Tutorial - Python Twitter Guide](https://img.shields.io/badge/Tutorial-Python_Twitter_Guide-blue)](https://MichaelCurrin.github.io/python-twitter-guide)

</div>


## How to use this project

This project does a lot of things but its core is searching for tweets and getting daily trending data and storing results in a database or CSV. It uses the command-line to let you store hashtag searches and choose places to watch.

If you want to see how to see how this project handles auth, search or streaming, have a look at this module:

- [app/lib/twitter_api/](https://github.com/MichaelCurrin/twitterverse/tree/master/app/lib/twitter_api/)

You can clone and use the code locally or reference the code that you need for your own projects. Please provide a link back to this project. A copy of the license must be included with your code as well if you copy code directly from here.


## License

Released under [MIT](/LICENSE) by [@MichaelCurrin](https://github.com/MichaelCurrin).
