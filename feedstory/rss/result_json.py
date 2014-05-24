import json
import time

import feedparser
from dated.date_string import datetime_string, datetime_from_string
from dated import local, utc
from unicoder import decoded


def feed_to_json(feed, encoding):
    return decoded(json.dumps(feed, default=_feed_to_json, indent=4, encoding=encoding), encoding)


def _feed_to_json(obj):
    if isinstance(obj, time.struct_time):
        utc_datetime = utc.from_timestamp(obj)

        date_string = datetime_string(utc_datetime)

        time_dict = {'datetime': date_string}

        return time_dict
    elif isinstance(obj, BaseException):
        return {'error': obj.message}
    else:
        raise TypeError(repr(obj) + ' is not JSON serializable')


def json_to_feed(feed_json):
    return json.loads(feed_json, object_hook=_feed_dict)


def _feed_dict(d):
    if 'datetime' in d:
        inst = _utc_tuple_from_string(d['datetime'])
    elif isinstance(d, dict):
        inst = feedparser.FeedParserDict(d)
    else:
        inst = d
    return inst


def _utc_tuple_from_string(date_str):
    utc_time = local.to_utc(datetime_from_string(date_str))
    return utc_time.timetuple()