from quelo.query import get_results, get_value, execute


def insert_feed(c, url, title, description):
    execute(c, '''insert into feed (url, title, description)
                    values(?,?,?) ''', (url, title, description))


def get_feed_id(cursor, url):
    return get_value(cursor, '''select id
                                  from feed
                                 where url = ? ''', (url, ))


def get_latest_entries(c, result_url):
    return get_results(c, '''select url,
                                    title,
                                    published
                               from feed_result_last_item
                              where result_url = ? ''', (result_url, ))


def get_latest_feed(c, feed_url):
    return get_value(c, '''select rr.data

                             from rss_result rr,
                                  feed_result_last frl

                            where frl.feed_result_id = rr.feed_result_id
                              and rr.result_url = ? ''', (feed_url, ))


def get_feed_result_location_id(c, feed_id, result_url):
    return get_value(c, '''select id
                             from feed_result_location
                            where feed_id = ?
                              and url = ? ''', (feed_id, result_url))


def insert_feed_result_location(c, feed_id, result_url):
    execute(c, '''insert into feed_result_location(feed_id, url)
                         values(?, ?)''', (feed_id, result_url))


def insert_feed_result(c, result_id, published, updated, data):
    execute(c, '''insert into feed_result(result_id, published, updated, data)
                    values(?,?,?,?)''', (result_id, published, updated, data))


def get_feed_result_id(c, result_id, published):
    return get_value(c, '''select id
                             from feed_result
                            where result_id = ?
                              and published = ?''', (result_id, published))


def update_feed_result(cursor, feed_result_id, updated, json):
    return execute(cursor, '''update feed_result
                                 set updated = ?,
                                     data = ?
                               where id = ? ''', (updated, json, feed_result_id))


def insert_rss_feed_result(c, feed_result_id):
    execute(c, '''insert into rss_feed_result(feed_result_id)
                    values(?)''', (feed_result_id, ))


def insert_feed_result_unread(c, feed_result_id):
    execute(c, '''insert into feed_result_unread(feed_result_id)
                    values(?)''', (feed_result_id, ))


def insert_feed_result_entry(c, feed_result_id, feed_entry_id):
    execute(c, '''insert into feed_result_entry(feed_result_id, feed_entry_id)
                    values(?,?)''', (feed_result_id, feed_entry_id))


def get_feed_result_entry_id(c, feed_result_id, feed_entry_id):
    return get_value(c, '''select id
                             from feed_result_entry
                            where feed_result_id = ?
                              and feed_entry_id = ?''', (feed_result_id, feed_entry_id))