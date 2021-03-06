from feedstory import FeedsStory
from tests import caches


def main():
    url = 'http://www.repubblica.it/rss/homepage/rss2.0.xml'

    cache = caches.get_cache()

    try:
        feeds = FeedsStory(cache)

        result = feeds.add_entries(url)
        assert result.entries

        cache_result = cache.get_last_result(url)
        assert cache_result.etag == result.etag
        assert len(cache_result.entries) == len(result.entries)

        result = feeds.add_entries(url)
        assert len(result.entries) < len(cache_result.entries)

    finally:
        cache.close()

if __name__ == '__main__':
    main()