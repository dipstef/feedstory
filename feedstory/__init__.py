from feedstory.result import FeedUnreadEntries
from .result import FeedEntryPage
from .rss import parse_feed_result


class FeedParserUnreadEntries(FeedUnreadEntries):
    def __init__(self, result, entries, unread_entries):
        super(FeedParserUnreadEntries, self).__init__(result.url, result.title, result.description, result.updated,
                                                      result.json, entries, unread=True)
        self.unread_entries = unread_entries
        self.etag = result.etag


class FeedCacheResults(object):

    def __init__(self, cache):
        self._cache = cache

    def parsed_unread_entries(self, feed_url):
        etag = self._get_last_feed_etag(feed_url)

        return self.parse_entries(feed_url, etag)

    def parse_entries(self, feed_url, etag=None):
        result = parse_feed_result(feed_url, etag=etag)

        if result.entries:
            unread = self._filter_un_existing_entries(result.entries) if not etag else result.entries

            result = FeedParserUnreadEntries(result, result.entries, unread)

            self._cache.add_feed_result(result)

        return result

    def _get_last_feed_etag(self, feed_url):
        last_result = self._cache.get_last_result(feed_url)
        etag = last_result.etag if last_result else None
        return etag

    def _filter_un_existing_entries(self, entries):
        unread = [entry for entry in entries if not self._cache.get_entry(entry.url)]
        return unread