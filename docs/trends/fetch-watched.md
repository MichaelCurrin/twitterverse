# Fetch watched
> How to fetch trending topic data for one or more locations on the watched list.


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

For each country and town enabled in the schedule, get trends for the current time.

```bash
$ ./utils/insert/run_place_job_schedule.py
```

In this output example, there are 30 items which are enabled and have not been run today. So the script runs through each of them.
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

On a repeat run, any items already successfully completed for today will be skipped. Such as in this second output example.

```
Starting PlaceJob cron_jobs
  queued items: 0
```


## Get trends on daily schedule

If you setup as a daily cron job, you will have a history of trend data for places in the database and can create reports using your recent or historical data.

To run the Python script above on a schedule, add the wrapping bash script to your crontab - [tools/trends_place_job.sh](https://github.com/MichaelCurrin/twitterverse/blob/master/tools/cron/trends_place_job.sh). 

_Note: The benefit of this bash script is that it activates the virtual env internally and logs output to a file in the `app/var/log/cron` directory. Though, this logging logic could to be moved to within the Python script with a refactor so the bash script could be deleted._

### Test

You can test it directly from the project root and cancel it immediately.

```bash
$ tools/cron/trends_place_job.sh
...
```

### Add to cron schedule.

Edit your crontab file.

```bash
$ crontab -e
```

Example of running daily at midnight:

```
0    0    *    *    *    cd <PATH_TO_REPO> && tools/cron/trends_place_job.sh
```
