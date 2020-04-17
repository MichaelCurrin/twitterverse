# Models

Documentation on the structure of models in the database. See the [models](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/) module of the repo.


## Place and Trend models

See the [places.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/places.py) and [trends.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/trends.py) modules in the models section of the repo.

The table of _Place_ records (typically around 400 records) can be mapped to a growing number of _Trend_ records. On getting data from the Twitter API, we expect to get up to 50 trend topics to store as a records in our _Trend_ table. The _Trend_ record will only belong to one _Place_ object and not shared, though the trending topic (phrase or hashtag) might be duplicated across other _Trend_ objects, which are for a different time and/or owned by other _Place_ records.

* **Trend table**
    - Contains a trend topic for a specific time and place. Each record has a foreign key to map it to a Place record, derived from the Trend's WOEID value in the API.
 * **Place table**
    - Contains records of all places. These can be mapped to _Trend_ records.
 * **Place child tables**
    - _Supername_ -> _Continent_ -> _Country_ -> _Town_
    - These tables are all special child tables of _Place_ table - see `sqlobject.inheritance.InheritableSQLObject`. They are linked to each other in a hierarchy such that a Supername has Continents, which then have Countries, which then have Towns.
    - They are not strictly needed for Places and Trends to operate, however they aid in filtering Places. Such as when selecting trends in the db at a certain place level, or creating a PlaceJob schedule using only certain _Place_ types.
    - The place type tables only have have 2 columns each - the Place ID and the Supername/Continent/Country/Town ID. The _Place_ table has a child column which indicates which child table the Place can be found in. This can be null, since a _Place_ does not necessarily have to have a child table though it is preferred.
    - Every record in  one of these tables has a record in _Place_ table with the same ID.

This approach makes it easy to always map a Trend record to the same table (_Place_) instead of many, while still allowing easy separation of Place types in the Place-related tables.

For example:

 - Show all Places.
 - Show all from Countries table and count of its Towns we have mapped to it.
 - Show Towns which are in Asia.


## Tweet and Profile models

See the [tweets.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/tweets.py) modules in the models section of the repo.

* **Tweet table**
    - These are Twitter tweets, using part of the tweet object returned from _tweepy_ from the Twitter API.
    - A `Tweet` record must always be associated with a `Profile` table record. If the profile is removed, the tweets will be deleted.
    - The `Tweet` table has a unique constraint on the tweet ID (as fetched from Twitter). This means that tweets are not duplicated in the database and if a tweet is seen a second time then its details (such as engagements) can be updated.
* **Profile table**
    - Twitter users.
    - A Profile recored can have zero or more tweets associated with it and these can be accessed on the `.tweets` attribute of a record.
* **Campaign table**
    - Optional label which can be assigned to a Tweet to describe why the Tweet was added to the DB. This is used heavily in this project. A tweet may have multiple campaigns associated with it.
    - If a Tweet is added to because of a Twitter Search API query, then the Tweet should be assigned a relevant campaign. This can easily be done for a batch of Tweets fetched for a certain search query string and associated campaign name. The search query string which is used should be stored and maintained in a cron job file, not in the DB.
* **ProfileCampaign**
    - The relationship between Profile and Campaign is many-to-many and managed in the `ProfileCampaign` class, or `profile_campaign` table in SQL.
    - All Tweets in a campaign can be a selected using a join on the `ProfileCampaign` class. A Tweet might be common to multiple campaigns if it happened to match the search criteria of both campaigns.
* **Category table**
    - Optional label which can be assigned to Profiles. The Category describes the nature of the Twitter account or the general content of their tweets and therefore is best allocated manually after inspecting an a Profile or its Tweets.
    - Example categories for industries are "sports", "politics", "arts & culture" or "music". Examples for tracking influencers are "most followed", "most following", "most tweets" or "most engagements" and those Categories could be allocated to batches of profiles when they are scraped from a webpage of top Twitter users.
    - For reporting, Categories can be used to filter Profile or Tweet
    records. Then records can be compared within or across categories to see if Profiles in a certain industry are talking about a certain hashtag. Or take topic trending at a location and get context around it by seeing how Profiles in each industry are talking about it and how many of Twitter's most influencer users are talking about it.
* **ProfileCategory table**
    - A Profile can be allocated to more than one Category.
    - The relationship between Profile and Category records is many-to-many and managed in the `ProfileCategory` class. This is the `profile_category` table in SQL.
