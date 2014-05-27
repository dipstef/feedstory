import os

import quelo

from .feed_cache import FeedCache


_init_file = os.path.join(os.path.dirname(__file__), 'feed_cache.sql')


class FeedCacheConnect(object):

    def __init__(self, connection=quelo.connect):
        self._connection = connection

    def __call__(self, path):
        conn = self._connection(path, init_file=_init_file)
        return FeedCache(conn)