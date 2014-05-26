from distutils.core import setup
from setuptools import find_packages

VERSION = '0.1'

desc = """Feed cache, enables to keep an history of the feed published entries through time"""

name = 'feedstory'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages=find_packages(),
      platforms=['Any'],
      requires=['web.py', 'feedparser', 'quecco', 'urlo', 'httpy_client']
)
