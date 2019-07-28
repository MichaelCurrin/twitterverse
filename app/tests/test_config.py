# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.config import AppConf


class TestConfig(TestCase):

    def test_AppConf(self):
        conf = AppConf()
