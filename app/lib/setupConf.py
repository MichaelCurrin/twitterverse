# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser


# Make app configuration file available.
conf = SafeConfigParser()
conf.read(['etc/app.conf', 'etc/app.local.conf'])


def _test():
    """
    Check that we are able to get values out the configuration files
    correctly.

    Usage:
        1. cd to the package root.
        2. $ python lib/__init__.py
    """
    print 'Consumer Key: {}'.format(conf.get('TwitterAuth', 'consumerKey'))
    print 'Consumer Secret: {}'.format(conf.get('TwitterAuth', 'consumerSecret'))
    print 'Access Key: {}'.format(conf.get('TwitterAuth', 'accessKey'))
    print 'Access Secret: {}'.format(conf.get('TwitterAuth', 'accessSecret'))
    print
    print 'Location JSON: {}'.format(conf.get('Data', 'locations'))
    print 'Database name: {}'.format(conf.get('SQL', 'dbName'))
    print

if __name__ == '__main__':
    _test()
