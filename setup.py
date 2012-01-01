import os
from setuptools import setup, find_packages

from parsnip import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='python-parsnip',
    version=".".join(map(str, VERSION)),
    description='Parsnip is a basic python interface to allow the sending of web texts via the main 4 Irish mobile operators websites. It is influenced by/based on Cabbage http://cabbagetexter.com/.',
    long_description=readme,
    author="Timmy O'Mahony",
    author_email='timmy@pastylegs.com',
    url='https://github.com/pastylegs/python-parsnip',
    packages=find_packages(),
    package_data = {
        'parsnip': [
        ],
    },
)