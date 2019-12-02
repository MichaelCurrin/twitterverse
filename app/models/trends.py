# -*- coding: utf-8 -*-
"""
Trends model application file.

SQL database tables relating to trends.

This script cannot be run directly, since on an import it finds Trend
is in the models namespace already and on filename execution the config
file cannot be accessed without app dir in the path variable.
"""
from __future__ import absolute_import
from __future__ import print_function
__all__ = ['Trend']

import sqlobject as so

from .connection import conn
from .places import Place


class Trend(so.SQLObject):
    """
    A trending topic on Twitter, meaning a lot of Twitter accounts were talking
    about that topic.

    A topic exists at a point in time and maps to a specific place. It's term
    can either be a hashtag (starts with '#' and has no spaces) or a keyword
    phrase (no '#' and can have multiple words).

    Note that the topic is not unique, since the topic can be repeated in
    many locations and it can be repeated in one location across time.

    The topic has a trending volume figure, which is how many tweets there are
    about the topic in the past 24 hours (according to Twitter API docs).
    Adding up trends for a Place taken at the SAME time each day should give
    an accurate total of tweets for the period, since there should not be any
    overlap in tweets across two consecutive 24-hour periods. One might use
    the earliest record available for the day, assuming the cron job
    runs soon after midnight, so that any ad hoc data will not skew the
    results. However, the value will for the 24 hours of the PREVIOUS day.

    Note that the topic volume shown is always GLOBAL total volume i.e.
    independent of the location used to look up the topic. Volume usually
    ranges from around 10,000 to 1 million and smaller values are returned
    as null by Twitter API.

    However, it is still useful to count the number of places which a tppic
    is trending in as an indication of how widespread it is.
    """

    class sqlmeta:
        # Set sort order by most recently added records first.
        defaultOrder = '-timestamp'

    _connection = conn

    # The topic which is trending.
    topic = so.StringCol(length=64)
    topicIdx = so.DatabaseIndex(topic)

    # Whether the topic is a hashtag i.e. starts with '#'.
    hashtag = so.BoolCol(default=False)

    # Number of global tweets about topic in past 24 hours. Null values
    # are allowed, but not default is set.
    volume = so.IntCol(notNull=False)

    # The place associated with this trend record. See `setPlace` for why
    # this is an optional field.
    place = so.ForeignKey("Place", notNull=False, default=None)
    placeIdx = so.DatabaseIndex(place)

    # Date and time when record was created.
    timestamp = so.DateTimeCol(default=so.DateTimeCol.now)
    timestampIdx = so.DatabaseIndex(timestamp)

    def setPlace(self, woeid):
        """
        Link an existing Trend and Place records, given a Place WOEID.

        Expects a WOEID int, gets ID for the Place, then stores it as the
        foreign key for the Trend.

        This doesn't work to be placed in __init__ since then its called
        on a select and doen't work for modelCreate because the input kwargs
        are validated before the method is called.

        :param woeid: integer value for WOEID of the Place to link to.

        :return self: returns object instance.
        """
        assert isinstance(woeid, int), 'Expected WOEID as an `int`, but '\
            'got type `{0}`.'.format(type(woeid).__name__)
        try:
            # TODO: Is this the same as self.place?
            self.placeID = Place.byWoeid(woeid).id
        except so.SQLObjectNotFound as e:
            raise type(e)('Place with WOEID {0} could not be found in the db.'
                          .format(woeid))

        return self

    def _set_topic(self, value):
        """
        Override the topic setting method, so that hashtag boolean is updated
        automatically whenever topic is set.

        :param value: string value to set as the topic.
        """
        self._SO_set_topic(value)
        if value.startswith('#'):
            self._SO_set_hashtag(True)
        else:
            self._SO_set_hashtag(False)

    @classmethod
    def getColumnNames(cls):
        """
        Return a list of column names for the class, as strings. This is
        created from a dictionary, so the order is not guaranteed.
        """
        return list(cls.sqlmeta.columns.keys())

    def getData(self, quiet=True):
        """
        Output the current record with key:value pairs for column name
        and value. Note that this is not suitable to converted to JSON
        because of the data types of values.
        """
        data = {col: getattr(self, col) for col in self.getColumnNames()}

        if not quiet:
            for k, v in data.items():
                # Align key to the right.
                print(u'{0:>15} : {1}'.format(k, v))
