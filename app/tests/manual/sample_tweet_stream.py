# -*- coding: utf-8 -*-
"""
Working with one tweet from the streaming API.

Usage:
    $ ipython -i FILENAME
    >>> data = main()
    >>> data.keys() # Then explore the `data` object in ipython.
    [u'contributors', u'truncated', u'text', u'is_quote_status',
    u'in_reply_to_status_id', u'id', u'favorite_count', u'source',
    u'retweeted', u'coordinates', u'timestamp_ms', u'entities',
    u'in_reply_to_screen_name', u'id_str', u'retweet_count',
    u'in_reply_to_user_id', u'favorited', u'retweeted_status',
    u'user', u'geo', u'in_reply_to_user_id_str', u'lang',
    u'created_at', u'filter_level', u'in_reply_to_status_id_str',
    u'place']

    >>> data['text']
    u'RT @twice_ph: [TWICETAGRAM] 170701\n\uc624\ub79c\ub9cc\uc5d0 #\ub450\ubd80\ud55c\ubaa8 \n\uc800\ud76c\ub294 \uc798 \uc788\uc5b4\uc694 \uc6b0\ub9ac #ONCE \ub294?\n#ONCE \uac00 \ubcf4\uace0\uc2f6\ub2e4\n\n\ub4a4\uc5d4 \uc0c1\ud07c\uc8fc\uc758 \ucbd4\uc704\uac00 \ucc0d\uc5b4\uc900 \uc0ac\uc9c4\u314b\u314b\u314b \n#TWICE #\ud2b8\uc640\uc774\uc2a4\u2026 '

    >>> print data['text']
    RT @twice_ph: [TWICETAGRAM] 170701
    오랜만에 #두부한모
    저희는 잘 있어요 우리 #ONCE 는?
    #ONCE 가 보고싶다

    뒤엔 상큼주의 쯔위가 찍어준 사진ㅋㅋㅋ
    #TWICE #트와이스…


If copying from the command line into Python, characters need to be escaped
or the prefix `r` must be applied to the string.

Alternatives which I couldn't get to work fully:
    https://stackoverflow.com/questions/22394235/invalid-control-character-with-python-json-loads
    https://stackoverflow.com/questions/7262828/python-how-to-convert-string-literal-to-raw-string-literal
"""
import json


