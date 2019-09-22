# -*- coding: utf-8 -*-
"""
Test database library.
"""
from unittest import TestCase

from lib import database


class TestDatabase(TestCase):

    def test_Main(self):
        database.main([])
