#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Database stats report for a preview of the row counts of each table.

Usage:
    $ python preview.py
    # => print results to console.
"""
import os
import sys
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                                      os.pardir))
# Make dirs in app dir importable.
if appDir not in sys.path:
    sys.path.insert(0, appDir)

import models


def showTableRecords(maxResults=10):
    print 'Results preview\n'.format(maxResults)
    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        results = tableClass.select()
        limitedResults = results.limit(maxResults)

        heading = '{0} ({1})'.format(tableName, results.count())
        print heading
        print '-'*len(heading)
        for r in limitedResults:
            print r
        print
        print limitedResults
        print
        print


def main(args):
    if args:
        showTableRecords(int(args[0]))
    else:
        showTableRecords()


if __name__ == '__main__':
    main(sys.argv[1:])
