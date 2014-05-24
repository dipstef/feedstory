from quelo.query import execute, get_value, get_row


def insert_feed_entry(c, feed_id, url, title, summary, publication, data):
    execute(c, '''insert into feed_entry(feed_id, url, title, summary, published, data)
                    values(?,?,?,?,?,?) ''', (feed_id, url, title, summary, publication, data))


def get_feed_entry_id(c, feed_id, url):
    return get_value(c, '''select id
                            from feed_entry
                           where feed_id = ?
                             and url = ? ''', (feed_id, url))


def get_feed_entry(c, url):
    return get_row(c, '''select title,
                                published
                           from feed_entry
                          where url = ? ''', (url, ))