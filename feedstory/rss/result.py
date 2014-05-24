from dated import utc
from procol.console import print_err_trace

from .result_json import feed_to_json, json_to_feed
from ..result import FeedEntry, FeedResult


class RssEntries(FeedResult):
    def __init__(self, result, json, entries, request_etag=None):
        url = result.href

        feed = result.feed

        title = feed.title
        description = feed.title_detail.value
        entries = entries

        updated = _result_publication(result, entries)

        super(RssEntries, self).__init__(url, title, description, updated, json, entries)
        self._feed = result

        self.request_etag = request_etag
        self.etag = result.etag

    def is_for_unread_entries(self):
        return bool(self.request_etag)


def _result_publication(feed_result, entries):
    try:
        publication_date = utc.from_timestamp(feed_result.feed.published_parsed)
    except AttributeError:
        publication_date = max([entry.publication for entry in entries])

    return publication_date


class FeedParserEntries(RssEntries):

    def __init__(self, result, json, request_etag=None):
        entries, broken = _partition_valid_broken_entries(result.entries)
        super(FeedParserEntries, self).__init__(result, json, entries, request_etag)
        self.broken_entries = broken


class RssResult(FeedParserEntries):

    def __init__(self, result, request_etag=None):
        super(RssResult, self).__init__(result, feed_to_json(result), request_etag)


class JsonRssResult(FeedParserEntries):

    def __init__(self, json, request_etag=None):
        super(JsonRssResult, self).__init__(json_to_feed(json), json, request_etag)


class FeedParserEntry(FeedEntry):
    def __init__(self, entry):
        publication = utc.from_timestamp(entry.published_parsed)
        entry_json = feed_to_json(entry)

        super(FeedParserEntry, self).__init__(entry.link, entry.title, publication, entry.summary, entry_json)


def _partition_valid_broken_entries(entries):
    valid, broken = [], []
    page_entries = (entry for entry in entries if entry.link)

    for entry in page_entries:
        feed_entry = _feed_entry(entry)

        if feed_entry:
            valid.append(feed_entry)
        else:
            broken.append(entry)

    return valid, broken


def _feed_entry(entry):
    try:
        return FeedParserEntry(entry)
    except AttributeError, e:
        print_err_trace(e)
        pass


class RssErrorResult(RssResult):
    def __init__(self, result, error, etag):
        super(RssErrorResult, self).__init__(result, etag)
        self.error = error


class FeedUnchanged(object):
    def __init__(self, url, result, etag):
        self.url = url
        self.result = result
        self.entries = []
        self.request_etag = etag

    def is_for_unread_entries(self):
        return True

    def __str__(self):
        return 'Feed unchanged: %s' % self.url