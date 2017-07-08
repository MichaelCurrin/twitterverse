# -*- coding: utf-8 -*-
"""
Setup connection to database.
"""
__all__ = 'conn'

import os
import sys

from sqlobject.sqlite import builder

# Allow imports from lib.
sys.path.insert(0, os.path.abspath('.'))
from lib import conf


dbName = conf.get('SQL', 'dbName')

# Create connection to database to be shared by table classes.
conn = builder()(dbName)
