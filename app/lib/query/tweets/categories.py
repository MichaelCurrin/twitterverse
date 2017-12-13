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


def printUnassignedProfiles():
    """
    Iterate through Profiles in db to print out those in no Categories.

    Output may be very long for large datasets of Profiles.

    TODO: Add filters such as top N recently created profiles or most
    followers. And find a way to make this more useful, considering that
    the influencer category and a specific influencer category could be assigned
    on fetchProfiles.py running, but it has to be clear that industry is
    assigned yet.

    @return: None
    """
    for profileRec in db.Profile.select(orderBy='screen_name'):
        if not profileRec.categories.count():
            print u"@{screenName} | {name} | {followers:,d} followers".format(
                screenName=profileRec.screenName,
                name=profileRec.name,
                followers=profileRec.followersCount
            )
            print profileRec.getFlatDescription()
            print


if __name__ == '__main__':
    print "Available cateogries"
    print "===================="
    printAvailableCategories()
    print
    print "Profiles"
    print "========"
    printCategoriesAndProfiles()
