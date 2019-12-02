
## Cursor
# simple
#   api.user_timeline(id="twitter")
# rather do as
#   tweepy.Cursor(api.user_timeline, id="twitter")



from __future__ import print_function
if False:
    # Use Cursor to go through pages of results.
    for follower in limitHandled(list(tweepy.Cursor(api.followers).items())):
        if follower.friends_count > 2:
            print(follower.screen_name)


# Get followers
if False:
    # api.friends
    # api.friends_timeline
    # items(200)
    for follower in tweepy.Cursor(api.followers).items():
        print(follower)
        print()
        #follower.follow()


"""
http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html

Items or Pages

So far we have just demonstrated pagination iterating per an item. What if instead you want to process per a page of results? You would use the pages() method:

for page in tweepy.Cursor(api.user_timeline).pages():
    # page is a list of statuses
    process_page(page)

Limits

What if you only want n items or pages returned? You pass into the items() or pages() methods the limit you want to impose.

# Only iterate through the first 200 statuses
for status in tweepy.Cursor(api.user_timeline).items(200):
    process_status(status)

# Only iterate through the first 3 pages
for page in tweepy.Cursor(api.user_timeline).pages(3):
    process_page(page)
"""


