#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Database stats report for all the tables and row counts.

Usage:
    $ python -m lib.query.schema.tableCounts
    # => print results to console.
"""
import models


def showTableCounts():
    """
    Print a table of db table names and row counts, separated by a pipe symbol.
    The column widths are adjusted to accomodate the widest strings.
    """
    summaryData = []
    nameWidth = 1
    countWidth = 1

    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        count = tableClass.select().count()
        summaryData.append((tableName, count))

        if len(tableName) > nameWidth:
            nameWidth = len(tableName)
        if len(str(count)) > countWidth:
            countWidth = len(str(count))

    template = '{0:%ss} | {1:%sd}' % (nameWidth, countWidth)

    print 'Table     | Rows'
    print '==========|====='
    for row in summaryData:
        print template.format(*row)
    print
    print


if __name__ == '__main__':
    showTableCounts()
