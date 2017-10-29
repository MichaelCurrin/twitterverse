# Models


## Structure


Documentation on the structure of models in the database. See the [models](app/models/) directory.


### Places and Trends models

See the [places](app/models/places.py) and [trends](app/models/trends.py) models.

The table of Place records (typically around 400 records) can be mapped to a growing number of Trend records. On getting data from the Twitter API, we expect to get up to 50 trend topics to store as a records in our Trend table. The Trend record will only belong to one Place object and not shared, though the trending topic (phrase or hashtag) might be duplicated across other Trend objects, which are for a different time and/or owned by other Places records .

* Trend table
    - contains a trend topic for a specific time and place. Each record has a foreign key to map it to a Place record, derived from the Trend's WOEID value in the API.
 * Place table
    - contains records of all Places. These can be mapped to Trend records.
 * Place child tables.
    - Supername -> Continent -> Country -> Town
    - These tables are all special child tables of Place table - see `sqlobject.inheritance.InheritableSQLObject`. They are linked to each other in a hierarchy such that a Supername has Continents, which then have Countries, which then have Towns.
    - They are not strictly needed for Places and Trends to operate, however they aid in filtering Places. Such as when selecting trends in the db at a certain place level, or creating a PlaceJob schedule using only certain Place types.
    - The place type tables only have have 2 columns each - the Place ID and the Supername/Continent/Country/Town ID. The Place table has a child column which indicates which child table the Place can be found in. This can be null, since a Place does not necessarily have to have a child table though it is preferred.
    - Every record in  one of these tables has a record in Place table with the same ID.

This approach makes it easy to always map a Trend record to the same
table (Place) instead of many, while still allowing easy seperation of
Place types in the Place-related tables.

For example:

 - show all Places
 - show all from Countries table and count of its Towns we have mapped to it.
 - show Towns which are in Asia


### Tweet model

See the [tweets](app/models/tweets.py) model.


* Tweet table
 - Twitter tweets, using part of the tweet object returned from tweepy from the Twitter API.
 - must be mapped to a Profile record.
* Profile table
 - Twitter users
 - one Profile can have zero or more tweets and these can be accessed on the .tweets attribute of a record.
* Label table
 - optional label name which can be assigned to a Profile. Describes the reason the Profile and/or Tweets were added to the db.
 - the relationship between Profile and Label is many-to-many and managed in the ProfileLabel class, or profile_label table in SQL.
* Category table
 - optional category name which can be assigned to a Profile. Describes the nature of real life owner of the Twitter account or the general content of their tweets.
 - the relationship between Profile and Category is many-to-many and managed in the ProfileCategory class, or profile_category table in SQL.
