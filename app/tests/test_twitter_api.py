# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.twitter_api import authentication


class TestAuth(TestCase):

    def test_getAPIConnection(self):
        api = authentication.getAPIConnection(userFlow=False)

    def test_getAppOnlyConnection(self):
        api = authentication.getAppOnlyConnection()
