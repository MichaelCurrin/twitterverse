#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Category manager utility.

Manage values in the Category table and manage links between Category
and Profiles.
"""
import argparse
import os
import sys
# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))

from lib import database as db
from lib.tweets import assignProfileCategory
from lib.query.tweets.categories import printAvailableCategories,\
                                        printCategoriesAndProfiles


def main():
    """
    Handle command-line arguments to print or edit data.
    """
    parser = argparse.ArgumentParser(description="Category manager utility.")

    parser.add_argument('-a', '--available',
                        action='store_true',
                        help="Output available Categories in db, with Profile"
                             " counts for each then exit.")
    parser.add_argument('-s', '--summary',
                        action='store_true',
                        help="Output summary of Categories and Profiles then"
                             " exit.")
    parser.add_argument('-u', '--unassigned',
                        action='store_true',
                        help="Output list of Profiles which do yet have a"
                             " Category assigned to them then exit.")

    parser.add_argument('-c', '--category',
                        help="""Create input category, if it does not yet exist.
                             If --names argument is used with this, then
                             also assign this Category (by name or the
                             --available index) to all Profiles in the
                             screen names list.""")
    parser.add_argument('-n', '--names',
                        metavar='SCREEN_NAME',
                        nargs='+',
                        help="""Optional list of one or more screen names
                             (without leading @) of users in the db.
                             If provided, assign the input category to these
                             screen names, otherwise only attempt to create
                             the category.""")

    args = parser.parse_args()

    if args.available:
        printAvailableCategories()
    elif args.summary:
        printCategoriesAndProfiles()
    elif args.unassigned:
        for p in db.Profile.select(orderBy='screen_name'):
            if not p.categories.count():
                print u"@{screenName} | {name} | {followers:,d} followers"\
                .format(screenName=p.screenName, name=p.name,
                        followers=p.followersCount)
                print p.description
                print
    elif args.category:
        # Always attempt to create category, but only assign Profiles
        # if they are provided.
        if not args.names:
            assignProfileCategory(cat=args.category, screenNames=None)
        else:
            # Encode list of str command-line arguments as unicode.
            screenNames = [s.decode('utf-8') for s in args.names]

            if args.category.isdigit():
                # Get one item but decrease index by 1 since the available list
                # starts at 1.
                cat = db.Category.select()[int(args.category) - 1].name
            else:
                cat = args.category

            print "Category: {0}".format(cat)
            newCnt, existingCnt = assignProfileCategory(
                cat,
                screenNames=screenNames
            )
            print " - new links: {0:,d}".format(newCnt)
            print " - existing links found: {0:,d}".format(existingCnt)
    else:
        raise AssertionError("Invalid arguments. See --help.")


if __name__ == '__main__':
    main()
