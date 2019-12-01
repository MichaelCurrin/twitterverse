# -*- coding: utf-8 -*-
"""
Test database library.
"""
from unittest import TestCase

from lib import database


class TestDatabase(TestCase):

    def test_main(self):
        """
        Test command-line entry point.
        """
        database.main([])
