# -*- coding: utf-8 -*-
"""
Application configuration file.

Usage:
    >>> from lib.config import AppConf
    >>> conf = AppConf()
"""
import glob
import os
from ConfigParser import SafeConfigParser

import lib.file_handling


class AppConf(SafeConfigParser):
    """
    Make app configuration filenames absolute paths and relative to app
    config dir. Then configure the conf object with data.

    The local app conf file is optional and in values in it will overwrite
    those set in the main app conf file.
    """

    def __init__(self):
        """
        Initiate instance of AppConf class.
        """
        SafeConfigParser.__init__(self)

        # Make absolute path to app dir available as attribute.
        self.appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   os.path.pardir))
        # Set absolute paths to configuration input files.
        confNames = ('app.conf', 'app.local.conf')
        confPaths = [os.path.join(self.appDir, 'etc', c) for c in confNames]

        # Parse the configuration files.
        self.read(confPaths)
        self.set('DEFAULT', 'appDir', self.appDir)

    def check_paths(self):
        """
        Check that configured paths are valid.

        Consider also:
            os.path.exists(path)
            os.path.getsize(path)
        """
        paths = [
            self.get('Data', 'locationsSample'),
        ]
        for path in paths:
            lib.file_handling.check_readable(path)

        # You get an error on checking write access for non-existent file.
        locations_dir = os.path.dirname(self.get('Data', 'locations'))
        paths = [
            self.get('SQL', 'dbDir'),
            self.get('Staging', 'stagingDir'),
            self.get('Scraper', 'outputDir'),
            locations_dir,
        ]
        for path in paths:
            lib.file_handling.check_writable(path)

    def getAppDir(self):
        """
        Return path to app directory.
        """
        return self.appDir

    def stagingCSVs(self, prefix=""):
        """
        Get paths of all CSVs in configured staging dir.

        CSVs should have a naming convention, to prefix parameter filters
        for example to all the CSVs with prefix "search".

        Glob does no ordering so we make it alphabetical.
        """
        csvDir = self.get('Staging', 'stagingDir')
        filePattern = "{}*.csv".format(prefix)
        pattern = os.path.join(csvDir, filePattern)
        paths = glob.glob(pattern)

        return sorted(paths)
