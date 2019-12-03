#!/usr/bin/env bash -e
# Regression test to Search API functionality which is done in utility scripts.
#
# Run after after DB has been setup and with venv active.
# For now, continue to use main DB and main credentials, rather than test DB.
echo "Not stored"
echo
echo 'Write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -q '#BlackFriday'
echo

echo 'Write to CSV script'
./utils/extract/search.py fetch -p 2 -q '#BlackFriday'
echo


echo "Stored"
# Requires this named campaign to exist in the DB.

echo 'Write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -c '#BlackFriday'
echo

echo 'Write to CSV script'
./utils/extract/search.py fetch -p 2 -c '#BlackFriday'
echo
