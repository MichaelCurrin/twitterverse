# -*- coding: utf-8 -*-
"""
Cronjobs model application file.

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
    Listing of places which we want to regularly get trend data for.

    The WOEID of a place is used to look up trends at the location,
    for records which have status set to enabled. An item can be marked
    as disabled, so that it will be skipped by a procedure but kept in the
    table so it can be enabled again easily.

    A place can appear only once in the table. Only towns or countries can be
    added to the job list, due to how Twitter API works - this is enforced
    when a record is created.

    The table starts off empty and desired places can be added or removed
    depending on admin user's preferences.
    """

    class sqlmeta:
        # Order as enabled (True) items first, then by jobs with oldest
        # (or null) last completed timestamps first and then by oldest
        # (or null) last attempted timestamps. Therefore when running jobs, the
        # ones which have not been completed before or for the longest time
        # are given priority over ones which were recently completed.
        # And any disabled jobs will be at the bottom when viewing a report.
        defaultOrder = "enabled DESC, last_completed ASC, last_attempted ASC"

    _connection = conn

    # Create a reference to Place table. Place IDs cannot be repeated in
    # this job table.
    place = so.ForeignKey('Place', unique=True)
    # Create an index on place.
    placeIdx = so.DatabaseIndex(place)

    # Date and time when record was created.
    created = so.DateTimeCol(notNull=True, default=so.DateTimeCol.now)

    # When the job was last attempted regardless of outcome.
    lastAttempted = so.DateTimeCol(notNull=False, default=None)

    # When the job item was last completed successfully. Defaults to null.
    lastCompleted = so.DateTimeCol(notNull=False, default=None)
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

    def setEnabled(self):
        """
        Set the job to enabled.
        """
        self.enabled = True

    def setDisabled(self):
        """
        Set the job to disabled.
        """
        self.enabled = False

    def getStatus(self, asText=False):
        """
        Get the status from when the job was last run.

        If last attempted time is None, then return None since we cannot
        confirm success or failure.

        Return True for success, if last completed time is not None and
        is after last attempted time. Otherwise return False for failure.

        @param asText: Default False. If True, return status as human-readable
            string.

        @return status: job status as OK (True) or failed (False) or not
            run (None). Returned as human-readable string if asText is True.
        """
        if self.lastAttempted:
            if self.lastCompleted and self.lastCompleted > self.lastAttempted:
                status = "OK" if asText else True
            else:
                status = "failed" if asText else False
        else:
            status = "not run" if asText else None

        return status
