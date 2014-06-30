import quecco
from feedstory.remote.server import serve
from tests import FeedCaches


def main():
    caches = FeedCaches(quecco.threads)
    serve(caches, port=8088)


if __name__ == '__main__':
    main()