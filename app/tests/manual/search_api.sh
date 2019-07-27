#!/usr/bin/env bash -e
# Regression test to Search API functionality which is done in util scripts.
#
# Run this from app dir with venv activated.

echo 'Write to DB'
./utils/insert/search_and_store_tweets.py -p 2 -q '#Friday'
echo

echo 'Write to CSV'
./utils/extract/search.py fetch -p 2 -q '#Friday'
