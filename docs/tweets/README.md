# Tweets

Get tweets and Twitter profiles and store results in the Tweet and Profile tables.

`Tweet` records are assigned one or more `Campaign` labels.

`Profile` records are assigned one or more `Category` labels.

See the [utils](https://github.com/MichaelCurrin/twitterverse/tree/master/app/utils) directory for scripts to run from the terminal.

**Twitter API limitations**

This app uses the Twitter Search API to search for tweets by queries. However, Twitter limits you to only get tweets created in the _past week_, even if specify a longer date range in the query.

If you know a Twitter profiles's handle or ID, you can get all their tweets historically, back to some years ago.

If you know a tweet's ID, you can fetch that tweet to create or update it locally.


**Tweet search summary**

Search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window. Specify how many pages of tweets you default - each page has 100 tweets and you can fetch thousands of tweets if the script runs for a high-volume search.

Use the _campaign manager_ utility to create and update tweet campaigns - search queries which have convenient names. You can easily rerun the same search queries daily (or a few times a week if you need to always be up to date).

Print the tweets to the screen, or use the main functionality of storing tweets and users to the DB along with metadata like user category or tweet campaign.

Use the _search and store tweets_ utility into add tweets directly to the DB, using the ORM.

Note on _utils/extract_ module:

Along with the _insert_ module, there are also an _extract_ module to to handle saving to a CSV and later importing the CSV also with the ORM, to make fetching data faster. This means that searches on Twitter are shorter and therefore you can do more searches in a period, you can handle volumes of thousands of tweets easier. This is not complete yet - it saves to a CSV but the mechanism to import the tweets is not setup.


**Lookup by profile summary**

Get the tweet timeline of selected watched profile, or yourself.

There is a tool which also helps with this by getting handles from a site which lists the most popular Twitter accounts as a influencers.

Use the _category manager_ utility to create and update categories which are lists of twitter users.
