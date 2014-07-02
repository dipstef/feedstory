from feedstory import FeedsStory
from feedstory.remote.client import FeedCacheClient


def main():
    url = 'http://www.repubblica.it/rss/homepage/rss2.0.xml'

    cache = FeedCacheClient(('127.0.0.1', 8088))

    feeds = FeedsStory(cache)

    result = feeds.add_entries(url)
    assert result.entries

    cache_result = cache.get_last_result(url)
    assert cache_result.etag == result.etag
    assert len(cache_result.entries) == len(result.entries)

    result = feeds.add_entries(url)
    assert len(result.entries) < len(cache_result.entries)


if __name__ == '__main__':
    main()