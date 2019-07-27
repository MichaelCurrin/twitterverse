#!/usr/bin/env bash -e
# Regression test to Search API functionality which is done in util scripts.

source venv/bin/activate
cd app

echo 'Write to DB'
./utils/insert/search_and_store_tweets.py -p 1 -q '#Monday'
echo

echo 'Write to CSV'
./utils/extract/search.py fetch -q '#Monday'
