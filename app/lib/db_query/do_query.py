"""
Receive SQL query in stdin, send to configured database file, then return
the query result rows.

Note that db queries don't have to done through python like this,
but can be done in SQL directly. For example:
    $ sqlite3 path/to/db -csv -header < path/to/query > path/to/report
However this script will use the configured DB for you.

Usage:
    ## methods of input:

    # Pipe text to the script.
    $ echo "SELECT * FROM Trend LIMIT 10" | python -m lib.db_query.do_query

    # Redirect text from .sql file to the script.
    $ python -m lib.db_query.do_query --csv < lib/query/sql/abc.sql \
        > var/reporting/abc.csv

    # Enter an ad hoc query in lines of stdin. Use ctrl+D to signal EOF.
    $ python -m lib.db_query.do_query <enter>
        SELECT *
        FROM Trend LIMIT 10;
        <ctrl+D>


    ## Methods to output:

    # Print to console
    $ python -m lib.db_query.do_query < abc.sql

    # Write to CSV
    $ python -m lib.db_query.do_query --csv < abc.sql > abc.csv

TODO:
    * Test printing with '\xed' character
    * Instead of getting from stdin, accept a single quoted query with
        without line breaks.
        e.g. python -m lib.db_query.do_query -q 'SELECT a
            FROM b;'
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

    :param cell: any python object representing a cell value from a table row.

    :return: stringified version of the input cell value, with CSV
        formatting applied.
    """
    if cell is None:
        return ''
    else:
        phrase = str(cell)
        # Remove double-quotes.
        phrase = phrase.replace('"', "'")
        # Add quotes if there is a comma.
        phrase = f'"{phrase}"' if ',' in phrase else phrase

        return phrase


def main(args, query=None):
    """
    Receive a SQL query as a string and execute then print results to stdout.
    """
    if set(args) & {'-h', '--help'}:
        print('Usage: python -m lib.db_query.sql.do_query [-c|--csv]'
              ' [-s|--summary] [-h|--help]')
        print('    A query is required in stdin.')
        print('Options and arguments:')
        print('--help    : show help.')
        print('--csv     : default behaviour is print rows as tuples. The CSV')
        print('            flags makes results return in a format ideal for')
        print('            writing out to a CSV file. i.e. comma separate')
        print('            values without tuple brackets and quoting any')
        print('            strings containing a comma. Headers are still')
        print('            excluded.')
        print('--summary : print only count of rows returned.')
    else:
        if not query:
            query = sys.stdin.read()
            if not query:
                raise ValueError('Database query is required as stdin.')

        results = db.conn.queryAll(query)

        if set(args) & {'-s', '--summary'}:
            print(len(results))
        elif set(args) & {'-c', '--csv'}:
            for row in results:
                # Any unicode characters will be lost (replaced with
                # question marks) by converting to str.
                rowStr = (formatForCSV(c) for c in row)
                print(','.join(rowStr))
        else:
            for row in results:
                print(row)


if __name__ == '__main__':
    main(sys.argv[1:])
