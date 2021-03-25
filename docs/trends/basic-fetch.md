# Basic fetch
> Fetch fetch of trending topics using name of a location.

This approach requires the [seed locations](trends/seed-locations.md) step to be completed.

## Manual

Utility to get and store trend data for a country and its towns.

```bash
$ cd app
$ utils/insert/trends_country_and_towns.py
```

## Cron

Add the script above as a cronjob.

Edit crontab file.

```bash
$ crontab -e
```

Examples:

```
0    */6     *   *   *    cd <PATH_TO_REPO> && venv/bin/python app/utils/insert/trends_country_and_towns.py --default
0    */12    *   *   *    cd <PATH_TO_REPO> && venv/bin/python app/utils/insert/trends_country_and_towns.py United States
```
