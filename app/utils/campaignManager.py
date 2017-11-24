#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Category manager utility.

Manage values in the Category table and manage links between Category
and Profiles.
"""
import argparse
import os
import sys
# Allow imports to be done when executing this file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.path.pardir)))

from lib import database as db
from lib.tweets import assignTweetCampaign
from lib.query.tweets.campaigns import printAvailableCampaigns,\
                                       printCampaignsAndTweets
