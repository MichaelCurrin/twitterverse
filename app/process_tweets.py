# -*- coding: utf-8 -*-
from string import punctuation

from test import _writeJSON, _readJSON

tweetData = _readJSON('var/tweet_test.json')

# Punctuation to be removed.
mySymbols = punctuation.replace(u'#', u'').replace(u'@', u'')

wordsDict = {}

for t in tweetData:
    # case?
    # apostrophes in words? ' vs ’?

    # Split by spaces and new line characters.
    words = t['text'].split(u' ')
    for w in words:
        print w
        cleanW = w.replace('\n', '')
        try:
            for p in mySymbols:
                if p in mySymbols:
                    cleanW = cleanW.replace(p, '')
            if cleanW.lower() not in (u'and', u'not', u'or', u'in') and \
                not cleanW.lower().startswith(u'http'):
                if cleanW not in wordsDict:
                    wordsDict.update({cleanW:1})
                else:
                    wordsDict[cleanW] +=1
        except UnicodeEncodeError:
            print 'unicode'
            print w
            raise
        print [cleanW]
        print

# America\u2019s ?

# this what happens when printing unicode string in a list or set
# Trump’s
#[u'Trump\u2019s']
# it can't be forced to string or get ascii error.
# however it's decoded fine when printing.

print wordsDict
print
for x in set(wordsDict):
    print x

# We can't easily get phrases from tweets to match up with trending topcs
# But we can search for presence of a topic in a user's tweets.
# after removing punctutation depending on rule for trending phrase?
# or do regex.

#print dir(set(wordsDict))
#['__and__', '__class__', '__cmp__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__iand__', '__init__', '__ior__', '__isub__', '__iter__', '__ixor__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__rand__', '__reduce__', '__reduce_ex__', '__repr__', '__ror__', '__rsub__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__xor__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'union', 'update']
