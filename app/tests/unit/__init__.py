"""
Unit tests module.
"""
from __future__ import absolute_import
import os

# Set global flag which is used to ensure test config values are used. This
# must set here since the connection.py module is used indirectly by other
# scripts so it is hard to pass a test flag to the config init.
os.environ['TEST_MODE'] = "1"
