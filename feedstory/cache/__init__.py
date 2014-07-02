import os

import quecco
from .feed_cache import FeedCache


_init_file = os.path.join(os.path.dirname(__file__), 'feed_cache.sql')


class FeedCacheConnect(object):

    def __init__(self, connection=quecco.local):
        self._connection = connection

    def __call__(self, path):
        conn = self._connection(path, init_file=_init_file)
        return FeedCache(conn)


def connect(path, connection=quecco.local):
    connection = FeedCacheConnect(connection)
    return connection(path)