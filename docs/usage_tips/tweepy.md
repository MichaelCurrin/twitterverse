# Tweepy Tips


## Authenticate

Make sure you have created `etc/app.local.conf` with your own Twitter account's details so that you can authenticate.

```python
>>> from lib.twitter_api import authentication
>>> APIConn = authentication.getAPIConnection()
```


## Tweepy Queries

See tweepy.api docs for queries allowed to the Twitter API.

For example:

```python
>>> # Get user's timeline.
>>> APIConn.user_timeline(...)
>>> # Retweet a tweet.
>>> APIConn.retweet(...)
```

The following sections cover queries specific to this repo's app.


## Get tweets

Get one page of 200 tweets for a given screen name. This will not persist any profile or tweet data.

```python
>>> from lib import tweets
>>> fetchedTweets = tweets.get_tweets(APIConn, screenName='abc')
>>> print fetchedTweets
...
>>> t = fetchedTweets[0]
>>> dir(t)
>>> # => list of tweepy tweet object attributions and methods.
>>> t.created_at
datetime.datetime(..., ...)
>>> t.text
...
```
