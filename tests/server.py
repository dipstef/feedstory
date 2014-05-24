from quecco import scope
from feedstory.remote.server import serve
from tests import FeedCaches


def main():
    caches = FeedCaches(scope.threads)
    serve(caches, port=8088)


if __name__ == '__main__':
    main()