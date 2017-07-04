# -*- coding: utf-8 -*-
import re,scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from securityspider.scrapy_bloom.ScrapyBloom import ScrapyBloom
from securityspider.items import SecurityItem

scr_blo = ScrapyBloom()

class KrebsonsecuritySpider(Spider):
    name = "krebsonsecurity"
    allowed_domains = ["https://krebsonsecurity.com"]
    start_urls = ["https://krebsonsecurity.com"]

    def parse(self, response):
        num_pages = 141
        base_url = "https://krebsonsecurity.com/page/{0}"
        for page in range(1, num_pages):
            yield scrapy.Request(base_url.format(page), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        sites = sel.xpath('//h2[contains(@class,"post-title")]/a/@href').extract()
        for site in sites:
            # print(site)
            # yield scrapy.Request(site,dont_filter=True,callback=self.parse_cto_info)
            iscon = scr_blo.isContain(site)
            if(iscon == True):
                continue
            else:
                scr_blo.insert(site)
                yield scrapy.Request(site, dont_filter=True, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.url)
        p = re.compile('\\+u+\w{4}|\\t|\\n|\\r')

    #     The lines below is a spider contract. For more info see:
    #     http://doc.scrapy.org/en/latest/topics/contracts.html
    #
    #     @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
    #     @scrapes name
    #     """
    #
        # sel = Selector(response)
        items = []

        for site in response.xpath('//div[@class="post-smallerfont"]'):
            item = SecurityItem()
            item['author'] = ''
            item['keywords'] = ''
            item['title'] = site.xpath('h2/text()').extract_first().strip()
            item['title'] = p.sub("", item['title'])
            item['description'] = "".join(site.xpath('div//p//text()').extract()).strip()
            item['description'] = p.sub("", item['description'])
            item['url'] = response.url
            item['datetime'] = site.xpath('small/span[@class="date"]/text()').extract_first().strip()
            item['datetime'] = item['url'][28:32] + "." + item['url'][33:35] + "." + item['datetime']
            # item['title'] = re.sub(r'\\+u+\w{4}|\\t|\\n|\\r',"",site.xpath('h2/text()').extract_first()).strip()
            # item['description'] = re.sub(r'\\+u+\w{4}|\\t|\\n|\\r',"",''.join(site.xpath('div//p//text()').extract())).strip()
            items.append(item)
    #
        return items
