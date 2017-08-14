# -*- coding: utf-8 -*-
"""
Receive SQL query in stdin, send to configured database file, then return
the query result rows.

Usage:
    $ echo "SELECT * FROM Trend LIMIT 10" | python -m lib.query.doQuery

    $ python -m lib.query.doQuery < lib/query/sql/abc.sql \
        > var/reporting/abc.csv

TODO
    Test with u'\xed' character
"""
import sys

from lib import database as db


def quote(phrase):
    """
    Remove double-quotes from a string and if there is a comma then returns
    value enclosed in double-quotes (ideal for outputting to CSV).

    @param phrase: a string.
    """
    # Remove double-quotes.
    phrase = phrase.replace('"', "'")
    # Add quotes if there is a comma.
    phrase = '"{}"'.format(phrase) if ',' in phrase else phrase
    return phrase


def main(inputFile):
    """
    Receive a SQL query as a string and execute then print results to stdout.
    """
    for rowList in db.conn.queryAll(inputFile):
        # Any unicode characters will be lost (replaced with question marks)
        # by converting to str.
        rowStr = (quote(str(c)) for c in rowList)
        print ','.join(rowStr)


if __name__ == '__main__':
    main(sys.stdin.read())
