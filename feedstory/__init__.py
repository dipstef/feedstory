from feedstory.result import FeedResult
from .result import FeedEntryPage
from .rss import parse_feed_result


class FeedsCached(object):

    def __init__(self, cache):
        self._cache = cache

    def parse_entries(self, feed_url, etag=None):
        etag = etag or self._get_last_feed_etag(feed_url)

        return self._parse_entries(feed_url, etag)

    def _parse_entries(self, feed_url, etag=None):
        feed_result = parse_feed_result(feed_url, etag=etag)

        if feed_result.entries:
            self._cache.add_feed_result(feed_result)

        return feed_result

    def _get_last_feed_etag(self, feed_url):
        last_result = self._cache.get_last_result(feed_url)

        etag = last_result.etag if last_result else None
        return etag

    def _filter_un_existing_entries(self, entries):
        unread = [entry for entry in entries if not self._cache.get_entry(entry.url)]
        return unread