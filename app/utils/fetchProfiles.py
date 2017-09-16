#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Fetch Profiles utility.
"""
import os
import sys

# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))
from lib.tweets import insertOrUpdateProfileBatch


def main(args):
    """
    Add or update Profile table with screen names.

    Expects a list screen names, either from arguments list or to be read
    from a specified text file.

    @param args: command-line arguments as a list of strings. See
        the usage help message below.

    @return: None
    """
    # Look for the preview flag and remove it if found, so that other
    # flags will moved to the start and so that the preview flag is not part of
    # the arguments list. If we have no args left after popping preview flag,
    # then the help message will be shown.
    for i in range(len(args)):
        if args[i] in ('-p', '--preview'):
            args.pop(i)
            preview = True
            break
    else:
        # Flag was not found. Use default behaviour.
        preview = False

    if not args or set(args) & set(('-h', '--help')):
        print """\
Usage:
$ ./utils/fetchProfiles.py [-p|--preview] [-f|--file FILEPATH]
    [-l|--list SCREEN_NAME, ...] [-h|--help]

Options and arguments:
--help     : Show this help output.
--preview  : If this flag is set anywhere in the args list, then no data
             is fetched from the API and just the screen names received
             are printed to stdout (either from file or list method).
--file     : Read in the following argument as FILEPATH argument. Cannot
             be used with the --list flag.
FILEPATH   : Path to a text file, which has one screen name per row and
             no header or other data. Use to lookup profiles from Twitter API
             and then add/update a record in the Profile table.
--list     : Read in the following arguments as SCREEN_NAME list.
             Cannot be used with the --file flag.
SCREEN_NAME: A list of Twitter screen names as command-line arguments.
             Use to lookup profiles from Twitter API and then add/update
             a record in the Profile table.

Note that looking up a screen name is not case sensitive, based on testing
the Twitter API.
"""
    else:
        if args[0] in ('-f', '--file'):
            assert len(args) == 2, ('Specify exactly one filename after the'
                                    ' --file flag.')
            filename = args[1]

            assert os.access(filename, os.R_OK), 'Unable to read path `{0}`'\
                                                 .format(filename)
            with open(filename, 'rb') as reader:
                screenNames = reader.read().splitlines()

        elif args[0] in ('-l', '--list'):
            screenNames = args[1:]
            assert screenNames, ('Specify one or more screen names after the'
                                 ' --list flag.')
        else:
            raise ValueError('Invalid arguments. Use the --help flag.')

        if preview:
            for i, v in enumerate(screenNames):
                print '{0:3d}. {1:s}'.format(i + 1, v)
        else:
            insertOrUpdateProfileBatch(screenNames)


if __name__ == '__main__':
    main(sys.argv[1:])