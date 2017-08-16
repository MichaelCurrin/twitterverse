#!/bin/bash
###############################################################################
#
# Generate the topic stats report with a query to the database and send
# the results out to a pre-configured CSV file for the current date.
#
# This script must be run with app as current working directory.
#
# Usage:
# $ cd app
# $ ./utils/reporting/topicStatsReport.sh [pathToDB]
#     where pathToDB is the configured db path. Defaults to 'var/db.sqlite'
#     if not supplied.
#
# $ view var/reporting/
# Now you can view the report, which starts with topic_report in the name
# and has the current date. Any existing report on the day will be overwritten.
#
###############################################################################


# Check for first argument otherwise use the default.
if [ ! -z "$1" ]
  then
    dbName=$1
  else
    dbName=db.sqlite
fi

echo DB path: $dbName

inPath=lib/query/sql/topicStats.sql
echo Report: $inPath

outPath=var/reporting/topic_report_$(date +"%y-%m-%d").csv

sqlite3 $dbName -csv -header < $inPath > $outPath && echo Output: $outPath
