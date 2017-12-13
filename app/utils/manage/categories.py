#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Category manager utility.

Manage values in the Category table and manage links between Categories
and Profiles.
"""
import argparse
import os
import sys
# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir,
                                                os.path.pardir)))

from lib import database as db
from lib.tweets import assignProfileCategory
from lib.query.tweets.categories import printAvailableCategories,\
                                        printCategoriesAndProfiles,\
                                        printUnassignedProfiles


def main():
    """
    Handle command-line arguments to print or edit data.
    """
    parser = argparse.ArgumentParser(description="Category manager utility.")

    view = parser.add_argument_group("View", "Print data to stdout")
    view.add_argument(
        '-a', '--available',
        action='store_true',
        help="Output available Categories in db, with Profile counts for each."
    )
    view.add_argument(
        '-p', '--profiles',
        action='store_true',
        help="Output local Profiles grouped by Category."
    )
    view.add_argument(
        '-u', '--unassigned',
        action='store_true',
        help="""Output list of Profiles which do not yet have a Category
             assigned to them."""
    )

    update = parser.add_argument_group("Update", "Create or update Category"
                                       " names and assign Profile links")
    update.add_argument(
        '-c', '--category',
        help="""Create input category, if it does not yet exist. If --names
             argument is used with this, then also assign this Category
             (using name or row index in --available) to all given Profiles."""
    )
    update.add_argument(
        '-n', '--names',
        metavar='SCREEN_NAME',
        nargs='+',
        help="""Optional list of one or more screen names (without leading @)
             of users in the db. If provided, assign the input category to
             these screen names, otherwise only attempt to create the
             category."""
    )

    args = parser.parse_args()

    # Arguments are intended to be used alone, but could be combined.
    if args.available:
        printAvailableCategories()
    if args.profiles:
        printCategoriesAndProfiles()
    if args.unassigned:
        printUnassignedProfiles()
    if args.category:
        # Always attempt to create category, but only assign Profiles
        # if they are provided.
        if not args.names:
            assignProfileCategory(
                categoryName=args.category,
                screenNames=None
            )
        else:
            screenNames = [unicode(s) for s in args.names]

            # See this logic also in fetchProfiles.py script.
            # TODO: Move this to lib/tweets.py as a function.
            if args.category.isdigit():
                # Get one item but decrease index by 1 since the available list
                # starts at 1. Assume available list also uses sqlmeta default
                # ordering.
                categoryRec = db.Category.select()[int(args.category) - 1]
                categoryName = categoryRec.name
            else:
                categoryName = args.category

            print "Category: {0}".format(categoryName)
            newCnt, existingCnt = assignProfileCategory(
                categoryName=categoryName,
                screenNames=screenNames
            )
            print " - new links: {0:,d}".format(newCnt)
            print " - existing links found: {0:,d}".format(existingCnt)
    else:
        assert args.names is None, "--category is required if --names is set."


if __name__ == '__main__':
    main()
