# -*- coding: utf-8 -*-
"""
Test DB Query place library.
"""
from unittest import TestCase

from lib.db_query.place import pairs


class TestPlace(TestCase):

    def test_Pairs(self):
        pairs.getPairs([])
