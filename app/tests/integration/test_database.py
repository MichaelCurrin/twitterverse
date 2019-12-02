from unittest import TestCase

from lib import database


class TestDatabaseSetup(TestCase):

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
