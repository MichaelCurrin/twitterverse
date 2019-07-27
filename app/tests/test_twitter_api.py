# -*- coding: utf-8 -*-
from unittest import TestCase

import lib.twitter_api.auth


class TestAuth(TestCase):

    def test_getAPIConnection(self):
        api = lib.twitter_api.auth.getAPIConnection(userFlow=False)


    def test_getAppOnlyConnection(self):
        api = lib.twitter_api.auth.getAppOnlyConnection()
