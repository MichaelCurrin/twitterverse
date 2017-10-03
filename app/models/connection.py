# -*- coding: utf-8 -*-
"""
Connection application file.

Setup a connection to the database.

Usage:
    $ python -m lib.connection
"""
from sqlobject.sqlite import builder

from lib.config import AppConf


def setupConnection():
    """
    Create connection to database, to be shared by table classes. The file
    will be created if it does not exist.
    """
    dbPath = AppConf().getDBPath()
    conn = builder()(dbPath)

    return conn


conn = setupConnection()
