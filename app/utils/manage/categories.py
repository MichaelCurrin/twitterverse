#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Category manager utility.

Manage values in the Category table and manage links between Categories
and Profiles.
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import os
import sys
import webbrowser

from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import DuplicateEntryError
from sqlobject.sqlbuilder import IN
from six.moves import input

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))

from lib import database as db
from lib.tweets import assignProfileCategory
from lib.db_query.tweets.categories import (
    printAvailableCategories,
    printCategoriesAndProfiles,
    printUnassignedProfiles
)


def view(args):
    """
    Handle the view subcommand.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments. Arguments are intended to be used alone, but
        could be combined.

    :return: None
    """
    if args.available:
        printAvailableCategories()
    if args.profiles:
        printCategoriesAndProfiles()
    if args.unassigned:
        printUnassignedProfiles()


def add(args):
    """
    Handle the add subcommand.

    Always attempt to create a category otherwise fetch the existing one.
    If Profile names are provided, assign the Category to those Profiles.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments.

    :return: None
    """
    screenNames = [s.encode('utf-8') for s in args.names] if args.names \
        else None

    if screenNames and args.category.isdigit():
        # Get one item but decrease index by 1 since the available list
        # starts at 1. Assume available list also uses sqlmeta default
        # ordering.
        categoryRec = db.Category.select()[int(args.category) - 1]
        categoryName = categoryRec.name
    else:
        categoryName = args.category

    print("Category: {0}".format(categoryName))
    newCnt, existingCnt = assignProfileCategory(
        categoryName=categoryName,
        screenNames=screenNames
    )
    print(" - new links: {0:,d}".format(newCnt))
    print(" - existing links found: {0:,d}".format(existingCnt))


def runBulkCategoryUpdater(profiles):
    """
    Interactive command-line tool iterate through all Profiles and manage
    Categories for each. Allows skipping and exiting.

    :param profiles: Profile records to iterate over, as SelectResults object.

    :return: None
    """
    instructions = """Commands:
* .help             Show this help message.
  .h
* CATEGORY          Name of existing category to assign to Profile.
                    Use a minus as a prefix to remove the link.
* N                 Integer as index reference for existing Category to assign
                    to the Profile. Use a minus as prefix to remove the link.
* .show             Output list of Categories already assigned to the Profile.
  .s
* .available        Output list of available Categories in the db, with
  .a                the index for each.
* .create CATEGORY  Create category with input name. This separate command
  .c CATEGORY       prevents accidentally creating new category names when
                    assigning.
* .open             Open URL for Profile in system's default browser.
  .o                This can be useful to see the profile's visual content.
* (empty line)      Skip to next Profile.
* .quit             Skip all remaining Profiles and exit.
  .q
"""
    print("Interactive bulk Profile Category updater")
    print("=========================================")
    print(instructions)

    total = profiles.count()
    for i, profileRec in enumerate(profiles):
        print("Profile {current} of {total}".format(
            current=i + 1,
            total=total
        ))
        print("-----------------------------")
        profileRec.prettyPrint()

        while True:
            userInput = input("\n@{0} /> ".format(profileRec.screenName))

            # Full stop is used as system command, even if the command
            # incorrect, such that .badcommand is not interpreted as a
            # campaign name.
            if not userInput.rstrip():
                break
            elif userInput[0] == ".":
                if userInput.lower() in (".h", ".help"):
                    print(instructions)
                elif userInput.lower() in (".s", ".show"):
                    profileCat = list(profileRec.categories)
                    print("Categories: {0:,d}".format(len(profileCat)))
                    for c in profileRec.categories:
                        print(" - {0}".format(c.name))
                elif userInput.lower() in (".a", ".available"):
                    printAvailableCategories()
                elif userInput.lower().startswith(".c"):
                    arguments = userInput.split(" ")
                    if len(arguments) == 2:
                        categoryName = arguments[1]
                        try:
                            db.Category(name=categoryName)
                        except DuplicateEntryError:
                            print("Category already exists: {0}"
                                  .format(categoryName))
                        else:
                            print("Created category: {0}".format(categoryName))
                            print("Note that the .available indexes may have"
                                  " shifted.")
                    else:
                        print("Invalid input for creating category.")
                elif userInput.lower() in (".o", ".open"):
                    print("Opening URL in browser...")
                    webbrowser.open(profileRec.getProfileUrl())
                elif userInput.lower() in (".q", ".quit"):
                    sys.exit(0)
                else:
                    print("That is not a valid command. Try .help")
            else:
                if userInput[0] == "-":
                    userInput = userInput[1:]
                    delete = True
                else:
                    delete = False

                if userInput.isdigit():
                    try:
                        categoryRec = db.Category.select()[int(userInput) - 1]
                    except IndexError:
                        print("That index is not valid. See .available then"
                              " try again.")
                        continue
                else:
                    try:
                        categoryRec = db.Category.byName(userInput)
                    except SQLObjectNotFound:
                        print("Category name not found in db. See .available"
                              " then try again.")
                        continue
                if delete:
                    # This fails silently if the link does not exist.
                    categoryRec.removeProfile(profileRec)
                    print("Deleted {screenName} from {category}".format(
                        screenName=profileRec.screenName,
                        category=categoryRec.name
                    ))
                else:
                    try:
                        categoryRec.addProfile(profileRec)
                    except DuplicateEntryError:
                        print("Link already exists.")
                    else:
                        print("Added {screenName} to {category}".format(
                            screenName=profileRec.screenName,
                            category=categoryRec.name
                        ))


