import json
import time

import feedparser
from dated import utc
from unicoder import decoded
import cPickle as pickle


def feed_to_json(feed, encoding):
    return decoded(json.dumps(feed, default=_feed_to_json, indent=4, encoding=encoding), encoding)


def _feed_to_json(obj):
    if isinstance(obj, time.struct_time):
        utc_datetime = utc.from_time_tuple(obj)

        time_dict = {'datetime': utc_datetime.to_string()}

        return time_dict
    elif isinstance(obj, BaseException):
        return {'error': pickle.dumps(obj)}
    else:
        raise TypeError(repr(obj) + ' is not JSON serializable')


def json_to_feed(feed_json):
    return json.loads(feed_json, object_hook=_feed_dict)


def _feed_dict(d):
    if 'datetime' in d:
        utc_time = utc.from_string(d['datetime'])
        inst = utc_time.timetuple()
    elif 'error' in d:
        inst = pickle.loads(d['error'])
    elif isinstance(d, dict):
        inst = feedparser.FeedParserDict(d)
    else:
        inst = d
    return inst