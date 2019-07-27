# -*- coding: utf-8 -*-
"""
File handling library module.
"""
import os


def check_readable(path):
    """
    Raise assertion error if the given path is not readable.
    """
    assert os.access(path, os.R_OK), "Unable to read from: {}".format(path)


def check_writable(path):
    """
    Raise assertion error if the given path is not writable.
    """
    assert os.access(path, os.W_OK),  "Unable to write to: {}".format(path)

