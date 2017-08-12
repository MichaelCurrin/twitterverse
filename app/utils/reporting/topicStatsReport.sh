#!/bin/bash

# Usage:
# $ cd app
# $ ./topicStatsReport.sh
# $ ls ../../var/reporting
# Now you can view the report.

# # Assume this is run from dir of the script then change to app dir.
cd ../..

sqlite3 var/db.sqlite -csv -header \
  < lib/query/sql/topicStats.sql \
  > var/reporting/topic_report_$(date +"%y-%m-%d@%T").csv
