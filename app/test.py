# -*- coding: utf-8 -*-
"""
http://docs.tweepy.org/en/v3.5.0/code_snippet.html

Goals for testing:
    Write test data to JSON files in var.
        tweepy offers ._json method

    Get 200 tweets for a user.
    Get all locations.
    Get 50 trends a for a location.

    Get another user
    Get another location

    Get my own tweets

    Do bar graph.
    Do tag cloud.

    Store tweets in DB with mix of columns I want and JSON column
    for full object.
"""
import json

import tweepy

import lib.twitterAuth


auth = lib.twitterAuth.generateToken()
api = lib.twitterAuth.getAPIConnection(auth)


def _writeJSON(data, filename):
    print 'Write'
    with open(filename, 'w') as writer:
         json.dump(data, writer, indent=4)
    return True


def _readJSON(filename):
    print 'Read'
    with open(filename, 'r') as reader:
        data = json.load(reader)
    return data


def getUserTweets(screen_name):
    global api

    timeline = api.user_timeline(screen_name=screen_name)

    filename = 'var/tweet_{0}.json'.format('test')

    # Convert from class to JSON.
    outData = [tweet._json for tweet in timeline]

    print filename
    _writeJSON(outData, filename)
    _readJSON(filename)

    #print json.dumps(st._json, indent=4)
    #print

    # dir(st) =>
    # class to JSON conversion
    #   '_json'
    # other fields
    # e.g. tweet.id
    #   'author', 'contributors', 'coordinates', 'created_at', 'destroy', 'entities', 'favorite', 'favorite_count', 'favorited', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'parse', 'parse_list', 'place', 'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'source_url', 'text', 'truncated', 'user']

    
def getAvailable():
    global api
    places = api.trends_available()

    filename = 'var/places.json'
    print filename
    _writeJSON(places, filename)
    _readJSON(filename)


def getTrend(woeid):
    global api
    trends = api.trends_place(woeid)
    filename = 'var/trend_{0}.json'.format('test')
    print filename
    _writeJSON(trends, filename)
    _readJSON(filename)


if __name__ == '__main__':
    if True:
        screen_name = 'RealDonaldTrump'
        getUserTweets(screen_name)

    if False:
        places = getAvailable()

    if False:
        # USA
        woeid = 23424977
        getTrend(woeid)
