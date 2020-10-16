"""
Database stats report to show how Places are mapped to each other, as child
and parent pairs.

Usage:
    $ python -m lib.db_query.place.pairs
    # => print results to console with default pipe separator.

    $ python -m lib.db_query.place.pairs --csv > ~/path/to/file.csv
    # => redirect output to CSV file with comma separation.
"""
from lib import database as db


def getPairs(args):
    """
    Create output showing Place objects mapped to parent Places in the DB.

    The output is shown as two columns. Parents place names are repeated.

    This can be exported to a CSV file using redirection. The CSV is ideal
    for uploading to Google Fusion tables as an input for a network graph.

    Entries in `Supername` table appear in parent column, but cannot be
    entered here as main places since they do not have a parent.
    """
    if not db.Continent.tableExists():
        print("Tables not setup yet. Skipping pairs printing.")

        return

    if set(args) & {"-c", "--csv"}:
        # Use comma separation and no padding.
        rowTemplate = "{0},{1}"
    else:
        # Use pipe separation and padding.
        rowTemplate = "{0:20} | {1:20}"

    data = [("Parent", "Child")]

    # Get continents and order by Super ID.
    for x in db.Continent.select().orderBy(db.Continent.q.supernameID):
        data.append((x.supername.name, x.name))

    # Get countries and order by continent ID.
    for x in db.Country.select().orderBy(db.Country.q.continentID):
        data.append((x.continent.name, x.name))

    # Get towns and order by country ID.
    for x in db.Town.select().orderBy(db.Town.q.countryID):
        data.append((x.country.name, x.name))

    for row in data:
        r = rowTemplate.format(*row)

        yield r


if __name__ == "__main__":
    import sys

    pairs = getPairs(sys.argv[1:])
    for p in pairs:
        print(p)
