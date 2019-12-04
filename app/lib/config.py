# -*- coding: utf-8 -*-
"""
Application configuration file.

Usage:
    >>> from lib.config import AppConf
    >>> conf = AppConf()
"""
from __future__ import absolute_import
import glob
import os
from six.moves.configparser import ConfigParser

import lib.file_handling


class AppConf(ConfigParser):
    """
    Make app configuration filenames absolute paths and relative to app config
    dir. Then configure the conf object with data.

    The local app conf file is optional and in values in it will overwrite
    those set in the main app conf file.
    """

    def __init__(self, test=False):
        """
        Initiate instance of AppConf class.

        :param test: Set to True to use test config and not local config file.
            Alternatively set TEST_MODE as a non-empty environment variable.
        """
        ConfigParser.__init__(self)

        test_mode = os.environ.get('TEST_MODE', None)

        self.appDir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir)
        )

        confNames = [
            'app.conf',
            'app.test.conf' if test or test_mode else 'app.local.conf'
        ]
        confPaths = [os.path.join(self.appDir, 'etc', c) for c in confNames]
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

    @property
    def dbPath(self):
        return self.get('SQL', 'dbPath')

    def stagingCSVs(self, prefix=""):
        """
        Get paths of all CSVs in configured staging dir.

        CSVs should have a naming convention, to prefix parameter filters for
        example to all the CSVs with prefix "search".

        Glob does no ordering so we make it alphabetical.
        """
        csvDir = self.get('Staging', 'stagingDir')
        filePattern = "{}*.csv".format(prefix)
        pattern = os.path.join(csvDir, filePattern)
        paths = glob.glob(pattern)

        return sorted(paths)

    def getAuthConsumerFields(self):
        """
        Return configured Twitter auth consumer fields pair.

        Required for auth flows:
        - App-only
        - App Access
        - User Access
        """
        consumer_key = self.get('TwitterAuth', 'consumerKey')
        consumer_secret = self.get('TwitterAuth', 'consumerSecret')
        assert consumer_key != 'YOUR_CONSUMER_KEY', (
            "Consumer fields still has the default values."
            " Update app.local.conf then try again."
        )
        assert consumer_key and consumer_secret, (
            "Consumer fields cannot be empty. Update app.local.conf"
            " then try again."
        )

        return consumer_key, consumer_secret

    def getAuthAccessFields(self):
        """
        Return configured Twitter auth access fields pair.

        Required for auth flows:
        - App Access
        - User Access
        """
        access_key = self.get('TwitterAuth', 'accessKey')
        access_secret = self.get('TwitterAuth', 'accessSecret')

        assert access_key and access_secret, (
            "Access fields cannot be empty. Update app.local.conf then"
            " try again."
        )

        return access_key, access_secret
