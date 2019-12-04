#!/usr/bin/env bash -e
# Regression test to Search API functionality which is done in utility scripts.
#
# Run after after DB has been setup and with venv active.
# For now, continue to use main DB and main credentials, rather than test DB.
#
# Use an arbitrary search term which will have volume. And just get a page
# or two.

echo "Using query"
echo
echo 'Use write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -q 'hello'
echo

echo 'Use write to CSV script'
./utils/extract/search.py fetch -p 2 -q 'hello'
echo

echo "Setup test campaign if it does not exist"
utils/manage/campaigns.py -c '_TEST_SEARCH' -q 'hello'
echo

echo "Using campaign"

echo 'Use write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -c '_TEST_SEARCH'
echo

echo 'Use write to CSV script'
./utils/extract/search.py fetch -p 2 -c '_TEST_SEARCH'
echo
