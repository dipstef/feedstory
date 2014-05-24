from urlparse import urljoin

from httpy.client import http_client
from urlo.parser import build_url
from dated.date_string import datetime_from_string

from ..rss.result_json import json_to_feed
from ..rss.result import JsonRssResult
from ..result import FeedEntryPage


class FeedCacheClient(object):
    def __init__(self, address, client=http_client):
        self._client = client
        self._result_url = build_url(host=address[0], port=address[1], path='/cache/feed')
        self._entry_url = urljoin(self._result_url, '/entry')

    def get_entry(self, entry_url):
        response = self._client.get(self._entry_url, params=dict(url=entry_url), timeout=30)

        entry_json = json_to_feed(response.body)
        if entry_json:
            return _convert_entry(entry_json)

    def add_feed_result(self, result):
        self._client.post(self._result_url, params=dict(feed=result.json))

    def get_last_result(self, feed_url):
        response = self._client.get(self._result_url, params=dict(url=feed_url), timeout=60)
        if response.body:
            return JsonRssResult(response.body)


def _convert_entry(entry):
    return FeedEntryPage(entry.url, entry.title, datetime_from_string(entry.publication))