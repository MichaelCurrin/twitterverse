# Watch Influencers
> Watch influential profiles and their tweets.

Steps are to get list of influential Twitter profiles from a listing, add them to the DB and insert their profiles and tweets. Optionally add cron job to lookup new tweets.

## Setup

### 1. Create screen names in text files

If you prefer to compile a list of handles using the command-line instead, skip to step 2.

Scrape popular Twitter account screen names from [SocialBlade.com](https://socialblade.com) and add text files with appropriate names. This process takes a few seconds. It is described here as a manual process to be run once-off or occasionally, though it could be automated.

The source site has static HTML with the top screen names across four categories, allowing a view either top 10 or top 100. Note that some categories like most tweets include Twitter accounts which are tests (they have test in the same) or bots (they offer a service to send Tweets to use on request of on schedule).

There will be some overlap in Twitter profiles appearing across the 4 lists, so even if you lookup four lists of 100 you will probably get slightly less than 400 unique profiles stored in your Profile table.

```bash
$ ./utils/influencer_scraper.py --help
```

Get 10 users in each category.

```bash
$ ./utils/influencer_scraper.py short
```

    Output dir: <PATH_TO_REPO>/app/var/lib/influencer_scraper
    Wrote: followers-short-2017-12-03.txt
    Wrote: following-short-2017-12-03.txt
    Wrote: tweets-short-2017-12-03.txt
    Wrote: engagements-short-2017-12-03.txt

The contents of the files are used as input for the next step. There may be duplication of users across files, but this is fine as the user can be added to the DB under two Category labels.

The files can be created or maintained by hand as well.

<!-- _TODO: Add sample file or steps to hand compile text file._ -->

### 2. Create Profile records

Use the generated text files of screen names from above, or input handles by hand.

In one command, the following steps happen:

1. Lookup profile data on the Twitter API using given handles.
2. Create Profile records in the DB.
3. Assign Category labels to the Profile records.

Tips:

- The screen names provided to the API are not case-sensitive.
- Note the the `--no-fetch` command if you want to experiment and print without storing data. See help:
    ```bash
    $ ./utils/insert/fetch_profiles.py --help
    ```

Fetch a list of profiles and assign categories, using the fetch profiles utility. A Category is a list of Profiles which makes them easier to fetch tweets for and to report on. You can have as many Category groups as you like.

- Provide handles in text file. An example file path is used below.
    ```bash
    $ # Preview.
    $ ./utils/insert/fetch_profiles.py --no-fetch --file var/lib/influencer_scraper/following-short-2017-12-03.txt
    6BillionPeople
    ArabicBest
    MixMastaKing
    ...
    ```
    ```bash
    $ # Assign custom category (created if it does not exist) and the system influencers label.
    $ ./utils/insert/fetch_profiles.py --file var/lib/influencer_scraper/following-short-2017-12-03.txt \
        --category 'Top Following' --influencers
    ```
- Provide handles as arguments.
    ```bash
    $ # Screen names as command-line list.
    $ ./utils/insert/fetch_profiles.py --category 'My watchlist' --list foo bar bazz
    ```

View the results using the _Category Manager_ utility. A category of thousands of profiles may take a few seconds to read and print.

```bash
$ ./utils/manage/categories.py view --profiles
1. Top Following   10 profiles
   - @6BillionPeople       | MarQuis Trill | Bitcoin Ethereum Litecoin Investor
   - @ArabicBest           | الاكثر تاثيرا
   - @MixMastaKing         | MEGAMIX CHAMPION
   ...

2. _TOP_INFLUENCER 10 profiles
   - @6BillionPeople       | MarQuis Trill | Bitcoin Ethereum Litecoin Investor
   - @ArabicBest           | الاكثر تاثيرا
   - @MixMastaKing         | MEGAMIX CHAMPION
   ...

3. My watchlist        3 profiles
   - @foo             | Foo
   - @bar             | Mr Bar
   - @bazz            | bazz
```

## Fetch Profiles in Categories

```bash
$ # Get default number of tweets (200) for each Profile, for given Categories.
$ ./utils/insert/fetch_tweets.py -c 'Top Engagements' 'Top Followers'
Fetching Tweets for 197 Profiles
...

$ ./utils/insert/fetch_tweets.py --categories _TOP_INFLUENCER --tweets-per-profile 25 --verbose
Fetching Tweets for 364 Profiles
...
```

<!-- _TODO: write/improve crontab instructions in full. The influencer scraper is not a good candidate for crontab since it is best used when manually labelling new Profiles in the top 100 and the top 10 will likely be changing often but still in the added top 100. Consider updating all profiles with crontab, so bios and followers are kept up to date weekly, since the calls are inexpensive when not getting Tweets_ -->
