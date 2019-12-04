# -*- coding: utf-8 -*-
"""
Database tests.
"""
from __future__ import unicode_literals
from __future__ import absolute_import
from unittest import TestCase

from lib import database
from models.trends import Trend


class TestDatabaseSetup(TestCase):
    """
    Test the database library module.
    """

    def tearDown(self):
        database._dropTables(verbose=False)

    def test_drop(self):
        database._dropTables()

    def test_create(self):
        database._createTables()

    def test_baseLabels(self):
        database._createTables(verbose=False)
        database._baseLabels()

    def test_populate(self):
        database._createTables(verbose=False)

        limit = 1
        database._populate(limit)


class TestModel(TestCase):
    """
    Test ORM operations on the SQL database.

    In particular, edgecases such as unicode character handling.
    """

    def tearDown(self):
        database._dropTables(verbose=False)

    def test_insert(self):
        database._dropTables(verbose=False)
        database._createTables(verbose=False)
        database._baseLabels()

        t = Trend(topic="abc", volume=1)
        self.assertEqual(t.topic, "abc")
        self.assertEqual(t.volume, 1)

        t = Trend(topic="a b Ç 😊", volume=1000)
        self.assertEqual(t.topic, "a b Ç 😊")

        database._dropTables(verbose=False)
