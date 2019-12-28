#!/usr/bin/env python
"""
Twitter API test module.

Local test to check that Twitter credentials are valid connect to Twitter
API and that the auth functions can be used to do this.
"""
from __future__ import absolute_import
import os
import sys
import unittest
from unittest import TestCase

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.path.pardir, os.path.pardir)
))


from lib.twitter_api import authentication


class TestAuth(TestCase):

    def test_generateAppAccessToken(self):
        auth = authentication._generateAppAccessToken()

    def test_getTweepyConnection(self):
        auth = authentication._generateAppAccessToken()
        api = authentication._getTweepyConnection(auth)

    def test_getAPIConnection(self):
        """
        Test that App Access token can be used to connect to Twitter API.
        """
        api = authentication.getAPIConnection(userFlow=False)

    def test_getAppOnlyConnection(self):
        """
        Test App-only token.
        """
        api = authentication.getAppOnlyConnection()


if __name__ == '__main__':
    unittest.main()
