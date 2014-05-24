import sys
import web


urls = ('/cache/feed', 'FeedCacheService',
        '/cache/feed/entry', 'FeedEntryCacheService')


app = web.application(urls, globals())


class FeedCacheService(object):

    def GET(self):
        user_data = web.input()
        feed_cache = caches.get_cache(**user_data)

        result = feed_cache.get_last_result(user_data.url)
        return result.json if result else ''

    def POST(self):
        user_data = web.input()
        feed_cache = caches.get_cache(**user_data)
        user_data = web.input()
        feed_cache.add_feed_result(user_data.feed)


def serve(feed_caches, port=8088):
    global caches
    caches = feed_caches

    sys.argv = ['localhost']
    sys.argv.append(str(port))
    app.run()

    #After Keyboard Interrupt
    print 'Closing Caches'
    caches.close()