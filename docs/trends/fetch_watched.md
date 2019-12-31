# Fetch trends
> How to fetch trending topic data for one or more locations


## Manual

### Help

View script help for [utils/insert/run_place_job_schedule.py](https://github.com/MichaelCurrin/twitterverse/blob/master/app/utils/insert/run_place_job_schedule.py).

```bash
$ ./utils/insert/run_place_job_schedule.py --help
```
```
Run all jobs in the db.
No options are available for this script.
```

### Fetch and insert

Get trends for all countries and towns enabled in the schedule.

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

## Cron

If you setup as a daily cron job, you will have a history of trend data for places in the database and can create reports using your recent or historical data.

To run the Python script above on a schedule, add the wrapping bash script to your crontab - [tools/trends_place_job.sh](https://github.com/MichaelCurrin/twitterverse/blob/master/tools/cron/trends_place_job.sh).

Edit crontab file.

```bash
$ crontab -e
```

Example:

```
0    0    *    *    *    cd <PATH_TO_REPO> && tools/cron/trends_place_job.sh
```

The benefit of the script is that is logs output to a file in the `app/var/log/cron` directory, although this could to be moved to within the Python script with a refactor and the bash script could be deleted.
