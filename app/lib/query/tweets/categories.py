# -*- coding: utf-8 -*-
"""
Category queries application file.
"""
from lib import database as db


def printAvailableCategories():
    """
    Iterate through Categories in db and print out name and Profile count
    for each.
    """
    print "     Category                  | Profiles"
    print "-------------------------------+---------"
    catList = db.Category.select()
    for i, v in enumerate(catList):
        print u'{index:3d}. {cat:25s} | {profCnt:7,d}'.format(
            index=i + 1, cat=v.name, profCnt=v.profiles.count()
        )
    print


def printCategoriesAndProfiles():
    """
    Iterate through Categories in db and print out name and list of
    the Profiles in it.
    """
    for i, cat in enumerate(db.Category.select()):
        profiles = list(cat.profiles.orderBy('screen_name'))
        print u"{index:d}. {name} ({profCnt:,d})".format(index=i + 1,
                                                         name=cat.name,
                                                         profCnt=len(profiles))
        for p in profiles:
            print u" - @{screenName:20} {name}".format(screenName=p.screenName,
                                                       name=p.name)
        print
