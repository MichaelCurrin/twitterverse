# -*- coding: utf-8 -*-
from unittest import TestCase

from lib.config import AppConf


class TestConfig(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__(*args, **kwargs)
        self.conf = AppConf()

    def test_check_paths(self):
        self.conf.check_paths()

    def test_app_dir(self):
        self.conf.getAppDir()

    def test_staging_dir(self):
        self.conf.stagingCSVs()

    def test_read_values(self):
        """
        Do no validation, just check the section and field can be read.
        """
        self.conf.get('TwitterAuth', 'consumerKey')
        self.conf.get('TwitterAuth', 'consumerSecret')

        self.conf.get('TwitterAuth', 'accessKey')
        self.conf.get('TwitterAuth', 'accessSecret')