def bulk(args):
    """
    Handle the bulk subcommand.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments.

    :return: None
    """
    orderDict = {
        'screen-name': 'screen_name ASC',
        'full-name': 'name ASC',
        'modified': 'modified DESC',
        'added': 'id DESC',
        'followers': 'followers_count DESC'
    }
    sortOrder = orderDict[args.order_by]

    if args.category:
        if args.category.isdigit():
            # Get one item but decrease index by 1 since the available list
            # starts at 1. Assume available list also uses sqlmeta default
            # ordering.
            categoryRec = db.Category.select()[int(args.category) - 1]
        else:
            try:
                categoryRec = db.Category.byName(args.category)
            except SQLObjectNotFound as e:
                raise type(e)("Filter can only be applied to existing"
                              " categories. Category not found: {0}"
                              .format(args.category))
        profileResults = categoryRec.profiles.orderBy(sortOrder)
    else:
        profileResults = db.Profile.select().orderBy(sortOrder)

    runBulkCategoryUpdater(profileResults)


def clean(args):
    """
    Handle the clean subcommand.

    :param args: Result of argparse.parse_args(), with attributes for the
        subcommand arguments.

    :return: None
    """
    if args.category_name.isdigit():
        categoryRec = db.Category.select()[int(args.category_name) - 1]
    else:
        categoryRec = db.Category.byName(args.category_name)

    count = categoryRec.profiles.count()

    questionValues = {
        'count': count,
        'plural': 's' if count != 1 else '',
        'name': categoryRec.name
    }

    if args.action == 'unlink':
        if count == 0:
            print('No profiles to unlink.')
        else:
            response = input(
                "Are you sure you want to unlink {count:,d} profile{plural}"
                " from Category `{name}`? [Y/N] /> ".format(**questionValues)
            )
            if response.lower() in ('y', 'yes'):
                for profRec in categoryRec.profiles:
                    profRec.removeCategory(categoryRec)
                print("Done.")
            else:
                print("Cancelled.")
    elif args.action == 'delete-profiles':
        if count == 0:
            print('No profiles to delete.')
        else:
            response = input(
                "Are you sure you want to delete {count:,d} profile{plural}"
                " in Category `{name}`? [Y/N] /> ".format(**questionValues)
            )
            if response.lower() in ('y', 'yes'):
                profIDList = [prof.id for prof in categoryRec.profiles][:2]
                db.Profile.deleteMany(
                    IN(db.Profile.q.id, profIDList)
                )
                print("Done.")
            else:
                print("Cancelled.")
    elif args.action == 'delete-category':
        response = input(
            "Are you sure you want to delete Category `{name}`, which "
            " has {count:,d} profile{plural} assigned to it? [Y/N] /> "
            .format(**questionValues)
        )
        if response.lower() in ('y', 'yes'):
            categoryRec.destroySelf()
            print("Done.")
        else:
            print("Cancelled.")


