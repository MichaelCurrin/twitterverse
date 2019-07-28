#!/bin/bash
###############################################################################
#
# Generate the topic stats report with a query to the database and send
# the results out to a pre-configured CSV file for the current date.
# Overwrites existing CSV for today's date, if one exists.
#
# This script must be run with app as current working directory.
#
# Usage:
# $ cd app
# $ ./utils/reporting/topic_stats_report.sh [pathToDB]
#     where pathToDB is the configured db path. Defaults to 'var/db.sqlite'
#     if not supplied.
#
# $ view var/reporting/
# Now you can view the report, which starts with topic_report in the name
# and has the current date. Any existing report on the day will be overwritten.
#
###############################################################################

# Check for first argument as db file name, otherwise use default.
if [[ ! -z "$1" ]]
  then
    DB_PATH="$1"
  else
    DB_PATH='var/db.sqlite'
fi
echo "DB path: $DB_PATH"

if [[ ! -r ${DB_PATH} ]]; then
  echo 'Could not find db file.'
  exit 1
fi

QUERY_PATH='lib/db_query/sql/topicStats.sql'
echo "Input query: ${QUERY_PATH}"

TODAY=$(date +'%Y-%m-%d')
CSV_PATH="var/reporting/topic_report_$TODAY.csv"

sqlite3 ${DB_PATH} -csv -header < ${QUERY_PATH} > ${CSV_PATH} \
  && echo "Output report: $CSV_PATH"
