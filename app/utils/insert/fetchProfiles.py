#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Profiles utility.

Get profile data from the Twitter API and add to the database. If a Category
is provided as argument, assign the Category to the Profile records.
"""
import argparse
import io
import os
import sys

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir,
                                                os.path.pardir)))
from lib import database as db
from lib.tweets import insertOrUpdateProfileBatch, assignProfileCategory


def main():
    """
    Command-line tool to add or update Profile records from list of Twitter
    screen names.

    Expects a list screen names, either from arguments list or to be read
    from a specified text file. If Category is provided, then assign to
    the Profiles.

    @return: None
    """
    parser = argparse.ArgumentParser(description="""Fetch Profiles Utility.
        Use the input from --file or --list arguments to lookup profiles from
        Twitter API and then add/update a record in the Profile table.
        Optionally assign a --category value to assign to Profiles input,
        or simply create the Category without assigning to Profiles input.""")

    parser.add_argument('--file',
                        metavar='PATH',
                        help="""Path to a text file, which has one screen name
                            per row and no row header or other data. """)

    parser.add_argument('--list',
                        metavar='SCREEN_NAME',
                        nargs='+',
                        help="""A list of one or more Twitter screen names,
                            separated by spaces.""")

    parser.add_argument('-n', '--no-fetch',
                        action='store_true',
                        help="""By default, fetch Profile data from Twitter
                            and insert or update locally. If this flag is
                            supplied, then do NOT fetch, but still print
                            screen names which would be fetched""")

    parser.add_argument('-c', '--category',
                        help="""Optional category name. If supplied, assign
                            all Profiles in the input to this Category,
                            creating the Category if it does not exist yet.
                            Category assignment is still done even if the
                            --no-fetch flag prevents fetching of Profile data
                            from the Twitter API. For convenience, if
                            the category argument is an integer, then the name
                            from the --available list is looked up and
                            assigned."""
                        )
    parser.add_argument('-a', '--available',
                        action='store_true',
                        help="""Boolean flag. If supplied, show available
                            Category names in the db with Profile counts and
                            exit.""")

    args = parser.parse_args()

    if args.available:
        print "     Category                  | Profiles"
        print "-------------------------------+---------"
        catList = db.Category.select()
        for i, v in enumerate(catList):
            print u'{index:3d}. {cat:25s} | {profCnt:7,d}'.format(
                index=i + 1, cat=v.name, profCnt=v.profiles.count()
            )
        print
    else:
        screenNames = None

        if args.file or args.list:
            if args.file:
                assert os.access(args.file, os.R_OK), \
                    "Unable to read path: {0}".format(args.file)
                # Read in as unicode text, in case of special characters.
                with io.open(args.file, 'r') as reader:
                    screenNames = reader.read().splitlines()
            else:
                # Encode list of str command-line arguments as unicode.
                screenNames = [s.decode('utf-8') for s in args.list]

            if args.no_fetch:
                print "Preview of input names:"
                for i, v in enumerate(screenNames):
                    print u'{index:3d}. {name:s}'.format(index=i + 1, name=v)
                print
            else:
                print "Inserting and updating profiles..."
                insertOrUpdateProfileBatch(screenNames)
        else:
            assert args.category, ("Either supply screen names using --file"
                                   " or --list, or supply --category name to"
                                   " be created.")
        # Assign categories last, so we have chance to create the Profiles
        # above.
        if args.category:
            if args.category.isdigit():
                # Get one item but decrease index by 1 since the available list
                # starts at 1.
                cat = db.Category.select()[int(args.category) - 1].name
            else:
                cat = args.category
            print "Category: {0}".format(cat)
            newCnt, existingCnt = assignProfileCategory(cat,
                                                        screenNames=screenNames)
            print " - new links: {0:,d}".format(newCnt)
            print " - existing links found: {0:,d}".format(existingCnt)


if __name__ == '__main__':
    main()
