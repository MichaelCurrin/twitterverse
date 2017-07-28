# -*- coding: utf-8 -*-
"""
Setup connection to database.
"""
import os

from sqlobject.sqlite import builder

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import sys
    p = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     os.path.pardir))

    sys.path.insert(0, p)
from lib.config import AppConf


def setupConnection():
    dbPath = AppConf().getDBPath()

    # Create connection to database to be shared by table classes. The file
    # will be created if it does not exist.
    conn = builder()(dbPath)

    return conn


conn = setupConnection()
