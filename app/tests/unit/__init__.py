"""
Unit tests module.
"""
import os

# Set global flag which is used to ensure test config values are used. This
# must be set here since the connection.py module is used indirectly by other
# scripts so it is hard to pass a test flag to the config init.
os.environ["TEST_MODE"] = "1"
