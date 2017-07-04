
from setuptools import setup, find_packages

setup(
    name='crawlsecurity',
    # version='1.0',
    # packages=find_packages(),
    entry_points={
        'scrapy.commands': [
            'crawlall=securityspider.commands:crawlall',
        ],
    },
)