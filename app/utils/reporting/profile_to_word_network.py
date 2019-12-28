#!/usr/bin/env python
"""
Profile to terms network utility.

Create output for a CSV file as four columns. Maps Twitter users in the
db to terms which they used. This can be used to create a network graph.
See also the app/lib/query/tweets/top_words.py file, which has summary data.

Iterate through Profile records and their tweets to create output as screen
name and term, with a term type as a dimension for filtering and frequency
integer for filtering, sorting or applying a weighting.
"""
from __future__ import absolute_import
from __future__ import print_function
import argparse
import re
import os
import sys
from collections import Counter

# Allow imports to be done when executing this file directly.
appDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      os.path.pardir, os.path.pardir))
sys.path.insert(0, appDir)

from lib import database as db


def main():
    """
    Command-line to generate output data or show a help message.
    """
    columns = u'"Screen Name",Type,Term,Frequency'

    description = u"""Create network mapping profiles to words. Prints
comma-separated values to stdout, which can be redirected to a CSV file.
Header: {columns}""".format(columns=columns)

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.parse_args()

    print(columns)

    pattern = re.compile(r"[^#@\w'-]+")

    # TODO: Consider if there is a way to do this quicker without using
    # the ORM. Such as with some array and distinct funtions in SQL.
    for prof in db.Profile.select():
        # Place all the terms for the current profile in here, with frequency.
        profileTerms = Counter()

        for t in prof.tweets:
            words = pattern.split(t.message)
            for word in words:
                # Filter on mentions and hashtags until stopwords and case can
                # be handled on plain words.
                if word.startswith(u'@') or word.startswith(u'#'):
                    profileTerms.update({word: 1})

        for term, freq in profileTerms.items():
            if term.startswith(u'@'):
                termType = u'mention'
            elif term.startswith('#'):
                termType = u'hashtag'
            else:
                continue
                # For testing now, skip printing term which is generic.
                termType = u'other'

            # It is safest to quote terms, as they may have single quotes
            # which could be misread when opened as a CSV.
            # TODO: Write using csv module instead to handle tweets with
            # quotes, or replace here with single quotes.
            term = term.replace('"', "'")
            print(u'@{screenName},{termType},"{term}",{freq}'.format(
                screenName=prof.screenName,
                termType=termType,
                term=term,
                freq=freq
            ))


if __name__ == '__main__':
    main()
