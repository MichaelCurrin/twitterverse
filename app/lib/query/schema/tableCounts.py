#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Database stats report for all the tables and row counts.

Usage:
    $ python -m lib.query.schema.tableCounts
    # => print results to console.
"""
from sqlobject.dberrors import OperationalError

import models


def showTableCounts():
    """
    Print a table of db table names and row counts, separated by a pipe symbol.
    The column widths are adjusted to accommodate the widest strings.
    """
    summaryData = []
    nameWidth = 1
    countWidth = 1

    for tableName in models.__all__:
        tableClass = getattr(models, tableName)
        try:
            count = tableClass.select().count()
        except OperationalError:
            count = 'table missing!'
        summaryData.append((tableName, count))

        if len(tableName) > nameWidth:
            nameWidth = len(tableName)
        # Error text does not count towards line width.
        if isinstance(count, int) and len(str(count)) > countWidth:
            countWidth = len(str(count))

    template = '{0:%s} | {1:>%s}' % (nameWidth, countWidth)

    print "Table           | Rows"
    print "================|==============="
    for row in summaryData:
        print template.format(*row)
    print


if __name__ == '__main__':
    showTableCounts()
