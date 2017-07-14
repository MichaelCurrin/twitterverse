# -*- coding: utf-8 -*-
import json

from test import _writeJSON, _readJSON


tweetData = _readJSON('var/tweet_test.json')

t = tweetData[0]

print json.dumps(t, indent=4)