def main():
    # No line breaks, straight from API
    x = r'{"created_at":"Sat Jul 01 08:43:29 +0000 2017","id":881070742980313088,"id_str":"881070742980313088","text":"RT @twice_ph: [TWICETAGRAM] 170701\n\\uc624\\ub79c\\ub9cc\\uc5d0 #\\ub450\\ubd80\\ud55c\\ubaa8 \n\\uc800\\ud76c\\ub294 \\uc798 \\uc788\\uc5b4\\uc694 \\uc6b0\\ub9ac #ONCE \\ub294?\n#ONCE \\uac00 \\ubcf4\\uace0\\uc2f6\\ub2e4\n\n\\ub4a4\\uc5d4 \\uc0c1\\ud07c\\uc8fc\\uc758 \\ucbd4\\uc704\\uac00 \\ucc0d\\uc5b4\\uc900 \\uc0ac\\uc9c4\\u314b\\u314b\\u314b \n#TWICE #\\ud2b8\\uc640\\uc774\\uc2a4\\u2026 ","source":"\\u003ca href="http:\\/\\/twitter.com\\/download\\/android" rel="nofollow"\\u003eTwitter for Android\\u003c\\/a\\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":3722867834,"id_str":"3722867834","name":"Amazing Twice","screen_name":"metdew1","location":"\\ub300\\ud55c\\ubbfc\\uad6d \\uc11c\\uc6b8","url":null,"description":"I\'m a korean. My age too old. \nBut really really like TWICE. World ONCE\nfamily i alway thanks your support to\nTWICE. Wish good luck alway with U.","protected":false,"verified":false,"followers_count":977,"friends_count":1204,"listed_count":59,"favourites_count":114142,"statuses_count":100351,"created_at":"Tue Sep 29 06:19:21 +0000 2015","utc_offset":-25200,"time_zone":"Pacific Time (US & Canada)","geo_enabled":false,"lang":"ko","contributors_enabled":false,"is_translator":false,"profile_background_color":"000000","profile_background_image_url":"http:\\/\\/abs.twimg.com\\/images\\/themes\\/theme1\\/bg.png","profile_background_image_url_https":"https:\\/\\/abs.twimg.com\\/images\\/themes\\/theme1\\/bg.png","profile_background_tile":false,"profile_link_color":"9266CC","profile_sidebar_border_color":"000000","profile_sidebar_fill_color":"000000","profile_text_color":"000000","profile_use_background_image":false,"profile_image_url":"http:\\/\\/pbs.twimg.com\\/profile_images\\/858888732539207681\\/89mbzS98_normal.jpg","profile_image_url_https":"https:\\/\\/pbs.twimg.com\\/profile_images\\/858888732539207681\\/89mbzS98_normal.jpg","profile_banner_url":"https:\\/\\/pbs.twimg.com\\/profile_banners\\/3722867834\\/1494858108","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweeted_status":{"created_at":"Sat Jul 01 06:10:54 +0000 2017","id":881032343829463040,"id_str":"881032343829463040","text":"[TWICETAGRAM] 170701\n\\uc624\\ub79c\\ub9cc\\uc5d0 #\\ub450\\ubd80\\ud55c\\ubaa8 \n\\uc800\\ud76c\\ub294 \\uc798 \\uc788\\uc5b4\\uc694 \\uc6b0\\ub9ac #ONCE \\ub294?\n#ONCE \\uac00 \\ubcf4\\uace0\\uc2f6\\ub2e4\n\n\\ub4a4\\uc5d4 \\uc0c1\\ud07c\\uc8fc\\uc758 \\ucbd4\\uc704\\uac00 \\ucc0d\\uc5b4\\uc900 \\uc0ac\\uc9c4\\u314b\\u314b\\u314b \n#TWICE #\\ud2b8\\uc640\\uc774\\uc2a4\\u2026 https:\\/\\/t.co\\/9CPNYQiwcq","display_text_range":[0,140],"source":"\\u003ca href="http:\\/\\/twitter.com\\/download\\/android" rel="nofollow"\\u003eTwitter for Android\\u003c\\/a\\u003e","truncated":true,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":3779372892,"id_str":"3779372892","name":"TWICE PHILIPPINES \\u2728","screen_name":"twice_ph","location":"Philippines \\ud544\\ub9ac\\ud540","url":null,"description":"Philippine-based support group for TWICE. Officially affiliated with JYPNPH and PKCI http:\\/\\/facebook.com\\/groups\\/TWICEPH\\u2026 ... http:\\/\\/facebook.com\\/TWICEPH\\/","protected":false,"verified":false,"followers_count":7071,"friends_count":224,"listed_count":72,"favourites_count":523,"statuses_count":12448,"created_at":"Sun Oct 04 09:05:12 +0000 2015","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":"en","contributors_enabled":false,"is_translator":false,"profile_background_color":"FFFFFF","profile_background_image_url":"http:\\/\\/pbs.twimg.com\\/profile_background_images\\/722977345053712385\\/naASDMjX.jpg","profile_background_image_url_https":"https:\\/\\/pbs.twimg.com\\/profile_background_images\\/722977345053712385\\/naASDMjX.jpg","profile_background_tile":true,"profile_link_color":"FF3485","profile_sidebar_border_color":"000000","profile_sidebar_fill_color":"000000","profile_text_color":"000000","profile_use_background_image":true,"profile_image_url":"http:\\/\\/pbs.twimg.com\\/profile_images\\/863338740629905408\\/tO_19lHj_normal.jpg","profile_image_url_https":"https:\\/\\/pbs.twimg.com\\/profile_images\\/863338740629905408\\/tO_19lHj_normal.jpg","profile_banner_url":"https:\\/\\/pbs.twimg.com\\/profile_banners\\/3779372892\\/1494670969","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"extended_tweet":{"full_text":"[TWICETAGRAM] 170701\n\\uc624\\ub79c\\ub9cc\\uc5d0 #\\ub450\\ubd80\\ud55c\\ubaa8 \n\\uc800\\ud76c\\ub294 \\uc798 \\uc788\\uc5b4\\uc694 \\uc6b0\\ub9ac #ONCE \\ub294?\n#ONCE \\uac00 \\ubcf4\\uace0\\uc2f6\\ub2e4\n\n\\ub4a4\\uc5d4 \\uc0c1\\ud07c\\uc8fc\\uc758 \\ucbd4\\uc704\\uac00 \\ucc0d\\uc5b4\\uc900 \\uc0ac\\uc9c4\\u314b\\u314b\\u314b \n#TWICE #\\ud2b8\\uc640\\uc774\\uc2a4 \nhttps:\\/\\/t.co\\/NHPtfkruR4 https:\\/\\/t.co\\/WRv9qP8Mk2","display_text_range":[0,129],"entities":{"hashtags":[{"text":"\\ub450\\ubd80\\ud55c\\ubaa8","indices":[26,31]},{"text":"ONCE","indices":[46,51]},{"text":"ONCE","indices":[55,60]},{"text":"TWICE","indices":[92,98]},{"text":"\\ud2b8\\uc640\\uc774\\uc2a4","indices":[99,104]}],"urls":[{"url":"https:\\/\\/t.co\\/NHPtfkruR4","expanded_url":"https:\\/\\/www.instagram.com\\/p\\/BV_i2J_gx1w\\/","display_url":"instagram.com\\/p\\/BV_i2J_gx1w\\/","indices":[106,129]}],"user_mentions":[],"symbols":[],"media":[{"id":881032307179573248,"id_str":"881032307179573248","indices":[130,153],"media_url":"http:\\/\\/pbs.twimg.com\\/media\\/DDoONykU0AAT3d6.jpg","media_url_https":"https:\\/\\/pbs.twimg.com\\/media\\/DDoONykU0AAT3d6.jpg","url":"https:\\/\\/t.co\\/WRv9qP8Mk2","display_url":"pic.twitter.com\\/WRv9qP8Mk2","expanded_url":"https:\\/\\/twitter.com\\/twice_ph\\/status\\/881032343829463040\\/photo\\/1","type":"photo","sizes":{"thumb":{"w":150,"h":150,"resize":"crop"},"small":{"w":680,"h":680,"resize":"fit"},"medium":{"w":960,"h":960,"resize":"fit"},"large":{"w":960,"h":960,"resize":"fit"}}},{"id":881032328272683008,"id_str":"881032328272683008","indices":[130,153],"media_url":"http:\\/\\/pbs.twimg.com\\/media\\/DDoOPBJUIAAlDMF.jpg","media_url_https":"https:\\/\\/pbs.twimg.com\\/media\\/DDoOPBJUIAAlDMF.jpg","url":"https:\\/\\/t.co\\/WRv9qP8Mk2","display_url":"pic.twitter.com\\/WRv9qP8Mk2","expanded_url":"https:\\/\\/twitter.com\\/twice_ph\\/status\\/881032343829463040\\/photo\\/1","type":"photo","sizes":{"large":{"w":734,"h":734,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"medium":{"w":734,"h":734,"resize":"fit"},"small":{"w":680,"h":680,"resize":"fit"}}}]},"extended_entities":{"media":[{"id":881032307179573248,"id_str":"881032307179573248","indices":[130,153],"media_url":"http:\\/\\/pbs.twimg.com\\/media\\/DDoONykU0AAT3d6.jpg","media_url_https":"https:\\/\\/pbs.twimg.com\\/media\\/DDoONykU0AAT3d6.jpg","url":"https:\\/\\/t.co\\/WRv9qP8Mk2","display_url":"pic.twitter.com\\/WRv9qP8Mk2","expanded_url":"https:\\/\\/twitter.com\\/twice_ph\\/status\\/881032343829463040\\/photo\\/1","type":"photo","sizes":{"thumb":{"w":150,"h":150,"resize":"crop"},"small":{"w":680,"h":680,"resize":"fit"},"medium":{"w":960,"h":960,"resize":"fit"},"large":{"w":960,"h":960,"resize":"fit"}}},{"id":881032328272683008,"id_str":"881032328272683008","indices":[130,153],"media_url":"http:\\/\\/pbs.twimg.com\\/media\\/DDoOPBJUIAAlDMF.jpg","media_url_https":"https:\\/\\/pbs.twimg.com\\/media\\/DDoOPBJUIAAlDMF.jpg","url":"https:\\/\\/t.co\\/WRv9qP8Mk2","display_url":"pic.twitter.com\\/WRv9qP8Mk2","expanded_url":"https:\\/\\/twitter.com\\/twice_ph\\/status\\/881032343829463040\\/photo\\/1","type":"photo","sizes":{"large":{"w":734,"h":734,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"medium":{"w":734,"h":734,"resize":"fit"},"small":{"w":680,"h":680,"resize":"fit"}}}]}},"retweet_count":1,"favorite_count":40,"entities":{"hashtags":[{"text":"\\ub450\\ubd80\\ud55c\\ubaa8","indices":[26,31]},{"text":"ONCE","indices":[46,51]},{"text":"ONCE","indices":[55,60]},{"text":"TWICE","indices":[92,98]},{"text":"\\ud2b8\\uc640\\uc774\\uc2a4","indices":[99,104]}],"urls":[{"url":"https:\\/\\/t.co\\/9CPNYQiwcq","expanded_url":"https:\\/\\/twitter.com\\/i\\/web\\/status\\/881032343829463040","display_url":"twitter.com\\/i\\/web\\/status\\/8\\u2026","indices":[106,129]}],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"ko"},"is_quote_status":false,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[{"text":"\\ub450\\ubd80\\ud55c\\ubaa8","indices":[40,45]},{"text":"ONCE","indices":[60,65]},{"text":"ONCE","indices":[69,74]},{"text":"TWICE","indices":[106,112]},{"text":"\\ud2b8\\uc640\\uc774\\uc2a4","indices":[113,118]}],"urls":[{"url":"","expanded_url":null,"indices":[120,120]}],"user_mentions":[{"screen_name":"twice_ph","name":"TWICE PHILIPPINES \\u2728","id":3779372892,"id_str":"3779372892","indices":[3,12]}],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"ko","timestamp_ms":"1498898609286"}'

    # With link breaks from formatting - see http://jsonviewer.stack.hu/
    y = r"""{
      "id": 881070742980313088,
      "created_at": "Sat Jul 01 08:43:29 +0000 2017",
      "id_str": "881070742980313088",
      "text": "RT @twice_ph: [TWICETAGRAM] 170701\n\uc624\ub79c\ub9cc\uc5d0 #\ub450\ubd80\ud55c\ubaa8 \n\uc800\ud76c\ub294 \uc798 \uc788\uc5b4\uc694 \uc6b0\ub9ac #ONCE \ub294?\n#ONCE \uac00 \ubcf4\uace0\uc2f6\ub2e4\n\n\ub4a4\uc5d4 \uc0c1\ud07c\uc8fc\uc758 \ucbd4\uc704\uac00 \ucc0d\uc5b4\uc900 \uc0ac\uc9c4\u314b\u314b\u314b \n#TWICE #\ud2b8\uc640\uc774\uc2a4\u2026 ",
      "source": "\u003ca href=\"http:\/\/twitter.com\/download\/android\" rel=\"nofollow\"\u003eTwitter for Android\u003c\/a\u003e",
      "truncated": false,
      "in_reply_to_status_id": null,
      "in_reply_to_status_id_str": null,
      "in_reply_to_user_id": null,
      "in_reply_to_user_id_str": null,
      "in_reply_to_screen_name": null,
      "user": {
        "id": 3722867834,
        "id_str": "3722867834",
        "name": "Amazing Twice",
        "screen_name": "metdew1",
        "location": "\ub300\ud55c\ubbfc\uad6d \uc11c\uc6b8",
        "url": null,
        "description": "I'm a korean. My age too old. \nBut really really like TWICE. World ONCE\nfamily i alway thanks your support to\nTWICE. Wish good luck alway with U.",
        "protected": false,
        "verified": false,
        "followers_count": 977,
        "friends_count": 1204,
        "listed_count": 59,
        "favourites_count": 114142,
        "statuses_count": 100351,
        "created_at": "Tue Sep 29 06:19:21 +0000 2015",
        "utc_offset": -25200,
        "time_zone": "Pacific Time (US & Canada)",
        "geo_enabled": false,
        "lang": "ko",
        "contributors_enabled": false,
        "is_translator": false,
        "profile_background_color": "000000",
        "profile_background_image_url": "http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png",
        "profile_background_image_url_https": "https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png",
        "profile_background_tile": false,
        "profile_link_color": "9266CC",
        "profile_sidebar_border_color": "000000",
        "profile_sidebar_fill_color": "000000",
        "profile_text_color": "000000",
        "profile_use_background_image": false,
        "profile_image_url": "http:\/\/pbs.twimg.com\/profile_images\/858888732539207681\/89mbzS98_normal.jpg",
        "profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/858888732539207681\/89mbzS98_normal.jpg",
        "profile_banner_url": "https:\/\/pbs.twimg.com\/profile_banners\/3722867834\/1494858108",
        "default_profile": false,
        "default_profile_image": false,
        "following": null,
        "follow_request_sent": null,
        "notifications": null
      },
      "geo": null,
      "coordinates": null,
      "place": null,
      "contributors": null,
      "retweeted_status": {
        "created_at": "Sat Jul 01 06:10:54 +0000 2017",
        "id": 881032343829463040,
        "id_str": "881032343829463040",
        "text": "[TWICETAGRAM] 170701\n\uc624\ub79c\ub9cc\uc5d0 #\ub450\ubd80\ud55c\ubaa8 \n\uc800\ud76c\ub294 \uc798 \uc788\uc5b4\uc694 \uc6b0\ub9ac #ONCE \ub294?\n#ONCE \uac00 \ubcf4\uace0\uc2f6\ub2e4\n\n\ub4a4\uc5d4 \uc0c1\ud07c\uc8fc\uc758 \ucbd4\uc704\uac00 \ucc0d\uc5b4\uc900 \uc0ac\uc9c4\u314b\u314b\u314b \n#TWICE #\ud2b8\uc640\uc774\uc2a4\u2026 https:\/\/t.co\/9CPNYQiwcq",
        "display_text_range": [
          0,
          140
        ],
        "source": "\u003ca href=\"http:\/\/twitter.com\/download\/android\" rel=\"nofollow\"\u003eTwitter for Android\u003c\/a\u003e",
        "truncated": true,
        "in_reply_to_status_id": null,
        "in_reply_to_status_id_str": null,
        "in_reply_to_user_id": null,
        "in_reply_to_user_id_str": null,
        "in_reply_to_screen_name": null,
        "user": {
          "id": 3779372892,
          "id_str": "3779372892",
          "name": "TWICE PHILIPPINES \u2728",
          "screen_name": "twice_ph",
          "location": "Philippines \ud544\ub9ac\ud540",
          "url": null,
          "description": "Philippine-based support group for TWICE. Officially affiliated with JYPNPH and PKCI http:\/\/facebook.com\/groups\/TWICEPH\u2026 ... http:\/\/facebook.com\/TWICEPH\/",
          "protected": false,
          "verified": false,
          "followers_count": 7071,
          "friends_count": 224,
          "listed_count": 72,
          "favourites_count": 523,
          "statuses_count": 12448,
          "created_at": "Sun Oct 04 09:05:12 +0000 2015",
          "utc_offset": null,
          "time_zone": null,
          "geo_enabled": false,
          "lang": "en",
          "contributors_enabled": false,
          "is_translator": false,
          "profile_background_color": "FFFFFF",
          "profile_background_image_url": "http:\/\/pbs.twimg.com\/profile_background_images\/722977345053712385\/naASDMjX.jpg",
          "profile_background_image_url_https": "https:\/\/pbs.twimg.com\/profile_background_images\/722977345053712385\/naASDMjX.jpg",
          "profile_background_tile": true,
          "profile_link_color": "FF3485",
          "profile_sidebar_border_color": "000000",
          "profile_sidebar_fill_color": "000000",
          "profile_text_color": "000000",
          "profile_use_background_image": true,
          "profile_image_url": "http:\/\/pbs.twimg.com\/profile_images\/863338740629905408\/tO_19lHj_normal.jpg",
          "profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/863338740629905408\/tO_19lHj_normal.jpg",
          "profile_banner_url": "https:\/\/pbs.twimg.com\/profile_banners\/3779372892\/1494670969",
          "default_profile": false,
          "default_profile_image": false,
          "following": null,
          "follow_request_sent": null,
          "notifications": null
        },
        "geo": null,
        "coordinates": null,
        "place": null,
        "contributors": null,
        "is_quote_status": false,
        "extended_tweet": {
          "full_text": "[TWICETAGRAM] 170701\n\uc624\ub79c\ub9cc\uc5d0 #\ub450\ubd80\ud55c\ubaa8 \n\uc800\ud76c\ub294 \uc798 \uc788\uc5b4\uc694 \uc6b0\ub9ac #ONCE \ub294?\n#ONCE \uac00 \ubcf4\uace0\uc2f6\ub2e4\n\n\ub4a4\uc5d4 \uc0c1\ud07c\uc8fc\uc758 \ucbd4\uc704\uac00 \ucc0d\uc5b4\uc900 \uc0ac\uc9c4\u314b\u314b\u314b \n#TWICE #\ud2b8\uc640\uc774\uc2a4 \nhttps:\/\/t.co\/NHPtfkruR4 https:\/\/t.co\/WRv9qP8Mk2",
          "display_text_range": [
            0,
            129
          ],
          "entities": {
            "hashtags": [
              {
                "text": "\ub450\ubd80\ud55c\ubaa8",
                "indices": [
                  26,
                  31
                ]
              },
              {
                "text": "ONCE",
                "indices": [
                  46,
                  51
                ]
              },
              {
                "text": "ONCE",
                "indices": [
                  55,
                  60
                ]
              },
              {
                "text": "TWICE",
                "indices": [
                  92,
                  98
                ]
              },
              {
                "text": "\ud2b8\uc640\uc774\uc2a4",
                "indices": [
                  99,
                  104
                ]
              }
            ],
            "urls": [
              {
                "url": "https:\/\/t.co\/NHPtfkruR4",
                "expanded_url": "https:\/\/www.instagram.com\/p\/BV_i2J_gx1w\/",
                "display_url": "instagram.com\/p\/BV_i2J_gx1w\/",
                "indices": [
                  106,
                  129
                ]
              }
            ],
            "user_mentions": [
    
            ],
            "symbols": [
    
            ],
            "media": [
              {
                "id": 881032307179573248,
                "id_str": "881032307179573248",
                "indices": [
                  130,
                  153
                ],
                "media_url": "http:\/\/pbs.twimg.com\/media\/DDoONykU0AAT3d6.jpg",
                "media_url_https": "https:\/\/pbs.twimg.com\/media\/DDoONykU0AAT3d6.jpg",
                "url": "https:\/\/t.co\/WRv9qP8Mk2",
                "display_url": "pic.twitter.com\/WRv9qP8Mk2",
                "expanded_url": "https:\/\/twitter.com\/twice_ph\/status\/881032343829463040\/photo\/1",
                "type": "photo",
                "sizes": {
                  "thumb": {
                    "w": 150,
                    "h": 150,
                    "resize": "crop"
                  },
                  "small": {
                    "w": 680,
                    "h": 680,
                    "resize": "fit"
                  },
                  "medium": {
                    "w": 960,
                    "h": 960,
                    "resize": "fit"
                  },
                  "large": {
                    "w": 960,
                    "h": 960,
                    "resize": "fit"
                  }
                }
              },
              {
                "id": 881032328272683008,
                "id_str": "881032328272683008",
                "indices": [
                  130,
                  153
                ],
                "media_url": "http:\/\/pbs.twimg.com\/media\/DDoOPBJUIAAlDMF.jpg",
                "media_url_https": "https:\/\/pbs.twimg.com\/media\/DDoOPBJUIAAlDMF.jpg",
                "url": "https:\/\/t.co\/WRv9qP8Mk2",
                "display_url": "pic.twitter.com\/WRv9qP8Mk2",
                "expanded_url": "https:\/\/twitter.com\/twice_ph\/status\/881032343829463040\/photo\/1",
                "type": "photo",
                "sizes": {
                  "large": {
                    "w": 734,
                    "h": 734,
                    "resize": "fit"
                  },
                  "thumb": {
                    "w": 150,
                    "h": 150,
                    "resize": "crop"
                  },
                  "medium": {
                    "w": 734,
                    "h": 734,
                    "resize": "fit"
                  },
                  "small": {
                    "w": 680,
                    "h": 680,
                    "resize": "fit"
                  }
                }
              }
            ]
          },
          "extended_entities": {
            "media": [
              {
                "id": 881032307179573248,
                "id_str": "881032307179573248",
                "indices": [
                  130,
                  153
                ],
                "media_url": "http:\/\/pbs.twimg.com\/media\/DDoONykU0AAT3d6.jpg",
                "media_url_https": "https:\/\/pbs.twimg.com\/media\/DDoONykU0AAT3d6.jpg",
                "url": "https:\/\/t.co\/WRv9qP8Mk2",
                "display_url": "pic.twitter.com\/WRv9qP8Mk2",
                "expanded_url": "https:\/\/twitter.com\/twice_ph\/status\/881032343829463040\/photo\/1",
                "type": "photo",
                "sizes": {
                  "thumb": {
                    "w": 150,
                    "h": 150,
                    "resize": "crop"
                  },
                  "small": {
                    "w": 680,
                    "h": 680,
                    "resize": "fit"
                  },
                  "medium": {
                    "w": 960,
                    "h": 960,
                    "resize": "fit"
                  },
                  "large": {
                    "w": 960,
                    "h": 960,
                    "resize": "fit"
                  }
                }
              },
              {
                "id": 881032328272683008,
                "id_str": "881032328272683008",
                "indices": [
                  130,
                  153
                ],
                "media_url": "http:\/\/pbs.twimg.com\/media\/DDoOPBJUIAAlDMF.jpg",
                "media_url_https": "https:\/\/pbs.twimg.com\/media\/DDoOPBJUIAAlDMF.jpg",
                "url": "https:\/\/t.co\/WRv9qP8Mk2",
                "display_url": "pic.twitter.com\/WRv9qP8Mk2",
                "expanded_url": "https:\/\/twitter.com\/twice_ph\/status\/881032343829463040\/photo\/1",
                "type": "photo",
                "sizes": {
                  "large": {
                    "w": 734,
                    "h": 734,
                    "resize": "fit"
                  },
                  "thumb": {
                    "w": 150,
                    "h": 150,
                    "resize": "crop"
                  },
                  "medium": {
                    "w": 734,
                    "h": 734,
                    "resize": "fit"
                  },
                  "small": {
                    "w": 680,
                    "h": 680,
                    "resize": "fit"
                  }
                }
              }
            ]
          }
        },
        "retweet_count": 1,
        "favorite_count": 40,
        "entities": {
          "hashtags": [
            {
              "text": "\ub450\ubd80\ud55c\ubaa8",
              "indices": [
                26,
                31
              ]
            },
            {
              "text": "ONCE",
              "indices": [
                46,
                51
              ]
            },
            {
              "text": "ONCE",
              "indices": [
                55,
                60
              ]
            },
            {
              "text": "TWICE",
              "indices": [
                92,
                98
              ]
            },
            {
              "text": "\ud2b8\uc640\uc774\uc2a4",
              "indices": [
                99,
                104
              ]
            }
          ],
          "urls": [
            {
              "url": "https:\/\/t.co\/9CPNYQiwcq",
              "expanded_url": "https:\/\/twitter.com\/i\/web\/status\/881032343829463040",
              "display_url": "twitter.com\/i\/web\/status\/8\u2026",
              "indices": [
                106,
                129
              ]
            }
          ],
          "user_mentions": [
    
          ],
          "symbols": [
    
          ]
        },
        "favorited": false,
        "retweeted": false,
        "possibly_sensitive": false,
        "filter_level": "low",
        "lang": "ko"
      },
      "is_quote_status": false,
      "retweet_count": 0,
      "favorite_count": 0,
      "entities": {
        "hashtags": [
          {
            "text": "\ub450\ubd80\ud55c\ubaa8",
            "indices": [
              40,
              45
            ]
          },
          {
            "text": "ONCE",
            "indices": [
              60,
              65
            ]
          },
          {
            "text": "ONCE",
            "indices": [
              69,
              74
            ]
          },
          {
            "text": "TWICE",
            "indices": [
              106,
              112
            ]
          },
          {
            "text": "\ud2b8\uc640\uc774\uc2a4",
            "indices": [
              113,
              118
            ]
          }
        ],
        "urls": [
          {
            "url": "",
            "expanded_url": null,
            "indices": [
              120,
              120
            ]
          }
        ],
        "user_mentions": [
          {
            "screen_name": "twice_ph",
            "name": "TWICE PHILIPPINES \u2728",
            "id": 3779372892,
            "id_str": "3779372892",
            "indices": [
              3,
              12
            ]
          }
        ],
        "symbols": [
    
        ]
      },
      "favorited": false,
      "retweeted": false,
      "filter_level": "low",
      "lang": "ko",
      "timestamp_ms": "1498898609286"
    }
    """
    # Works on y, but not x
    data = json.loads(y)

    print(json.dumps(data, indent=4))

    return data


if __name__ == '__main__':
    main()
