import os
from feedstory.cache import FeedCacheConnect
import quecco


_cache_path = os.path.join(os.path.dirname(__file__), 'feed_cache.db')


class FeedCaches(object):

    def __init__(self, connection=quecco.local):
        self._conn = None
        self._connect = FeedCacheConnect(connection)

    #can return a cache by site or feed category
    def get_cache(self, **kwargs):
        if self._conn is None:
            self._conn = self._connect(_cache_path)
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()

caches = FeedCaches()