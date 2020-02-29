r"""
DB query module.

Receive SQL query in stdin, send to configured database file, then return
the query result rows.

Note that DB queries don't have to done through Python like this,
but can be done with sqlite3 command directly. For example:

    $ sqlite3 <PATH_TO_DB_FILE> -csv -header < <PATH_TO_QUERY> > <PATH_TO_REPORT>

However, this script will automatically choose the configured DB for you.

This script was done to avoid an issue when running an old SQLite version,
but it turned out that this script had no advantage as the query was still
limited by the system SQLite version.


Usage:

    ## Methods of input:

    $ # Pipe text to the script.
    $ echo "SELECT * FROM Trend LIMIT 10" | python -m lib.db_query.do_query

    $ # Redirect text from .sql file to the script.
    $ python -m lib.db_query.do_query --csv < lib/query/sql/abc.sql \
        > var/reporting/abc.csv

    $ # Enter an ad hoc query in lines of stdin. Use ctrl+D to signal EOF.
    $ python -m lib.db_query.do_query <enter>
        SELECT *
        FROM Trend LIMIT 10;
        <CTRL + D>


    ## Methods to output:

    $ # Print to console
    $ python -m lib.db_query.do_query < abc.sql

    $ # Write to CSV
    $ python -m lib.db_query.do_query --csv < abc.sql > abc.csv


TODO:
    * Test printing with '\xed' character
    * Instead of getting from stdin, accept a single quoted query with
        without line breaks.
        e.g. python -m lib.db_query.do_query -q 'SELECT a
            FROM b;'
    * Move these instructions to docs.
"""
import sys

from lib import database as db


def formatForCSV(cell):
    """
    Convert a value to a value appropriate for a CSV.

    This is a basic implementation - there are probably much better ways to
    do with the stdlib such csv library.

    Removes double-quotes from a string and if there is a comma then returns
    value enclosed in double-quotes (ideal for outputting to CSV).

    Null values are returned as an empty string.

    TODO: If the data required in more than just a trending topic
    (e.g. user tweets) then it may be better to use the CSV module instead.

    :param cell: Any python object representing a cell value from a table row.

    :return: Stringified version of the input cell value, with CSV
        formatting applied.
    """
    if cell is None:
        return ''

    phrase = str(cell)
    # Remove double-quotes.
    phrase = phrase.replace('"', "'")
    # Add quotes if there is a comma.
    phrase = f'"{phrase}"' if ',' in phrase else phrase

    return phrase


def print_row(row, as_csv):
    """
    Print given row using optional CSV formatting.

    :return: None
    """
    if as_csv:
        # Any unicode characters will be lost (replaced with
        # question marks) by converting to str.
        rowStr = (formatForCSV(c) for c in row)
        print(','.join(rowStr))
    else:
        print(row)


def process(query, do_summary, as_csv):
    """
    Execute query and print results.

    The field names are included in the output. Note that the names this will
    not always be so readable, depending on your query. So in your SQL,
    preferably use an alias field name. Otherwise you will get something
    like "CASE ... END".
    """
    results = db.conn.queryAllDescription(query)

    if do_summary:
        print(len(results))
    else:
        header_row, data_rows = results
        header_names = [x[0] for x in header_row]

        print_row(header_names, as_csv)
        for row in data_rows:
            print_row(row, as_csv)


def main(args):
    """
    Main command-line function.
    """
    if set(args) & {'-h', '--help'}:
        print('Usage: python -m lib.db_query.sql.do_query [-c] [-s] [-h]')
        print()
        print('Execute a SQL query provided on stdin and print results')
        print('The default behaviour is print rows as tuples.')
        print()
        print('Options and arguments:')
        print('-c --csv     : The CSV flags makes results return in a format')
        print('               ideal for writing out to a CSV file. i.e. comma')
        print('               separated values without tuple brackets and ')
        print('               quoting any strings containing a comma. ')
        print('-s --summary : print only count of rows returned.')
        print('-h --help    : show help.')

        return

    query = sys.stdin.read()
    if not query:
        raise ValueError('A database query is required on stdin.')

    do_summary = set(args) & {'-s', '--summary'}
    as_csv = set(args) & {'-c', '--csv'}

    process(query, do_summary, as_csv)


if __name__ == '__main__':
    main(sys.argv[1:])
