# -*- coding: utf-8 -*-
"""
Twitter API test module.

Local test to check that Twitter credentials are valid connect to Twitter
API and that the auth functions can be used to do this.
s"""
from unittest import TestCase

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
