# -*- coding: utf-8 -*-
"""
Setup connection to database.

To execute this file directly but still enable imports from app dir:
    $ cd app
    $ python -m lib.connection
"""
from sqlobject.sqlite import builder

from lib.config import AppConf


def setupConnection():
    dbPath = AppConf().getDBPath()

    # Create connection to database to be shared by table classes. The file
    # will be created if it does not exist.
    conn = builder()(dbPath)

    return conn


conn = setupConnection()
