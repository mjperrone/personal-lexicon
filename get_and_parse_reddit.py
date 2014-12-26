#!/usr/bin/env python
# usage: `python get_and_parse_reddit.py reddit_user_name`

import time
import urllib2
import json
import sys
import HTMLParser
import re


# returns (list of comments, list of comment ids)
def get_comments(url):
    time.sleep(2)
    request = urllib2.Request(url)
    response = None
    while response is None:
        try:
            response = urllib2.urlopen(request)
            data = response.read()
        except urllib2.HTTPError, err:
            if err.code == 429:  # too many requests
                time.sleep(12)
            else:
                raise err
    decoded = json.loads(data)
    return [x['data']['body_html'] for x in decoded['data']['children']], [x['data']['name'] for x in decoded['data']['children']]


def scrape_comments(targetUser):
    all_comments, all_ids = [], []
    url = "http://www.reddit.com/user/%s/comments/.json" % targetUser + "?count=%d&after=%s"
    pages = 0
    after = ''
    while True:
        comments, ids = get_comments(url % (pages * 25, after))

        if not comments or any(i in all_ids for i in ids):
            break

        after = ids[-1]
        all_ids.extend(ids)
        all_comments.extend(comments)
        pages += 1
    return all_comments


if __name__ == '__main__':
    comments = scrape_comments(sys.argv[-1])
    for c in comments:
        a = HTMLParser.HTMLParser().unescape
        print re.sub(r"<.*?>", "", a(a(c)))
