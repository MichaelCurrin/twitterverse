# -*- coding: utf-8 -*-
"""
Test DB Query place library.
"""
from unittest import TestCase

from lib.db_query.place import pairs


class TestPlace(TestCase):

    def test_Pairs(self):
        # TODO: This would be better a functional test that depends on
        # existance of tables. Also, there is currently no output to validate.
        pairs.getPairs([])
