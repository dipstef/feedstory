from unicoder import encoded


class FeedResult(object):

    def __init__(self, url, title, description, updated, json, entries):
        self.url = url
        self.title = title
        self.description = description

        self.updated = updated
        self.entries = entries
        self.json = json

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    def __str__(self):
        return repr(self.entries)


class FeedEntryPage(object):
    def __init__(self, url, title, publication):
        self.url = url
        self.title = title
        self.publication = publication

    def __str__(self):
        return encoded(unicode(self))

    def __unicode__(self):
        return u'%s (%s): %s' % (self.title, self.publication, self.url)


class FeedEntry(FeedEntryPage):

    def __init__(self, url, title, publication, summary, json):
        super(FeedEntry, self).__init__(url, title, publication)
        self.date = self.publication.date()
        self.summary = summary
        self.json = json