# -*- coding: utf-8 -*-
import re,scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider
from securityspider.scrapy_bloom.ScrapyBloom import ScrapyBloom
from securityspider.items import SecurityItem

scr_blo = ScrapyBloom()

class HexacornSpider(Spider):
    name = "hexacorn"
    allowed_domains = ["http://http://www.hexacorn.com"]
    start_urls = ["http://www.hexacorn.com/blog/"]

    def parse(self, response):
        num_pages = 162
        base_url = "http://www.hexacorn.com/blog/page/{0}"
        for page in range(1, num_pages):
            yield scrapy.Request(base_url.format(page), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        sites = sel.xpath('//h2[contains(@class,"posttitle")]/a/@href').extract()
        for site in sites:
            # print(site)
            # yield scrapy.Request(site,dont_filter=True,callback=self.parse_cto_info)
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

        for site in response.xpath('//div[@class="post-content"]'):
            item = SecurityItem()
            item['author']=''
            item['keywords'] = ''
            item['title'] = site.xpath('h2/a/text()').extract_first().strip()
            item['title'] = p.sub("", item['title'])
            item['description'] = "".join(site.xpath('div[@class="entry"]//p//text()').extract()).strip()
            item['description'] = p.sub("", item['description'])
            # item['description'] = item['description'].replace('/\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]/g', "")
            item['url'] = response.url
            item['datetime'] = item['url'][29:33] + "." + item['url'][34:36] + "." + item['url'][37:39]
            items.append(item)
    #
        return items
