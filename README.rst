Feedstory
=========

Feed cache

Features
========

history of the feed published entries through time as ``google reader``
support different formats, standard ``rss`` and in the past ``google reader``
Plans for ``feedly`` support

Usage
=====
a class returning cache instances for rss feed, for instance one cache for feed domain.

.. code-block:: python

    from feedstory import connect, FeedStory

    >>> feed_cache = connect('feed.db')
    >>> feed = FeedStory(feed_cache)

    >>> result = feed.add_entries('https://news.ycombinator.com/rss')

Entries are stored in the cache with the latest etag

.. code-block:: python

    >>> cache_result = feed_cache.get_last_result('https://news.ycombinator.com/rss')

    assert cache_result.etag == result.etag
    assert len(cache_result.entries) == len(result.entries)

    #given no entries have been published from the last call
    >>> result = feeds.add_entries('https://news.ycombinator.com/rss')
    assert not result.entries


History
=======

Recording the feed history

.. code-block:: python

    from feedstory import record_feed, iterate_history

    >>> feedstory.record_feed('https://news.ycombinator.com/rss')


Processing every newly published entry

.. code-block:: python

   for entries in feedstory.iterate_history('https://news.ycombinator.com/rss'):
    .....
