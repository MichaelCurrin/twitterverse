# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from unittest import TestCase

from lib.config import AppConf


class TestConfig(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__(*args, **kwargs)
        self.conf = AppConf()

    def test_test_mode(self):
        self.assertTrue(os.environ.get('TEST_MODE'))

        db_path = self.conf.get('SQL', 'dbPath')
        self.assertTrue(db_path.endswith('test_db.sqlite'))

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
