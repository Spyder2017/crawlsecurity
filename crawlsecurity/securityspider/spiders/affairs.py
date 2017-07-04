# -*- coding: utf-8 -*-
import re,scrapy,datetime
from scrapy.selector import Selector
from scrapy.spiders import Spider
from securityspider.scrapy_bloom.ScrapyBloom import ScrapyBloom
from securityspider.items import SecurityItem

scr_blo = ScrapyBloom()

class HexacornSpider(Spider):
    name = "securityaffairs"
    allowed_domains = ["http://securityaffairs.co/wordpress/"]
    start_urls = ["http://securityaffairs.co/wordpress/"]

    def parse(self, response):
        num_pages = 497
        base_url = "http://securityaffairs.co/wordpress/page/{0}"
        for page in range(1, num_pages):
            yield scrapy.Request(base_url.format(page), dont_filter=True, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[contains(@class,"post_header single_post")]/h3/a/@href').extract()
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

        # sel = Selector(response)
        items = []

        for site in response.xpath('//div[@class="sidebar_content"]'):
            item = SecurityItem()
            item['title'] = site.xpath("//div[@class='post_header_wrapper']/h1/text()").extract_first().strip()
            item['title'] = p.sub("", item['title'])
            item['keywords'] = p.sub("", ",".join(site.xpath("//div[@class='post_tag']//a//text()").extract())).strip()
            item['datetime'] = site.xpath("//div[@class='post_detail']/text()").extract_first().strip()
            item['datetime'] = p.sub("",item['datetime'][:-3])
            item['author'] = p.sub("", site.xpath("//div[@class='post_detail']/a/text()").extract_first()).strip()
            item['url'] = response.url
            item['description'] = p.sub("", "".join(site.xpath("//div[@class='post_inner_wrapper']/p//text() | //div[@class='post_inner_wrapper']//h2/text()").extract())).strip()
            items.append(item)
    #
        return items
