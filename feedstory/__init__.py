import time
from feedstory.result import FeedResult
from .result import FeedEntryPage
from .rss import parse_feed_result
from .cache import connect


class Feeds(object):

    def __init__(self, caches):
        self._caches = caches

    def add_entries(self, feed_url, etag=None):
        cache = self._caches.get_cache(feed_url)
        return FeedsStory(cache).add_entries(feed_url, etag)


class FeedsStory(object):

    def __init__(self, cache):
        self._cache = cache

    def add_entries(self, feed_url, etag=None):
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

    def record_feed(self, feed_url, refresh=60):
        for entries in self.iterate_history(feed_url, refresh=refresh):
            pass

    def iterate_history(self, feed_url, refresh=60):
        while True:
            entries = self.add_entries(feed_url)
            yield entries
            time.sleep(refresh)


def feedstory(path):
    return FeedsStory(connect(path))


