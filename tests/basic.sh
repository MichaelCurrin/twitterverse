#!/bin/bash

source environment.sh

echo 'BASIC OPERATION TESTS'
echo

# Hide output but log as success. Errors are still shown.

echo 'setup conf'
python -m lib.config > /dev/null && echo '-> success'
echo

echo 'model'
python -m models.connection > /dev/null && echo '-> success'

echo
echo 'database'
python -m lib.database > /dev/null && echo '-> success'
echo

echo 'dbStats'
python -m lib.dbStats > /dev/null && echo '-> success'
echo

echo 'textHandling'
python lib/textHandling.py && echo '-> success'
echo


# This test only becomes meaningful when it has something useful to test and runs in main.
#echo 'trends'
#python lib/trends.py > /dev/null && echo '-> success'
#echo

# echo 'TwitterAuth'
# python lib/TwitterAuth.py > /dev/null && echo '-> success'
# echo

# how to measure success or failure and not args?
# if [[ "$0" -eq "0" ]]:
#   echo 'OK'
# else:
#   echo 'Fail'
# fi
# x=$(script) ?
