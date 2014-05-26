from distutils.core import setup

VERSION = '0.1'

desc = """Feed cache, enables to keep an history of the feed published entries through time"""

name = 'feedstory'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages=['feedstory', 'feedstory.cache', 'feedstory.cache.db', 'feedstory.remote', 'feedstory.rss'],
      platforms=['Any'],
      requires=['web.py', 'feedparser', 'quecco', 'urlo', 'httpy_client']
)
