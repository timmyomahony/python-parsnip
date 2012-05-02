import os
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='python-parsnip',
    version="0.0.1",
    description='Parsnip is a basic python interface to allow the sending of web texts via the main 4 Irish mobile operators websites. It is influenced by/based on Cabbage http://cabbagetexter.com/.',
    long_description=readme,
    author="Timmy O'Mahony",
    author_email='me@timmyomahony.com',
    url='https://github.com/timmyomahony/python-parsnip',
    install_requires=[
      'lxml', 
      'BeautifulSoup', 
    ],
    packages=['parsnip', 'parsnip.operators'], 
)
