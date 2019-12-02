# -*- coding: utf-8 -*-
"""
Connection application file.

Setup a connection to the database.
"""
from __future__ import absolute_import
from sqlobject.sqlite import builder

from lib.config import AppConf


def setupConnection():
    """
    Create connection to configured SQLite database file.

    The file will be created if it does not exist yet.

    :return: DB connection object, which should be added SQLObject table
        classes so they can access the db.
    """
    dbPath = AppConf().get('SQL', 'dbPath')

    return builder()(dbPath)


conn = setupConnection()
