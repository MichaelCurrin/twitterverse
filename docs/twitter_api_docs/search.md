# Twitter Search

See my [Python Twitter Guide](https://michaelcurrin.github.io/python-twitter-guide/) website - I have a section there on the Search API which is more up to date.


## API

- Twitter [dev docs](https://developer.twitter.com/en/docs)
- Twitter API search endpoint - [get-search-tweets](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets).

See the `API.search` method of _tweepy_ documented here: [API Search](http://docs.tweepy.org/en/latest/api.html#API.search). Note however that it seems to be missing parameters which are covered in the search method here and this code also does not much the Twitter API. [tweepy/api.py](    https://github.com/tweepy/tweepy/blob/master/tweepy/api.py).

Results are limited to about 7 days back from the current date, regardless
of count or possible date values set. The limit is covered here: [Search overview](https://developer.twitter.com/en/docs/tweets/search/overview).


### Result Type


#### Twitter docs

From [Get Search Sweets](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html) in Twitter docs.


> **result_type**
>
> Optional. Specifies what type of search results you would prefer to receive. The current default is "mixed." Valid values include:
> - mixed : Include both popular and real time results in the response.
> - recent : return only the most recent results in the response
> - popular : return only the most popular results in the response.

#### Own testing

For testing of world cup data

- popular: 15
- recent: 96

A single page was only 15 tweets on 'popular' (without and without date starting at yesterday). And multiple pages had to be used to get tweets (5 pages -> 49 tweets. On 'recent', 96 were received in a single page. 'mixed' was not tested.

 On another topic, the volume tested.

  - mixed: 193
  - recent: 604
  - popular: 6


## Tweepy

Note that the search syntax applies both when doing a search in the browser and using the Twitter Search API (either through say `curl` or `tweepy`).

### Pagination

Note when it comes to doing searches with pagination in `tweepy`, the `tweepy.Cursor` approach is known to have memory leak issues.
It has been recommended to use a while loop with max or since ID values
instead. This may be necessary for high volume queries only, so the
Cursor approach is used here for now until that becomes an issue.

- https://stackoverflow.com/questions/22469713/managing-tweepy-api-search/22473254#22473254
- https://www.karambelkar.info/2015/01/how-to-use-twitters-search-rest-api-most-effectively./


## Quick reference


A summary of search query syntax is available in this project, so it can be accessed easily from the command-line when composing search queries.

```bash
$ utils/campaigns/manage.py --search-help
```


### Guidelines

- Note that combining terms is different between REST API and Streaming API.
  Here, in the REST API, terms are implicitly `AND`-ed together. But 'OR'
  can be used. There does not appear to be a limit on the length
  of the query or number of terms.
- Symbols like @ or # can be used at the start of terms, but this will
  be give fewer tweets than searching without the symbols, so consider
  if they make sense.
- Double quotes can be used to enclose words as an exact match phrase,
  but quotes sentences must appear at the start of the search query to
  avoid getting zero results overall. This is a known bug on Twitter API.
- Examples:
    * `'wordA wordB wordC'` => search for tweets containing all 3 words,
        in any order.
    * `'wordA OR #wordB OR wordC'` => search for tweets containing any of
        the 3 words.
    * `'@handleA OR wordB'` => search for tweets about either term.
    * `'"Welcome home" OR "Good luck" OR wordC'` => search for terms
        about either of the quoted phrases or wordC
