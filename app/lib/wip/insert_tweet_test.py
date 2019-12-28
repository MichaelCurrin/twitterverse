"""
This is an incomplete file used for testing.
"""
from __future__ import absolute_import
from __future__ import print_function
import json

from .test import _readJSON


tweetData = _readJSON('var/tweet_test.json')

t = tweetData[0]

print(json.dumps(t, indent=4))

