#!/bin/bash
# Bash script for doing a pull several times a day of trending topics for a
# configured country and its towns.
#
# Usage:
# In crontab, add a command change to the repo directory and then run this file from there.
# That will ensure everything is done from the correct path.
# e.g.
# 0    */6     *   *   *    cd ~/path/to/twitterverse && ./tools/cron/trendsDefaultCountry.sh --default
# 0    */12    *   *   *    cd ~/path/to/twitterverse && ./tools/cron/trendsDefaultCountry.sh United States

if [[ $# -eq 0 ]]; then
  echo "No arguments supplied. Country name or --default flag is required."
  exit 1
fi

# `$*` to use all args, for entering of multi-word countries.
source virtualenv/bin/activate && ./app/utils/insert/trendsCountryAndTowns.py $*
