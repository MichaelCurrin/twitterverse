"""
Database stats report for a preview of the row counts of each table.

Usage:
    $ python -m lib.db_query.schema.preview [limit]
    # => print results to console.
"""
import models


def showTableRecords(maxResults=10):
    """
    Print out results from each table up to a maximum number of records.
    """
    print("Results preview\n")
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        results = tableClass.select()
        limitedResults = results.limit(maxResults)

        heading = "{0} ({1})".format(tableName, results.count())
        print(heading)
        print("-" * len(heading))
        for r in limitedResults:
            print(r)
        print()
        print(limitedResults)
        print()
        print()


def main(args):
    """
    Execute showTableRecords function with specified limit otherwise default.
    """
    if args:
        showTableRecords(int(args[0]))
    else:
        showTableRecords()


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
