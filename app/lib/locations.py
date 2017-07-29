# -*- coding: utf-8 -*-
"""
Read in the location data which has been read from Twitter API and stored
locally as JSON.

The data is not likely to change much, so the locations JSON file can be used
to build Place records in the database without reading the Twitter API.
This could be improved at a later stage to always use Twitter or to be
configurable.
"""
import json
import os

from lib.config import AppConf

appConf = AppConf()


def getJSON():
    """
    Read in location data fron a configured JSON file.

    Attempts to get from variable file if it exists and has data, otherwise
    reads from the static sample file which is versioned.

    Returns the list data as a generator.
    """
    path = appConf.get('Data', 'locations')
    if not (os.path.exists(path) and os.path.getsize(path)):
        path = appConf.get('Data', 'locationsSample')

    with open(path, 'r') as reader:
        locationsData = json.load(reader)

    for location in locationsData:
        yield location


def _test():
    # Convert generator of locations to list and then print neatly.
    data = list(getJSON())
    print json.dumps(data, indent=4)


if __name__ == '__main__':
    _test()
