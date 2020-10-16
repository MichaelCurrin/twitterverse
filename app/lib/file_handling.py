"""
File handling library module.
"""
import csv
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
    assert os.access(path, os.W_OK), "Unable to write to: {}".format(path)


def read_csv(path):
    """
    Return dict rows of a CSV, line by line.
    """
    with open(path, "U") as fIn:
        reader = csv.DictReader(fIn)
        for row in reader:
            yield row
