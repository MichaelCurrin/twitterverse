#!/usr/bin/env python
"""
Utility to get and store trend data for a country and its towns.

This expects a single country name then looks up the WOEID of the country
and child towns from the DB, then gets trending data for each.
"""
# Allow imports to be done when executing this file directly.
import os
import sys
import time

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
    ),
)

from lib import places, trends
from lib.config import AppConf
from lib.db_query.place import country_report

appConf = AppConf()

HELP = f"""\
Usage: {os.path.basename(__file__)} [-dsnfh] [COUNTRY_NAME]

The COUNTRY_NAME argument can be omitted if `--fast` or `--show` flags are
used.

Flags:
-h, --help    Show this message and exit.
-d, --default Use country configured in config file.
-s, --show    List available countries and exit.
-n,--no-store Do not persist the fetched data.
-f, --fast    Fast mode. Override the waiting behavior, which means queries
              will be done in quick succession, at least within each 15 min
              rate-limited window.
"""


def listCountries():
    print("See available countries below...\n")
    country_report.showTownCountByCountry(by_name=True)

    print("Enter a country name from the above an argument.")
    print(
        "Or, use `--default` flag to get the configured country, which "
        "is currently `{}`.".format(appConf.get("TrendCron", "countryName"))
    )


def main(args):
    """
    Command-line entry point to get Twitter API trending data.

    The max time is set in the app configuration file. If the duration of the
    current iteration was less than the required max then we sleep for the
    remaining number of seconds to make the iteration's total time close to 12
    seconds. If the duration was more, or the max was configured to zero, no
    waiting is applied.

    # TODO: Refactor to have less in this function.
    """
    if not args or set(args) & {"-h", "--help"}:
        print(
            HELP,
            file=sys.stderr,
        )
        sys.exit(1)
    elif set(args) & {"-s", "--show"}:
        listCountries()
    else:
        print("Starting job for trends by country and towns.")
        if set(args) & {"-d", "--default"}:
            # Use configured country name.
            countryName = appConf.get("TrendCron", "countryName")
        else:
            # Set country name string from arguments list, ignoring flags.
            words = [word for word in args if not word.startswith("-")]
            countryName = " ".join(words)
        assert countryName, "Country name input is missing."

        if set(args) & {"-f", "--fast"}:
            minSeconds = 0
        else:
            minSeconds = appConf.getint("TrendCron", "minSeconds")

        woeidIDs = places.countryAndTowns(countryName)
        delete = bool(set(args) & {"-n", "--no-store"})

        for woeid in woeidIDs:
            start = time.time()
            trends.insertTrendsForWoeid(woeid, delete=delete)
            duration = time.time() - start

            print("  took {}s".format(int(duration)))
            diff = minSeconds - duration
            if diff > 0:
                time.sleep(diff)


if __name__ == "__main__":
    main(sys.argv[1:])
