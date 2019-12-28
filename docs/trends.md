# Trends usage

Twitter provides up to 50 trending topics a day for each location and this data changes through the day. This application allows you to watch 62 countries and over 400 towns/cities for which Twitter provides trending data.

However, if you probably want to narrow the list of places to watch, to save on time to query and data stored and reported on. This guide takes you through that.


Start in the project's app directory.

```bash
$ cd app
```

## Setup places

Ensure you have the DB setup and locations populated, as per [installation](installation.md).

Check the summary view to see how many records you have for Country, Trend, etc.

Below is an example view.


```bash
$ utils/db_manager.py --summary
Getting table summary...
Table           | Rows
================|===============
Place           |   471
Supername       |     1
Continent       |     6
Country         |    62
Town            |   402
Trend           |     0
Profile         |     0
Tweet           |     0
Category        |     4
ProfileCategory |     0
Campaign        |     0
TweetCampaign   |     0
PlaceJob        |     0
```

Note this uses ORM names and note DB schema names. This view includes all the countries and towns which Twitter provides data for in its API, plus some Place, Supername and Continent are used to give them more structure to allow say filtering towns in a certain country or continent.


## Setup jobs to watch places

### What is enabling?

The `PlaceJob` table is used to mark a `Place` record as watched (`enabled`) and when last successful attempt was made to store `Trend` records for that `Place`. This means that a cronjob can fetch data multiple times per day but skip any `Places` where there is already data stored for today.

### How to enable

Use the interactive REPL to manage the place job watchlist. It is a Python REPL.

```bash
$ utils/manage/jobs.py --interactive
Job Manager interactive mode.

You are now viewing and editing PlaceJob table.

OPTIONS
 0) QUIT
 1) VIEW counts
 ...
```


Familiarize yourself with the interface, in particular how to quit and how to see the menu again.

The `VIEW ...` commands are do not alter anything so are safer to run repeatedly.

### Recommended

View the situations below and follow the steps which are appropriate.

- You only care about a handful of countries and/or towns.
    - Use the two `CREATE` options.
    - Use the `SINGLE - enable` option and choose places of interest.
- You want to watch all the data.
    - Use the `ALL - enable` option.
- You want to use the defaults provided with this project. i.e. All countries, plus towns in selected English-speaking countries.
    - Enter `12` to view pre-configured setup of countries and towns.
    - Insert them with `13`.


## Fetch trend data

View help.

```bash
$ ./utils/insert/run_place_job_schedule.py --help
```
```
Run all jobs in the db.
No options are available for this script.
```

Do search.

```bash
$ ./utils/insert/run_place_job_schedule.py
```
```
Starting PlaceJob cron_jobs
  queued items: 30
12/28/19 23:29:34 Inserting trend data for WOEID 1
Generating API token...
Worldwide            | 50 topics added
  took 3s
12/28/19 23:29:46 Inserting trend data for WOEID 23424977
United States        | 50 topics added
  took 1s
...
```
