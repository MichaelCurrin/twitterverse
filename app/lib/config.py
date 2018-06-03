# -*- coding: utf-8 -*-
"""
Application configuration file.

Usage:
    $ python -m lib.config

    >>> from lib.config import AppConf
    >>> appConf = AppConf()
"""
import os
from ConfigParser import SafeConfigParser


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

    def getAppDir(self):
        """
        Return app directory.
        """
        return self.appDir


def sample():
    """
    Check that we are able to get values out the configuration files
    correctly.
    """
    conf = AppConf()
    print 'Consumer Key: {}'.format(conf.get('TwitterAuth', 'consumerKey'))
    print 'Consumer Secret: {}'.format(conf.get('TwitterAuth',
                                                'consumerSecret'))
    print 'Access Key: {}'.format(conf.get('TwitterAuth', 'accessKey'))
    print 'Access Secret: {}'.format(conf.get('TwitterAuth', 'accessSecret'))
    print
    print 'Location JSON: {}'.format(conf.get('Data', 'locations'))
    print 'Database path: {}'.format(conf.get('SQL', 'dbPath'))
    print


if __name__ == '__main__':
    sample()
