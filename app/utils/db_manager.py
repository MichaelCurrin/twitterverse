#!/usr/bin/env python
"""
DB manager utility.
"""
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from lib import database
from lib.db_query.schema import table_counts


HELP_MSG = f"""\
Usage: {__file__} [-p] [-s] [-d] [-c] [-P] [-h]

Options and arguments:
-h --help    : Show help and exit.
-p --path    : Show path to configured DB file.
-s --summary : Show summary of tables and records in DB.
-d --drop    : Drop all tables.
-c --create  : Create all tables in models, but do not drop or alter
               existing tables or modify their data. Then insert base data
               for Campaign and Category labels (see config file), so they
               can be assigned as labelling process within utilities.
               Even the Campaign or Category tables existed already, base
               records are still inserted. If a base record exists then its
               creation is skipped.
-P --populate: Populate tables with default location data and relationships.
               ONLY if used without other flags, accepts an optional
               integer as max number of towns to create from fixtures data.
               This is useful during development to save time, if only a few
               or no towns are needed.

Note:
  Flags can be combined. e.g. -p -d -c -P -s
  Actions will always be performed in a fixed order.
    i.e. drop -> create -> populate -> summary
"""


def main(args):
    """
    Main command-line entrypoint.
    """
    if len(args) == 0 or set(args) & {"-h", "--help"}:
        print(HELP_MSG)

        return HELP_MSG
    else:
        if set(args) & {"-p", "--path"}:
            database._path()

        if set(args) & {"-d", "--drop"}:
            confirm_drop = input("Are you sure you want to DROP all tables? [Y/N] /> ")
            if confirm_drop.strip().lower() in ("y", "yes"):
                database._dropTables()
            else:
                print("Cancelled dropping tables. Exiting.")

                return None

        if set(args) & {"-c", "--create"}:
            database._createTables()
            database._baseLabels()

        if set(args) & {"-P", "--populate"}:
            if len(args) == 2 and args[1].isdigit():
                limit = int(args[1])
            else:
                limit = None
            database._populate(limit)

        if set(args) & {"-s", "--summary"}:
            print("Getting table summary...")
            table_counts.showTableCounts()


if __name__ == "__main__":
    main(sys.argv[1:])
