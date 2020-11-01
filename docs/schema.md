# Schema
> Reference for the structure of the tables and fields

Output from running `.schema` in SQLite console, excluding some indexes. This helps as a reference for writing SQL queries.

## Trends

```sql
CREATE TABLE place (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    woeid INT NOT NULL UNIQUE,
    name VARCHAR(64),
    timestamp TIMESTAMP,
    child_name VARCHAR(255)
);
CREATE TABLE supername (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE continent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supername_id INT CONSTRAINT supername_id_exists REFERENCES supername(id)
);
CREATE TABLE country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    continent_id INT CONSTRAINT continent_id_exists REFERENCES continent(id) ,
    country_code VARCHAR(2)
);
CREATE TABLE town (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INT CONSTRAINT country_id_exists REFERENCES country(id)
);

CREATE TABLE trend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic VARCHAR(64),
    hashtag BOOLEAN,
    volume INT,
    place_id INT CONSTRAINT place_id_exists REFERENCES place(id) ,
    timestamp TIMESTAMP
);
CREATE TABLE profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guid INT NOT NULL UNIQUE,
    screen_name VARCHAR(30) NOT NULL,
    name VARCHAR(60) NOT NULL,
    description TEXT,
    location TEXT,
    image_url TEXT,
    followers_count INT NOT NULL,
    statuses_count INT NOT NULL,
    verified BOOLEAN NOT NULL,
    modified TIMESTAMP NOT NULL
);
```


## Tweets

```sql
CREATE TABLE tweet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guid INT NOT NULL UNIQUE,
    profile_id INT NOT NULL CONSTRAINT profile_id_exists REFERENCES profile(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL,
    message TEXT NOT NULL,
    favorite_count INT NOT NULL,
    retweet_count INT NOT NULL,
    in_reply_to_tweet_guid INT,
    in_reply_to_profile_guid INT,
    modified TIMESTAMP NOT NULL
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE profile_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INT NOT NULL CONSTRAINT profile_id_exists REFERENCES profile(id) ON DELETE CASCADE,
    category_id INT NOT NULL CONSTRAINT category_id_exists REFERENCES category(id) ON DELETE CASCADE
);

CREATE TABLE campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    search_query TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE tweet_campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id INT NOT NULL CONSTRAINT tweet_id_exists REFERENCES tweet(id) ON DELETE CASCADE,
    campaign_id INT NOT NULL CONSTRAINT campaign_id_exists REFERENCES campaign(id) ON DELETE CASCADE
);

CREATE TABLE place_job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INT UNIQUE CONSTRAINT place_id_exists REFERENCES place(id) ,
    created TIMESTAMP NOT NULL,
    last_attempted TIMESTAMP,
    last_completed TIMESTAMP,
    enabled BOOLEAN NOT NULL
);
```
