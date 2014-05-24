import sys

import web

from feedstory.rss.result import JsonRssResult


urls = ('/cache/feed', 'FeedCacheService',
        '/cache/feed/entry', 'FeedEntryCacheService')


app = web.application(urls, globals())


class FeedCacheService(object):

    def GET(self):
        user_data = web.input()
        feed_cache = caches.get_cache(**user_data)

        json = feed_cache.get_last_feed_json(user_data.url)
        return json if json else ''

    def POST(self):
        user_data = web.input(_unicode=False)

        feed_cache = caches.get_cache(**user_data)

        result = JsonRssResult(user_data.json, request_etag=user_data.get('etag'))
        feed_cache.add_feed_result(result)


def serve(feed_caches, port=8088):
    global caches
    caches = feed_caches

    sys.argv = ['localhost']
    sys.argv.append(str(port))
    app.run()

    #After Keyboard Interrupt
    print 'Closing Caches'
    caches.close()