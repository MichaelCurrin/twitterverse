"""
Report to show mapping of Places to each other, in a tree format.

Usage:
    $ python -m lib.db_query.place.tree
    # => print results to console.
"""
from lib import database as db


def printTree():
    """
    Print out data of all records in Place table.

    Records are grouped in a visual tree structure as child and parent objects.
    No items are repeated, except where two towns happen to have the same name
    in a minority of cases.

    There should only be one world record in Supername table, but allow
    for more.
    """
    supers = db.Supername.select()

    for s in supers:
        continents = s.hasContinents
        print(
            "* {name} ({count} continents)".format(name=s.name, count=len(continents))
        )

        for continent in continents:
            countries = continent.hasCountries
            print(f"  * {continent.name} ({len(countries)} countries)")

            for country in countries:
                towns = country.hasTowns
                print(f"    * {country.name} ({len(towns)} towns)")

                for town in towns:
                    print("      * {town.name}")


if __name__ == "__main__":
    printTree()
