CREATE TABLE feed (
    id                                    integer not null primary key autoincrement,
    url                                   text not null,
    title                                 text not null,
    description                           text not null,
    unique(url)
);

CREATE TABLE feed_entry (
    id                                    integer not null primary key autoincrement,
    feed_id                               integer references feed(id) on delete cascade,
    url                                   text not null,
    title                                 text not null,
    summary                               text,
    published                             timestamp not null,
    data                                  text not null,
    unique(feed_id, url)
);

CREATE TABLE feed_result (
    id                                    integer not null primary key autoincrement,
    result_id                             integer references feed_result_location(id) on delete cascade,
    published                             timestamp not null,
    updated                               timestamp not null,
    data                                  text not null,
    unique(result_id, published)
);

CREATE TABLE feed_result_location (
    id                                    integer not null primary key autoincrement,
    feed_id                               integer references feed(id) on delete cascade,
    url                                   text not null,
    unique(feed_id, url)
);

CREATE TABLE feed_result_entry (
    id                                    integer not null primary key autoincrement,
    feed_result_id                        integer references feed_result(id) on delete cascade,
    feed_entry_id                         integer references feed_result_entry(id) on delete cascade,
    unique(feed_result_id, feed_entry_id)
);

CREATE TABLE feed_result_unread (
    feed_result_id                        integer primary key references feed_result(id) on delete cascade
);


CREATE TABLE rss_feed_result (
   feed_result_id                         integer primary key references feed_result(id) on delete cascade,
   request_etag                           text
);


CREATE VIEW feed_result_data AS

   select f.id as feed_id,
          f.url as feed_url,
          fr.result_id,
          rl.url as result_url,
          fr.id as feed_result_id,
          fr.published,
          fr.updated,
          fr.data
          

     from feed f,
          feed_result_location rl,
          feed_result fr

    where rl.id = fr.result_id
      and f.id = rl.feed_id;


CREATE VIEW feed_result_last AS

    select id as feed_result_id
      from feed_result
  group by result_id having max(published);


CREATE VIEW feed_entry_data AS

    select fr.feed_id,
           fr.feed_url,
           fr.result_id,
           fr.result_url,
           fre.feed_result_id,
           fr.published as result_published,
           fe.id as feed_entry_id,
           fe.url,
           fe.title,
           fe.summary,
           fe.published,
           fe.data

      from feed_result_data fr,
           feed_result_entry fre,
           feed_entry fe

     where fre.feed_result_id = fr.feed_result_id
        and fre.feed_entry_id = fe.id;


CREATE VIEW rss_entry AS

    select *
          
      from feed_entry_data

      where feed_result_id in (select feed_result_id
                                 from rss_feed_result);


CREATE VIEW rss_result AS
    
    select *
         
      from feed_result_data

     where feed_result_id in (select feed_result_id
                                from rss_feed_result);


CREATE VIEW rss_result_unread AS

    select *
      from rss_result
     where feed_result_id in (select feed_result_id
                                from feed_result_unread);




CREATE INDEX feed_result_location_url_idx ON feed_result_location(url);
CREATE INDEX feed_result_location_feed_id_idx ON feed_result_location(feed_id);

CREATE INDEX feed_result_published_idx ON feed_result(published);
CREATE INDEX feed_result_result_id_idx ON feed_result(result_id);
CREATE INDEX feed_result_updated_idx ON feed_result(updated);


CREATE INDEX feed_entry_feed_id_idx ON feed_entry(feed_id);
CREATE INDEX feed_entry_published_idx ON feed_entry(published);
CREATE INDEX feed_entry_title_idx ON feed_entry(title);
CREATE INDEX feed_entry_url_idx ON feed_entry(url);

CREATE INDEX feed_result_entry_feed_result_id_idx ON feed_result_entry (feed_result_id);
CREATE INDEX feed_result_entry_feed_entry_id_idx ON feed_result_entry (feed_entry_id);