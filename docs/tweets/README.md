# Tweets

If you know a Twitter user's handle or ID, you can get all their tweets historically, back to some years ago. And if you know a tweet's ID, you can fetch that tweet to create or update it locally. But, if you use the Search API to find tweets by a user or about a topic, Twitter limits you to only get tweets created in the _past week_.


## Lookup by profile

Get the tweet timeline of watched users or yourself. There is a tool which also helps with this by getting usernames from a site which lists the most popular Twitter accounts.

Use the category manager utility to create and update categories which are lists of twitter users.

## Search

Search for tweets which match a query such as phrases or hashtag - this data is only available from the API for a 7 day window. Specify how many pages of tweets you default - each page has 100 tweets and you can fetch thousands of tweets if the script runs for a high-volume search.

Use the campaign manager utility to create and update tweet campaigns - search queries which have convenient names. You can easily rerun the same search queries daily (or a few times a week if you need to always be up to date).

Print the tweets to the screen, or use the main functionality of storing tweets and users to the DB along with metadata like user category or tweet campaign.

Use the _search and store tweets_ utility to add tweets directly to the DB, using the ORM.

There are **in-progress** _extract_ tools to handle saving to a CSV and later importing the CSV also with the ORM, to make fetching data faster. This means that searches on Twitter are shorter and therefore you can do more searches in a period, you can handle volumes of thousands of tweets easier.
