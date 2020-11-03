#!/usr/bin/env bash
# Regression test to Search API functionality which is done in utility scripts.
#
# Run after DB has been setup with tables and with venv active.
# For now, continue to use main DB and main credentials, rather than test DB.
#
# Use an arbitrary search term which will have volume. And just get a page
# or two.

# TODO: Find a way to run against test DB but with actual API credentials.
# export TEST_MODE=1
# Read that in the config.
# Then make a dev confg file.

set -e

echo "Using query"
# Note that tweets will be added agains the _SEARCH_QUERY base campaign
# but note against a specific campaign.
echo
echo 'Use write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -q 'hello'
echo

echo 'Use write to CSV script'
./utils/extract/search.py fetch -p 2 -q 'hello'
echo

echo "Setup test campaign if it does not exist"
./utils/manage/campaigns.py -c '_TEST_SEARCH' -q 'hello'
echo

echo "Using campaign"

echo 'Use write to DB script'
./utils/insert/search_and_store_tweets.py -p 2 -c '_TEST_SEARCH'
echo

echo 'Use write to CSV script'
./utils/extract/search.py fetch -p 2 -c '_TEST_SEARCH'
echo
