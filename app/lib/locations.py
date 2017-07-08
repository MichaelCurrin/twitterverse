# -*- coding: utf-8 -*-
"""
Read in the location data which has been read from Twitter API and stored
locally as JSON.
"""
import json
import os
import sys

# Allow imports from lib.
sys.path.insert(0, os.path.abspath('.'))
from lib import conf


def readLocations():
    """
    Read in location data fron a configured JSON file.
    
    Attempts to get from variable file if it exists and has data, otherwise 
    reads from the static sample file which is versioned.

    Returns the list data as a generator.
    """
    path = conf.get('Data', 'locations')
    if not (os.path.exists(livePath) and os.path.getsize(livePath)):
        path = conf.get('Data', 'locationsSample')

    with open(path, 'r') as reader:
        locationsData = json.load(reader)
    
    for location in locationsData:
        yield location


def test():
    # Convert generator of locations to list and then print neatly.
    data = list(readLocations())
    print json.dumps(data, indent=4)


if __name__ == '__main__':
    test()
