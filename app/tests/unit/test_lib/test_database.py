# -*- coding: utf-8 -*-
"""
Test database library.

TODO Add database creation as setup for entire unit tests and tear down
to remove it.
"""
from __future__ import absolute_import
from unittest import TestCase

import models
from lib import database


class TestDatabase(TestCase):

    def test_modelList(self):
        modelCount = len(models.__all__)
        self.assertEqual(modelCount, 13)

    def test_modelClasses(self):
        classes = database._getModelClasses()
        self.assertEqual(len(classes), 13)