def main():
    """
    Handle command-line arguments to print or edit data.

    Subparsing style is based on the examples in the argparse documentation.
    """
    parser = argparse.ArgumentParser(description="Category manager utility.")

    subParser = parser.add_subparsers(help="Available subcommands. Use --help"
                                           " after one for more info.")

    viewSubparser = subParser.add_parser(
        "view",
        help="Print existing data to stdout."
    )
    viewSubparser.add_argument(
        '-a', '--available',
        action='store_true',
        help="Output available Categories in db, with Profile counts for each."
    )
    viewSubparser.add_argument(
        '-p', '--profiles',
        action='store_true',
        help="Output local Profiles grouped by Category."
    )
    # TODO: Improve this to be more useful, as the expected behavior is for all
    # fetchProfile records to get one or two categories when created.
    viewSubparser.add_argument(
        '-u', '--unassigned',
        action='store_true',
        help="""Output list of Profiles which do not yet have a Category
             assigned to them."""
    )
    viewSubparser.set_defaults(func=view)

    addSubparser = subParser.add_parser(
        "add",
        help="""Assign Categories to specified Profiles, or just create
            a Category."""
    )
    addSubparser.add_argument(
        'category',
        metavar='CATEGORY',
        help="""Category name. Create input category, if it does not exist yet.
            If combined with --names argument, CATEGORY can be a row index
            of existing Category as in `view --available` list."""
    )
    addSubparser.add_argument(
        '-n', '--names',
        metavar='SCREEN_NAME',
        nargs='+',
        help="""Optional list of one or more screen names (without leading
            @ sign) of users in the db. Assign the input CATEGORY value to
            these screen names."""
    )
    addSubparser.set_defaults(func=add)

    bulkSubparser = subParser.add_parser(
        "bulk",
        help="""Enter interactive command-line tool to iterate through Profiles
            and assign Categories to each by hand."""
    )
    bulkSubparser.add_argument(
        '-c', '--category',
        help="""Filter all Profiles to those which already have the CATEGORY
            value set as on their Categories. This is useful to focus on a
            subset of Profiles which need more specific Categories assigned. If
            not set, iterate through all Profiles."""
    )
    bulkSubparser.add_argument(
        '--order-by',
        choices=['screen-name', 'full-name', 'modified', 'added', 'followers'],
        default='screen-name',
        help="""Set the ordering for Profiles to be returned. Defaults to
            screen name if not set."""
    )
    bulkSubparser.set_defaults(func=bulk)

    cleanSubparser = subParser.add_parser(
        "clean",
        help="Remove unneeded data"
    )
    cleanSubparser.add_argument(
        metavar='CATEGORY',
        dest='category_name',
        help="""Category to affect, supplied as either name or an index from
            `view --available` list."""
    )
    cleanSubparser.add_argument(
        '--action',
        choices=['unlink', 'delete-category', 'delete-profiles'],
        default='unlink',
        help="""Unlink (default): remove all Profiles from Category but do not
            delete any Profiles or Category records. delete-category: Delete
            the Category itself (Profile records are not deleted).
            delete-profiles: Delete all the Profile records in the Category
            (the Category is not deleted)."""
    )
    cleanSubparser.set_defaults(func=clean)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
