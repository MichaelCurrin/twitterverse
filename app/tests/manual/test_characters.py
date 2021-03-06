#!/usr/bin/env python
"""
Exploration of how to handle unicode characters, in particular for tweets from
the Twitter API.
"""


def main():
    # =========
    # Example 1
    # =========

    # ASCII string.
    a = "Trump’s"
    # Unicode string. (This is the format from Twitter JSON.)
    b = "Trump’s"

    # Try convert to string object.
    # >>> str(a)
    # => 'Trump\xe2\x80\x99s' # no change
    # >>> str(b)
    # => Traceback (most recent call last):
    #    File "<stdin>", line 1, in <module>
    #        UnicodeEncodeError: 'ascii' codec can't encode character '\u2019'
    #           in position 5: ordinal not in range(128)

    # View the variable. Not human readible.
    # >>> a
    # => 'Trump\xe2\x80\x99s'
    # >>> b
    # => 'Trump\u2019s'

    # Print (turns out to be human readible output).
    print(a)
    # => Trump’s
    print(b)
    # => Trump’s

    # As a list. Note that the special character has to be stored in
    # a different form to what was entered.
    print([a])
    # => ['Trump\xe2\x80\x99s']
    print([b])
    # => ['Trump\u2019s']

    # From list back to standalone object. We see that the special character
    # is made human readible on printing.
    print([a][0])
    # => Trump’s
    print([b][0])
    # => Trump’s

    # Using __repr__ out of interest. The backlashes get quoted.
    # >>> repr(a)
    # => "'Trump\\xe2\\x80\\x99s'"
    # >>> repr(b)
    # => "'Trump\\u2019s'"

    # FIXME: No longer works in PY3 so should be updated or ignored.
    # Remove ALL unicode characters completely.
    # From https://stackoverflow.com/questions/15321138/removing-unicode-u2026-like-characters-in-a-string-in-python2-7
    # print(a.decode('unicode_escape').encode('ascii', 'ignore'))

    # => Trumps
    # print(b.decode('unicode_escape').encode('ascii', 'ignore'))
    # =>    Traceback (most recent call last):
    #         File "<stdin>", line 1, in <module>
    #           UnicodeEncodeError: 'ascii' codec can't encode character '\u2019'
    #           in position 5: ordinal not in range(128)

    print()

    # =========
    # Example 2
    # =========

    # Store and transform.
    c = "\u2026"
    # PY2 converts to str. PY3 converts to bytes.
    d = c.encode("utf-8")

    # PY3

    # >>> c
    # '…'
    # >>> d
    # b'\xe2\x80\xa6'

    # >>> print(c)
    # …
    # >>> print(d)
    # b'\xe2\x80\xa6'

    # PY2

    # >>> c
    # '\u2026'
    # >>> d
    # '\xe2\x80\xa6'

    print(c)
    # => …
    print(d)
    # => …

    # Note that applying `str(c)` raises an error and `unicode(c)` doesn't
    # change anything.

    print()

    # =========
    # Example 3
    # =========

    # Now how a pasted unicode symbol (shown here in brackets) renders the
    # same in a print for both types, but if entered as \uXXXX format then
    # the ascii string prints the characters literally.

    # unicode
    x = "I am unicode string with unicode symbol \u2026 (…)"
    y = "I am ascii string with unicode symbol \u2026 (…)"
    print(x)
    print(y)


if __name__ == "__main__":
    main()
