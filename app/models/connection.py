# -*- coding: utf-8 -*-
"""
Setup connection to database.
"""
__all__ = 'conn'

from sqlobject.sqlite import builder

if __name__ == '__main__':
    # Allow imports of dirs in app, when executing this file directly.
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.curdir))
from lib import conf


dbName = conf.get('SQL', 'dbName')

# Create connection to database to be shared by table classes.
conn = builder()(dbName)
