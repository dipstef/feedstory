from feedstory import parse_feed_result


def main():
    url = 'http://www.repubblica.it/rss/homepage/rss2.0.xml'

    result = parse_feed_result(url)
    assert result.entries
    assert not result.is_for_unread_entries()
    result = parse_feed_result(url, result.etag)
    assert not result.entries
    assert result.is_for_unread_entries()

if __name__ == '__main__':
    main()