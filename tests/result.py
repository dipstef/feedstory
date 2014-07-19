from feedstory.rss.result_json import feed_to_json, json_to_feed
from feedstory.rss import _feed_parse


def main():
    url = 'http://rss.cnn.com/rss/edition_europe.rss'

    result = _feed_parse(url)
    json_result = feed_to_json(result)

    parsed = json_to_feed(json_result)

    assert result == parsed

if __name__ == '__main__':
    main()