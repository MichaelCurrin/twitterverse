#!/bin/bash

echo "PRINT TESTS"
echo "Preview out a record gets printed for model types."
echo

echo 'model trend columns'
# This test should fail if there are no records in Trend.
# In this test we do not hide the stdout.
python -c "from lib import database as db; print db.Trend.getColumnNames(); print; x = db.Trend.select().limit(1); data = x.getOne().getData(quiet=False) " && echo '-> success'
echo


echo 'model place columns'
# This test should fail if there are no records in Trend.
# In this test we do not hide the stdout.
python -c "from lib import database as db; print db.Place.getColumnNames(); print; x = db.Place.select().limit(1); data = x.getOne().getData(quiet=False) " && echo '-> success'
echo

echo 'model country columns'
# This test should fail if there are no records in Trend.
# In this test we do not hide the stdout.
python -c "from lib import database as db; print db.Country.getColumnNames(); print; x = db.Country.select().limit(1); data = x.getOne().getData(quiet=False) " && echo '-> success'
echo
