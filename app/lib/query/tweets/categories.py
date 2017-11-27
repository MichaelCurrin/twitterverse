# -*- coding: utf-8 -*-
"""
Category queries application file.
"""
from lib import database as db


def printAvailableCategories():
    """
    Iterate through Categories in db to print out name and Profile count
    for each.

    @return: None
    """
    print "     Category                  | Profiles"
    print "-------------------------------+---------"
    categoryResult = db.Category.select()
    for i, v in enumerate(categoryResult):
        print u"{index:3d}. {category:25s} | {profCnt:7,d}".format(
            index=i + 1,
            category=v.name,
            profCnt=v.profiles.count()
        )
    print


def printCategoriesAndProfiles():
    """
    Iterate through Categories in db to print out the name and list of
    the Profiles in each.

    @return: None
    """
    for i, cat in enumerate(db.Category.select()):
        profiles = list(cat.profiles.orderBy('screen_name'))
        print u"{index:d}. {name:15s} {profCnt:,d} profiles".format(
            index=i + 1,
            name=cat.name,
            profCnt=len(profiles)
        )
        for p in profiles:
            print u"   - @{screenName:20} | {name}".format(
                screenName=p.screenName,
                name=p.name
            )
        print


if __name__ == '__main__':
    print "Available cateogries"
    print "===================="
    printAvailableCategories()
    print
    print "Profiles"
    print "========"
    printCategoriesAndProfiles()
