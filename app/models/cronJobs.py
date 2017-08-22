# -*- coding: utf-8 -*-
"""
SQL database tables relating to cron jobs.

The last run time is updated for a job when it is completed successfully.
A job item should only be required to run once a day.

If a job item is attempted but the procedure finds that the job item was
completed between start of the day and the current time then the job should be
skipped. This is useful say if the update procedure crashes halfway through
the jobs and is restarted, then it doesn't re-process the first half.
"""
# Names of tables to be included in the db. The order for when they are created
# matters.
__all__ = ['PlaceJob']

import sqlobject as so

from connection import conn


class PlaceJob(so.SQLObject):
    """
    Database table describing which places we want to get trends for on
    a regular basis and when the last time the job was run.

    The WOEID of a place is used to look up trends at the location.

    A place can appear only once in the table. Only towns or countries can be
    added to the job list, due to how Twitter API works - this is enforced
    when a record is created.

    The table starts off empty and desired places can be added or removed
    depending on admin user's preferences.

    An item can be marked as inactive, so that it will be skipped by a
    procedure but kept in the table so it can be made active again easily.
    """
    class sqlmeta:
        # Show with items with oldest last run dates first.
        defaultOrder = 'lastCompleted'
    _connection = conn

    # Create a reference to Place table. Place IDs cannot be repeated in
    # this job table.
    place = so.ForeignKey('Place', unique=True)
    # Create an index on place.
    placeIdx = so.DatabaseIndex(place)

    # Date and time when record was created.
    created = so.DateTimeCol(default=so.DateTimeCol.now)

    # When the job was last attempted regardless of outcome.
    lastAttempted = so.DateTimeCol(default=None)

    # When the job item was last completed successfully. Defaults to null.
    lastCompleted = so.DateTimeCol(default=None)
    # Create an index on last completed.
    lastCompletedIdx = so.DatabaseIndex(lastCompleted)

    # Boolean flag for whether the job item is enabled or should be skipped.
    enabled = so.BoolCol(notNull=True, default=True)

    def start(self):
        """
        Use this function to update the last attempted time.
        """
        self._set_lastAttempted(so.DateTimeCol.now())

    def end(self):
        """
        Use this function to update the last run time, if successful.
        """
        self._set_lastCompleted(so.DateTimeCol.now())

    def enable(self):
        """
        Set the job to enabled.
        """
        self.enabled = True

    def disable(self):
        """
        Set the job to disabled.
        """
        self.enabled = False
