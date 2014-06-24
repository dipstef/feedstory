from urlparse import urljoin

from httpy.client import http_client
from urlo.unquoted import build_url

from ..rss.result import JsonRssResult


class FeedCacheClient(object):
    def __init__(self, address, client=http_client):
        self._client = client
        self._result_url = build_url(host=address[0], port=address[1], path='/cache/feed')
        self._entry_url = urljoin(self._result_url, '/entry')

    def add_feed_result(self, result):
        params = {'json': result.json}
        if not result.request_etag:
            params['etag'] = result.request_etag

        self._client.post(self._result_url, data=params)

    def get_last_result(self, feed_url):
        response = self._client.get(self._result_url, params=dict(url=feed_url), timeout=60)
        if response.body:
            return JsonRssResult(response.body)