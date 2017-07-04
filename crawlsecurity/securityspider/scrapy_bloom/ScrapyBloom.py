import scrapy
import urlparse
from hashlib import md5
from pybloomfilter import BloomFilter

bf = BloomFilter(capacity=1000000, error_rate=0.01)

class ScrapyBloom(object):

    def isContain(self, url_str):
        m5 = md5()
        m5.update(url_str)
        url_str = m5.hexdigest()
        if url_str in bf:
            return True
        else:
            return False

    def insert(self,url_str):
        bf.add(url_str)