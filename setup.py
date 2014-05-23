from distutils.core import setup

VERSION = '0.1'

desc = """Sqlite response cache for httpy. Used together with an httpy_client will retrieve cached responses or
 store responses from the client."""

name = 'catechu'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['catechu.http', 'catechu.zeromq'],
      platforms=['Any'],
      requires=['web.py', 'feedparser', 'httpy']
)