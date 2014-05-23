from dated import utc

from .result_json import feed_to_json, json_to_feed
from feedstory.result import FeedEntry, FeedResult


class RssEntries(FeedResult):
    def __init__(self, result, json, entries):
        url = result.href

        feed = result.feed

        title = feed.title
        description = feed.title_detail.value
        entries = entries

        updated = _result_publication(result, entries)

        super(RssEntries, self).__init__(url, title, description, updated, json, entries)
        self._feed = result
        self.etag = result.etag


class RssResult(RssEntries):
    def __init__(self, result):
        json = feed_to_json(result)
        entries = _filter_valid_entries(result.entries)

        super(RssResult, self).__init__(result, json, entries)


def _result_publication(feed_result, entries):
    try:
        publication_date = utc.timestamp_to_utc(feed_result.feed.published_parsed)
    except AttributeError:
        publication_date = max([entry.publication for entry in entries])

    return publication_date


class JsonRssResult(RssEntries):
    def __init__(self, json):
        result = json_to_feed(json)
        entries = _filter_valid_entries(result.entries)

        super(JsonRssResult, self).__init__(result, json, entries)


class FeedParserEntry(FeedEntry):
    def __init__(self, entry):
        publication = utc.timestamp_to_utc(entry.published_parsed)
        entry_json = feed_to_json(entry)

        super(FeedParserEntry, self).__init__(entry.link, entry.title, publication, entry.summary, entry_json)


def _filter_valid_entries(entries):
    valid = []
    page_entries = (entry for entry in entries if entry.link)

    for entry in page_entries:
        entry = _valid_entry(entry)
        if entry:
            valid.append(entry)

    return valid


def _valid_entry(entry):
    try:
        return FeedParserEntry(entry)
    except AttributeError:
        pass


class RssErrorResult(RssResult):
    def __init__(self, result, error):
        super(RssErrorResult, self).__init__(result)
        self.error = error


class FeedUnchanged(object):
    def __init__(self, url, result):
        self.url = url
        self.result = result
        self.entries = []

    def __str__(self):
        return 'Feed unchanged: %s' % self.url