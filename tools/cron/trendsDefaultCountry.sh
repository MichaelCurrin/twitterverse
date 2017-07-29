#!/bin/bash
# Bash script for doing a pull several times a day of trending topics for a
# configured country and its towns.
#
# Usage:
# In crontab, add a command change to the repo directory and then run this file from there.
# That will ensure everything is done from the correct path.
# e.g.
# 0	*/6	*	*	*	cd ~/path/to/twitterverse && ./tools/cron/trendsDefaultCountry.sh

source virtualenv/bin/activate
./app/utils/insert/trendsCountryAndTowns.py default

