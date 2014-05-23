import time
from urllib2 import URLError

import feedparser
from procol.console import print_err

from feedstory.rss.result import _filter_valid_entries, FeedUnchanged, RssErrorResult, RssResult


def parse_feed_result(feed_url, etag=None):
    while True:
        try:
            return _parse_feed_result(feed_url, etag)
        except URLError, e:
            print_err(str(e))
            time.sleep(10)
        except BaseException, e:
            print_err('Exception: %s : %s' % (type(e), e))
            time.sleep(60)


def _parse_feed_result(feed_url, etag=None):
    feed = feedparser.parse(feed_url, etag=etag)

    if not 'bozo_exception' in feed:
        return FeedUnchanged(feed_url, feed) if feed.status == 304 else RssResult(feed)
    elif isinstance(feed.bozo_exception, URLError):
        raise feed.bozo_exception
    else:
        return RssErrorResult(feed, feed.bozo_exception)