"""
Topic search application file.

Usage:
    $ python -m lib.db_query.search.topic --help
"""
from lib import database as db


def topic(searchStr='', orderByVol=False):
    """
    Search existing trends records in the db for topics matching the input
    string.

    Searches are case insensitive.

    :param searchStr: word or phrase as a string for text to search in the
        topic column of Trend table. Leave as default empty string to
        not filter results. Multi-word searches are not possible except as
        phrases.
    :param orderByVol: Default False. If True, order by volume descending
        instead of topic alphabetically.
    """
    orderBy = 'MaxVol DESC' if orderByVol else 'Trend.topic ASC'
    query = """
        SELECT Trend.topic, MAX(Trend.volume) AS MaxVol
        FROM Trend
        WHERE Trend.topic LIKE '%{0}%'
        GROUP BY Trend.topic
        ORDER BY {1}
    """.format(searchStr, orderBy)

    res = db.conn.queryAll(query)

    # Note that volume can be added up, but any null values will not be
    # counted.
    print('Max Volume | Topic')
    for item in res:
        # Making '' causes errors for some reason for "Динамо"
        print('{0:10,d} | {1}'.format(item[1] if item[1] else -1, item[0]))


def main(args):
    """
    Do a search by topic input string and print results.
    """
    # TODO: add order by vol as option

    if not args or set(args) & {'-h', '--help'}:
        print(
            'Usage: python -m lib.db_query.search.topic [searchStr] [-h|--help]')
        print('Options and arguments:')
        print('--help    : Show help.')
        print('searchStr : Enter a topic to search for in the database. Enter')
        print('            as `ALL` to show all records.')
    else:
        searchStr = '' if args[0] == 'ALL' else args[0]
        topic(searchStr, orderByVol=True)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
