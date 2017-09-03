#!/bin/bash
# Bash script for doing a pull several times a day of trending topics for
# enabled places in the PlaceJob table.
#
# Usage:
# In crontab, add a command change to the repo directory and then run this file from there.
# That will ensure everything is done from the correct path.
# e.g.
# 0    0    *    *    *    cd ~/path/to/twitterverse && ./tools/cron/trendPlaceJob.sh

# Run the place job schedule script and send stdout and stderr to a file
# for the current day.

TODAY=$(date +'%Y-%m-%d')

source virtualenv/bin/actvate | exit 1
./app/utils/insert/runPlaceJobSchedule.py >> ./app/var/log/cron/place_job_$TODAY.log 2>&1
