#!/bin/bash
# Bash script for doing a pull several times a day of trending topics for
# enabled places in the PlaceJob table.
#
# Usage:
# This script must be run with twitterverse as the working directory.
# In crontab, add a command change to the repo directory and then run this file from there.
# That will ensure everything is done from the correct path.
# e.g.
# 0    0    *    *    *    cd ~/path/to/twitterverse && ./tools/cron/trendPlaceJob.sh

echo 'Getting trends for Places in PlaceJob table.'

source virtualenv/bin/activate || exit 1

TODAY=$(date +'%Y-%m-%d')
LOG_FILE="./app/var/log/cron/place_job_$TODAY.log"

echo "Writing to log file: $LOG_FILE"
echo "Also printing to standard out..."
echo

# Run the place job schedule script. Print results to console (unbuffered
# flag to get it in realtime) while also appending stdout to a log file named
# with today's date.
python -u app/utils/insert/runPlaceJobSchedule.py | tee -a $LOG_FILE
