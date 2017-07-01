# STREAMING API NOTES FROM DOCS


## Restrictions
https://dev.twitter.com/streaming/public

Each account may create only one standing connection to the public endpoints, and connecting to a public stream more than once with the same account credentials will cause the oldest connection to be disconnected.

Clients which make excessive connection attempts (both successful and unsuccessful) run the risk of having their IP automatically banned.


## Rate limiting

http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html

When using Twitter’s streaming API one must be careful of the dangers of rate limiting. If clients exceed a limited number of attempts to connect to the streaming API in a window of time, they will receive error 420. The amount of time a client has to wait after receiving error 420 will increase exponentially each time they make a failed attempt.


## POST

 POST statuses/filter

https://dev.twitter.com/streaming/reference/post/statuses/filter


Returns public statuses that match one or more filter predicates. Multiple parameters may be specified which allows most clients to use a single connection to the Streaming API. Both GET and POST requests are supported, but GET requests with too many parameters may cause the request to be rejected for excessive URL length. Use a POST request to avoid long URLs.

The track, follow, and locations fields should be considered to be combined with an OR operator. track=foo&follow=1234 returns Tweets matching “foo” OR created by user 1234.

The default access level allows up to 400 track keywords, 5,000 follow userids and 25 0.1-360 degree location boxes. If you need elevated access to the Streaming API, you can contact Gnip.


## Parameters
https://dev.twitter.com/streaming/overview/request-parameters

See help(stream.filter) for args

## languages


https://dev.twitter.com/streaming/overview/request-parameters#language

This parameter may be used on all streaming endpoints, unless explicitly noted.

Setting this parameter to a comma-separated list of BCP 47 language identifiers corresponding to any of the languages listed on Twitter’s advanced search page will only return Tweets that have been detected as being written in the specified languages. For example, connecting with languages=en will only stream Tweets detected to be in the English language.

See https://www.loc.gov/standards/iso639-2/php/code_list.php


## follow

A comma-separated list of user IDs, indicating the users whose Tweets should be delivered on the stream. Following protected users is not supported. For each user specified, the stream will contain:

    Tweets created by the user.
    Tweets which are retweeted by the user.
    Replies to any Tweet created by the user.
    Retweets of any Tweet created by the user.
    Manual replies, created without pressing a reply button (e.g. “@twitterapi I agree”).

The stream will not contain:

    Tweets mentioning the user (e.g. “Hello @twitterapi!”).
    Manual Retweets created without pressing a Retweet button (e.g. “RT @twitterapi The API is great”).
    Tweets by protected users.

## track

A comma-separated list of phrases which will be used to determine what Tweets will be delivered on the stream. A phrase may be one or more terms separated by spaces, and a phrase will match if all of the terms in the phrase are present in the Tweet, regardless of order and ignoring case. By this model, you can think of commas as logical ORs, while spaces are equivalent to logical ANDs (e.g. ‘the twitter’ is the AND twitter, and ‘the,twitter’ is the OR twitter).

The text of the Tweet and some entity fields are considered for matches. Specifically, the text attribute of the Tweet, expanded_url and display_url for links and media, text for hashtags, and screen_name for user mentions are checked for matches.

Each phrase must be between 1 and 60 bytes, inclusive.

Exact matching of phrases (equivalent to quoted phrases in most search engines) is not supported.

Punctuation and special characters will be considered part of the term they are adjacent to. In this sense, “hello.” is a different track term than “hello”. However, matches will ignore punctuation present in the Tweet. So “hello” will match both “hello world” and “my brother says hello.” Note that punctuation is not considered to be part of a #hashtag or @mention, so a track term containing punctuation will not match either #hashtags or @mentions.

UTF-8 characters will match exactly, even in cases where an “equivalent” ASCII character exists. For example, “touché” will not match a Tweet containing “touche”.

Non-space separated languages, such as CJK are currently unsupported.

URLs are considered words for the purposes of matches which means that the entire domain and path must be included in the track query for a Tweet containing an URL to match. Note that display_url does not contain a protocol, so this is not required to perform a match.

Twitter currently canonicalizes the domain “www.example.com” to “example.com” before the match is performed, so omit the “www” from URL track terms.

Finally, to address a common use case where you may want to track all mentions of a particular domain name (i.e., regardless of subdomain or path), you should use “example com” as the track parameter for “example.com” (notice the lack of period between “example” and “com” in the track parameter). This will be over-inclusive, so make sure to do additional pattern-matching in your code. See the table below for more examples related to this issue.

Track examples:

Twitter
twitter api,twitter streaming
