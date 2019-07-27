#!/usr/bin/env bash -e -x
# Regression test to Search API functionality which is done in util scripts.
#
# Run this from app dir with venv activated.

echo "Not stored"

echo 'Write to DB'
./utils/insert/search_and_store_tweets.py -p 2 -q '#BlackFriday'
echo

echo 'Write to CSV'
./utils/extract/search.py fetch -p 2 -q '#BlackFriday'
echo


echo "Stored"
# Requires this named campaign to exist in the DB.

echo 'Write to DB'
./utils/insert/search_and_store_tweets.py -p 2 -c '#BlackFriday'
echo

echo 'Write to CSV'
./utils/extract/search.py fetch -p 2 -c '#BlackFriday'
echo
