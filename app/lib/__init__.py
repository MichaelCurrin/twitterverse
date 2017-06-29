# -*- coding: utf-8 -*-
"""
Initialisation file for lib directory.
"""
from ConfigParser import SafeConfigParser


# Makes app configuration file available.
conf = SafeConfigParser()
conf.read(('etc/app.conf', 'etc/app.local.conf'))
