#!/bin/bash
echo "Starting tests."
cd ..
pwd
echo

echo "Virtual env"
if [ -d "virtualenv" ]; then
  echo "Found virtualenv folder or symlink"
else
  echo "Could not find virtualenv folder or symlink. Create it and install the packages in requirements.txt inside it."; exit 1
fi;

pwd
# Todo - how to exit on failure?
source virtualenv/bin/activate || echo "failed to activate"
echo "activated"

cd app
pwd

# Hide output but log as success. Errors are still shown.
echo 'setupConf'
python lib/setupConf.py > /dev/null && echo '-> success'
echo
echo 'model'
python models/model.py > /dev/null && echo '-> success'

echo
echo 'Setup tables if they do not exist'
python lib/database.py -c "initialise()" \
   > /dev/null && echo '-> success'
echo

echo 'dbQueries'
python lib/dbQueries.py > /dev/null && echo '-> success'
echo

echo 'textHandling'
python lib/textHandling.py > /dev/null && echo '-> success'
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
