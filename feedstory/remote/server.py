import inspect

from bottle import Bottle, BaseRequest, request

from ..rss.result import JsonRssResult

app = Bottle()


@app.get('/cache/feed')
def get_response(caches):
    cache = caches.get_cache(**request.query)

    json = cache.get_last_feed_json(request.query['url'])
    return json if json else ''


@app.post('/cache/feed')
def save_response(caches):
    cache = caches.get_cache(**request.query)

    result = JsonRssResult(request.query['json'], request_etag=request.query.get('etag'))
    cache.add_feed_result(result)


class BottlePlugin(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def apply(self, callback, context):
        """Return a decorated route callback."""
        args = inspect.getargspec(context['callback'])[0]
        # Skip this callback if we don't need to do anything

        keywords = {k: v for k, v in self._kwargs.iteritems() if k in args}

        if not keywords:
            return callback

        def wrapper(*a, **ka):
            ka.update(keywords)
            rv = callback(*a, **ka)
            return rv

        return wrapper

    def __str__(self):
        components = '\n'.join(('{component} (keyword={keyword})'.format(component=component,
                                                                         keyword=keyword)
                                for keyword, component in self._kwargs.iteritems()))

        return '{klass} using:\n{components})'.format(klass=self.__class__.__name__,
                                                      components=components)

    def __repr__(self):
        return str(self)


class CachesPlugin(BottlePlugin):
    def __init__(self, caches, keyword='caches'):
        """ :param keyword: """
        super(CachesPlugin, self).__init__(**{keyword: caches})
        self._caches = caches

    def close(self):
        print 'Closing Caches'
        self._caches.close()


def serve(feed_caches, port=8088, body_max_mb=100):
    BaseRequest.MEMFILE_MAX = body_max_mb * 2 ** 20

    plugin = CachesPlugin(feed_caches)
    app.install(plugin)

    app.run(port=port)
