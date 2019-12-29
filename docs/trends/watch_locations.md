# Watch locations
> How to mark locations as watched for trending topics


## Place job schedule

The `PlaceJob` table in [models/cron_jobs.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/models/cron_jobs.py) is a schedule of `Place` records to watch. A place is watched if there is an entry for it in the `PlaceJob` table which has `enabled` set to `TRUE`.

The table also keeps track of the last successful attempt to store `Trend` records for that `Place`. This means that a cronjob can fetch data multiple times per day but skip any `Places` where there is already data stored for today.

## Job manager

There is a REPL to manage the place job schedule. You can see the script at [manager/jobs.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/manage/jobs.py).

Start the interactive mode below. Familiarize yourself with the interface, then exit it.

```bash
$ utils/manage/jobs.py --interactive
Job Manager interactive mode.

You are now viewing and editing PlaceJob table.

OPTIONS
 1) QUIT
 2) VIEW counts
 ...
```

Note that `VIEW ...` commands are do not alter anything so are safer to run repeatedly.

## Recommended watchlist

View the situations below and follow the steps which are appropriate.

- You only care about a handful of countries and/or towns.
    - Use the two `CREATE` options.
    - Use the `SINGLE - enable` option and choose places of interest.
- You want to watch all the data.
    - Use the `ALL - enable` option.
- You want to use the defaults provided with this project. i.e. All countries, plus towns in selected English-speaking countries.
    - Enter `12` to view pre-configured setup of countries and towns.
    - Insert them with `13`.

## Setup watchlist

Using the [Job manager](#job-manager) REPL and [Recommended watchlist](#recommended-watchlist) above, setup places to watch.
