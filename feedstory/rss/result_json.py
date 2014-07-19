import json
import time

import feedparser
from dated import utc
from unicoder import to_unicode
import cPickle as pickle


def feed_to_json(feed, encoding='utf-8'):
    return to_unicode(json.dumps(feed, default=_feed_to_json, indent=4, encoding=encoding), encoding)


def _feed_to_json(obj):
    if isinstance(obj, time.struct_time):
        utc_datetime = utc.from_time_tuple(obj)
        return utc_datetime.to_string()
    elif isinstance(obj, BaseException):
        return {'error': pickle.dumps(obj)}
    else:
        raise TypeError(repr(obj) + ' is not JSON serializable')


def json_to_feed(feed_json):
    return json.loads(feed_json, object_hook=_feed_dict)


def _feed_dict(d):
    if isinstance(d, dict):
        for key, value in d.iteritems():
            #parsed time tuple
            if key.endswith('_parsed'):
                utc_time = utc.from_string(value)
                d[key] = utc_time.timetuple()
        inst = feedparser.FeedParserDict(d)
    elif 'error' in d:
        inst = pickle.loads(d['error'])
    else:
        inst = d
    return inst