# -*- coding: utf-8 -*-
"""
Initialisation file for extract library directory.

This library handles extracting data from the Twitter API and outputting
to a staging area as a CSV, so that it can be transformed and then loaded into
the DB later.

If extract and load steps happened in one command, then an error on writing
to the db would mean losing fetched tweets in memory, making it hard to
inspect the data and rebuild the SQL. Therefore, data is written out to a CSV
with minimal processing. Note that writing out data is slow, therefore we
write out rows in a single write action for a batch of objects provided.
"""
