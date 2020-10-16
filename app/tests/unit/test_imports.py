"""
Test imports.

Check that imports from modules are valid, especially after refactoring
structure and renaming. This is useful before there is wide coverage from
other tests.

This will check for some syntax errors and not logic or runtime errors.
"""
from unittest import TestCase

# flake8: noqa


class TestEtc(TestCase):
    def test_base_data(self):
        import etc.__init__
        import etc.base_data


class TestLib(TestCase):
    def test_lib(self):

        import lib
        from lib.config import AppConf
        from lib import database as db
        import lib.file_handling
        import lib.jobs
        import lib.locations
        import lib.places
        import lib.text_handling
        import lib.trends
        import lib.tweets

    def test_db_query(self):
        import lib.db_query

        import lib.db_query.place
        import lib.db_query.place.country_report
        import lib.db_query.place.pairs
        import lib.db_query.place.tree

        import lib.db_query.schema
        import lib.db_query.schema.preview
        import lib.db_query.schema.table_counts

        import lib.db_query.search
        import lib.db_query.search.message
        import lib.db_query.search.topic

        import lib.db_query.tweets
        import lib.db_query.tweets.campaigns
        import lib.db_query.tweets.categories
        import lib.db_query.tweets.top_profiles
        import lib.db_query.tweets.top_tweets
        import lib.db_query.tweets.top_words

        import lib.db_query.do_query

    def test_extract(self):

        import lib.extract
        import lib.extract.csv_writer
        import lib.extract.search

    def test_twitter_api(self):

        import lib.twitter_api
        import lib.twitter_api.rates
        import lib.twitter_api.search
        import lib.twitter_api.streaming


class TestModels(TestCase):
    def test_init(self):
        import models.__init__
        import models.connection
        import models.cron_jobs
        import models.places
        import models.trends
        import models.tweets
