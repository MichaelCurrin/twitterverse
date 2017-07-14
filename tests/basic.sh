#!/bin/env bash
echo "Starting tests."
cd ../app

pwd
echo

# how to exit with error code like python exit(1)?
#source ../virtualenv/bin/actvate || echo "ERROR Could not activate virtual env"; exit
# Temporary solution.
# exit? see example
echo "Virtual env"
source ~/.local/bin/twitterverse/bin/activate || echo "fail"
echo "active"

# Hide output but log as success. Errors are still shown.
echo 'setupConf'
python lib/setupConf.py > /dev/null && echo '-> success'
echo
echo 'model'
python models/model.py > /dev/null && echo '-> success'
echo
echo 'database'
python lib/database.py > /dev/null && echo '-> success'
echo
echo 'dbQueries'
python lib/dbQueries.py > /dev/null && echo '-> success'
echo
echo 'textHandling'
python lib/textHandling.py > /dev/null && echo '-> success'
echo
echo 'trends'
python lib/trends.py > /dev/null && echo '-> success'
echo

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
