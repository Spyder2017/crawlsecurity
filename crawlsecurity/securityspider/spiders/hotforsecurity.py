# -*- coding: utf-8 -*-
import re,scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from securityspider.scrapy_bloom.ScrapyBloom import ScrapyBloom
from securityspider.items import SecurityItem

scr_blo = ScrapyBloom()

class HotforsecuritySpider(Spider):
    name = "hotforsecurity"
    allowed_domains = ["https://hotforsecurity.bitdefender.com/"]
    start_urls = ["https://hotforsecurity.bitdefender.com/"]

    def parse(self, response):
        num_pages = 284
        base_url = "https://hotforsecurity.bitdefender.com/page/{0}"
        for page in range(1, num_pages):
            yield scrapy.Request(base_url.format(page), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        sites = sel.xpath('//h2[contains(@class,"entry-title h3")]/a/@href').extract()
        for site in sites:
            # 使用布隆过滤器对网址进行筛选过滤
            iscon = scr_blo.isContain(site)
            if (iscon == True):
                continue
            else:
                scr_blo.insert(site)
                yield scrapy.Request(site, dont_filter=True, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.url)
        # p = re.compile('\\+u+\w{4}|\\t|\\n|\\r')
        p = re.compile("<[^>]+>|\t|\r|\n")

    #     The lines below is a spider contract. For more info see:
    #     http://doc.scrapy.org/en/latest/topics/contracts.html
    #
    #     @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
    #     @scrapes name
    #     """
    #
        # sel = Selector(response)
        items = []

        for site in response.xpath('//div[@class="col-lg-10 col-md-10 col-sm-10"]'):
            item = SecurityItem()
            item['author'] = ''
            item['title'] = site.xpath('header/h1//text()').extract_first().strip()
            item['title'] = p.sub("", item['title'])
            item['description'] = "".join(site.xpath('div[@class="entry-content herald-entry-content"]//p//text()').extract()).strip()
            item['description'] = p.sub("", item['description'])
            item['url'] = response.url
            item['keywords'] = ",".join(site.xpath('//div[@class="meta-tags"]//a//text()').extract()).strip()
            item['keywords'] = p.sub("", item['keywords'])
            item['datetime'] = site.xpath('//span[@class="updated"]/text()').extract_first().strip()
            item['datetime'] = p.sub("",item['datetime'])
            items.append(item)
    #
        return items
