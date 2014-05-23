import os

from dated.normalized import utc
import quelo

from .db.feed_entry import get_feed_entry, get_feed_entry_id, insert_feed_entry
from .db.feed_result import insert_feed_result_location, get_feed_result_location_id, get_feed_result_id, \
    insert_feed_result, insert_feed, update_feed_result, insert_feed_result_unread, insert_rss_feed_result, \
    get_feed_result_entry_id, insert_feed_result_entry, get_feed_id
from ..result import FeedEntryPage, FeedUnreadEntries


class FeedCache(object):

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_entry(self, entry_url):
        entry = get_feed_entry(self._cursor, entry_url)
        if entry:
            return FeedEntryPage(entry_url, *entry)

    def add_feed_result(self, result):
        self._add_feed_result(result, result.url)

        for entry in result:
            if entry.url:
                self.add_feed_entry(result, entry)

        self._conn.commit()

    def _add_feed_result(self, result, feed_url):
        self._add_feed_result_location(result, feed_url)

        feed_result_id = get_feed_result_id(self._cursor, result.location_id, result.updated)

        if not feed_result_id:
            insert_feed_result(self._cursor, result.location_id, result.updated, utc.now(), result.json)
            feed_result_id = get_feed_result_id(self._cursor, result.location_id, result.updated)

            #This is to mark that we have been requesting unread entries
            if isinstance(result, FeedUnreadEntries):
                insert_feed_result_unread(self._cursor, feed_result_id)

            self._add_result(feed_result_id, result)
        else:
            update_feed_result(self._cursor, feed_result_id, utc.now(), result.json)

        result.db_id = feed_result_id

    def _add_result(self, feed_result_id, result):
        insert_rss_feed_result(self._cursor, feed_result_id)

    def _add_feed_result_location(self, result, feed_url):
        # The location(url) of the result, in case of the simple rss feed it is equals to the feed url,
        # however in cases as google reader or feedly where the feed history could be scrolled this equal to the
        # result set url
        self._add_feed(result, feed_url)

        result_location_id = get_feed_result_location_id(self._cursor, result.feed_id, result.url)
        if not result_location_id:
            insert_feed_result_location(self._cursor, result.feed_id, result.url)
            result_location_id = get_feed_result_location_id(self._cursor, result.feed_id, result.url)

        result.location_id = result_location_id

    def _add_feed(self, result, feed_url):
        feed_id = get_feed_id(self._cursor, result.url)

        if not feed_id:
            insert_feed(self._cursor, feed_url, result.title, result.description)
            feed_id = get_feed_id(self._cursor, feed_url)

        result.feed_id = feed_id

    def add_feed_entry(self, feed_result, entry):
        feed_entry_id = get_feed_entry_id(self._cursor, feed_result.feed_id, entry.url)

        if not feed_entry_id:
            feed_entry_id = self._add_result_entry(feed_result, entry)

        entry.db_id = feed_entry_id

        feed_result_entry_id = get_feed_result_entry_id(self._cursor, feed_result.db_id, entry.db_id)
        if not feed_result_entry_id:
            insert_feed_result_entry(self._cursor, feed_result.db_id, entry.db_id)

    def _add_result_entry(self, feed_result, entry):
        insert_feed_entry(self._cursor, feed_result.feed_id, entry.url, entry.title, entry.summary,
                          entry.publication, entry.json)

        feed_entry_id = get_feed_entry_id(self._cursor, feed_result.feed_id, entry.url)
        return feed_entry_id

    def close(self):
        self._conn.close()

_init_file = os.path.join(os.path.dirname(__file__), 'feed_cache.sql')


class FeedCacheConnect(object):

    def __init__(self, connection=quelo.connect):
        self._connection = connection

    def __call__(self, path):
        conn = self._connection(path, init_file=_init_file)
        return FeedCache(conn)
