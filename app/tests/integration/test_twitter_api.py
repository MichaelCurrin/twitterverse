# -*- coding: utf-8 -*-
"""
Twitter API test module.
"""
from unittest import TestCase

from lib.twitter_api import authentication


class TestAuth(TestCase):

    def test_generateAppToken(self):
        auth = authentication._generateAppAccessToken()

    def test_getTweepyConnection(self):
        auth = authentication._generateAppAccessToken()
        api = authentication._getTweepyConnection(auth)

    def test_getAPIConnection(self):
        """
        Test App Access token.
        """
        api = authentication.getAPIConnection(userFlow=False)

    def test_getAppOnlyConnection(self):
        """
        Test App-only token.
        """
        api = authentication.getAppOnlyConnection()
