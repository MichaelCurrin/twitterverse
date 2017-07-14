# -*- coding: utf-8 -*-
"""
This is an incomplete file used for testing.
"""
from lib.textHandling import stripSymbols
from test import _writeJSON, _readJSON

# Read in JSON data for testing, to save on API calls and waiting to load data.
tweetData = _readJSON('var/tweet_test.json')

wordsDict = {}

for t in tweetData:
    # Remove punctuation and symbols and replace white space chars with plain

    # space.
    wordsList = stripSymbols(t['text'], keepHash=True, keepAt=True)

    ## TODO - handle http instead of removing all punctuation from it.
    ## use regex to remove punctuation, unicode characters and make
    ## all white spaces plain spaces.
    ## Consider correct time to split before after regex.
    ## https://stackoverflow.com/questions/23122659/python-regex-replace-unicode
    for w in wordsList:
        newKey = w
        if newKey.lower() not in (u'and', u'not', u'or', u'in', u'') and \
                not newKey.lower().startswith('http'):
            if newKey.lower() not in [word.lower() for word in wordsDict]:
                # Add entry for the first time, using current item's case.
                wordsDict[newKey] = 1
            else:
                # Do we use case of current item or existing item in dictionary?
                for oldKey in wordsDict:
                    # Get the exiting key.
                    if newKey.lower() == oldKey.lower():
                        break
                # Test strings from left to right for difference in case.
                if newKey < oldKey:
                    # New key has a capital letter where old doesn't.
                    # So remove existing key and use it to value for new key.
                    value = wordsDict.pop(oldKey)
                    wordsDict[newKey] = value + 1
                else:
                    # Add to existing key's value.
                    wordsDict[oldKey] += 1

keys = wordsDict.keys()
keys.sort()
for x in keys:
    print x, wordsDict[x]
# Or use set() if counts do not matter.

# We can't easily get phrases from tweets to match up with trending topcs
# But we can search for presence of a topic in a user's tweets.
# after removing punctutation depending on rule for trending phrase?
# or do regex.

#print dir(set(wordsDict))
#['__and__', '__class__', '__cmp__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__iand__', '__init__', '__ior__', '__isub__', '__iter__', '__ixor__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__rand__', '__reduce__', '__reduce_ex__', '__repr__', '__ror__', '__rsub__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__xor__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'union', 'update']


# Compare tweet words against Trend db.

from lib import dbQueries
trendWords = dbQueries.getTrendsFromLocation()

# Common words (for case will be a problem)
tweetSet = set(wordsDict)
trendSet = set(trendWords)

print 'COMMON'
print set.intersection(tweetSet, trendSet)
print
print 'TWEET ONLY'
print tweetSet - trendSet
print
print 'TREND ONLY'
print trendSet - tweetSet
print

# The weakness of the above is that it compares tweet words to topics which
# could be phrases, so it would be better to compare trend topic phrase
# to original tweets.
# For now we can easily compare users by hashtag or keyword, or a user's
# hashtags against a place's trending hashtags.


# Todo:
# map user to words
# and map location to words
# then export as CSV