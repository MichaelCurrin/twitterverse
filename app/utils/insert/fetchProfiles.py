#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Profiles utility.

Get profile data from the Twitter API and add to the database. If a Category
is provided as argument, assign the Category to the Profile records.
"""
import argparse
import os
import sys

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir,
                                                os.path.pardir)))
from lib import database as db
from lib.config import AppConf
from lib.tweets import insertOrUpdateProfileBatch, assignProfileCategory
from lib.query.tweets.categories import printAvailableCategories


conf = AppConf()

# If an argument indicates that the input is of influencers, then assign
# this Category to Profiles. This is done independently of the custom category
# provided with the --category argument.
INFLUENCER_LABEL = u"_TOP_INFLUENCER"


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
        Optionally assign an influencer category name and/or a custom category
        name to Profiles.""")

    viewGrp = parser.add_argument_group("View", "Print data to stdout")
    viewGrp.add_argument(
        '-a', '--available',
        action='store_true',
        help="""If supplied, show available Category names in the db with
            Profile counts, then exit."""
    )

    usersGrp = parser.add_argument_group("Users",
                                         "Process Twitter screen names")
    usersGrp.add_argument(
        '--file',
        metavar='PATH',
        help="""Path to a text file, which has one screen name per row and no
            row header or other data. It is recommended to run the
            influencer scraper utility and then set PATH as path to one
            of the generated files in the output directory, which is currently
            configured as: {0}
            """.format(conf.get('Scraper', 'outputDir'))
    )
    usersGrp.add_argument(
        '--list',
        metavar='SCREEN_NAME',
        nargs='+',
        help="A list of one or more Twitter screen names, separated by spaces."
    )
    usersGrp.add_argument(
        '-n', '--no-fetch',
        action='store_true',
        help="""Use this flag to print out the input screen names without
            fetching any data or assigning categories. This is useful to
            preview the screen names input and then remove the flag to fetch
            the data."""
    )

    categoriesGrp = parser.add_argument_group("Categories", """Assign categories
                                              to input profiles named in Users
                                              section""")
    categoriesGrp.add_argument(
        '-i', '--influencers',
        action='store_true',
        help="""If this flag is supplied, assign the configured influencer
            category '{0}' to fetched Profiles. This works independently of the
            --category argument but it is recommended to use both at once.
        """.format(INFLUENCER_LABEL)
    )
    # TODO: Consider splitting the index out as a separate argument.
    categoriesGrp.add_argument(
        '-c', '--category',
        help="""Custom category name (quoted if multiple words) or integer for
            category index. If supplied, assign all Profiles in the input
            to this Category, creating the Category if it does not exist yet.
            If the category argument is an integer, then the name from the
            --available list is looked up and and used as the Category (this
            index is convenient for manual use but should not be used in a
            cron job, since the same index could reference different values
            over time)."""
    )

    args = parser.parse_args()

    if args.available:
        printAvailableCategories()
    elif args.file or args.list:
        if args.file:
            assert os.access(args.file, os.R_OK), \
                "Unable to read path: {0}".format(args.file)
            with open(args.file, 'rb') as reader:
                screenNames = reader.read().splitlines()
        else:
            screenNames = args.list

        if args.no_fetch:
            print "Preview of input names:"
            for i, v in enumerate(screenNames):
                print "{index:3d}. {name:s}".format(index=i + 1, name=v)
            print
        else:
            print "Inserting and updating profiles..."
            # Split out the failed names so they be skipped in the Category
            # assignment step. Most errors are handled in the function,
            # but, if this script is interrupted while fetching then no
            # categories will be allocated to any Profiles which were created.
            successNames, failureNames = insertOrUpdateProfileBatch(screenNames)
            print "Successes: {0}".format(len(successNames))
            print "Failures: {0}".format(len(failureNames))

            if args.influencers:
                print "Assign category: {0}".format(INFLUENCER_LABEL)
                newCnt, existingCnt = assignProfileCategory(
                    categoryName=INFLUENCER_LABEL,
                    screenNames=successNames
                )
                print " - new links: {0:,d}".format(newCnt)
                print " - existing links found: {0:,d}".format(existingCnt)
                print

            if args.category:
                if args.category.isdigit():
                    # Get one item but decrease index by 1 since the available
                    # list starts at 1.
                    categoryRec = db.Category.select()[int(args.category) - 1]
                    categoryName = categoryRec.name
                else:
                    categoryName = args.category

                print "Assign category: {0}".format(categoryName)
                newCnt, existingCnt = assignProfileCategory(
                    categoryName=categoryName,
                    screenNames=successNames
                )
                print " - new links: {0:,d}".format(newCnt)
                print " - existing links found: {0:,d}".format(existingCnt)


if __name__ == '__main__':
    main()
