#!/bin/bash
# Get trending topics for all enabled places in the PlaceJob schedule table.
#
# This is a wrapper on a Python script, with the addition of logging to a file.

echo 'Getting trends for Places in PlaceJob table.'

TODAY=$(date +'%Y-%m-%d')
LOG_FILE="./app/var/log/cron/place_job_$TODAY.log"

echo "Writing to log file: $LOG_FILE"
echo "Also printing to standard out..."
echo

# Run the place job schedule script. Print results to console (unbuffered flag
# to get it in realtime) while also appending stdout to a log file named with
# today's date.
venv/bin/python -u app/utils/insert/run_place_job_schedule.py | tee -a $LOG_FILE
