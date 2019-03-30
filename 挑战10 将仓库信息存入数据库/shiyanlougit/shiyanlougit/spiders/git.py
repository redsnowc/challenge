# -*- coding: utf-8 -*-
import scrapy
from shiyanlougit.items import ShiyanlougitItem


class GitSpider(scrapy.Spider):
    name = 'git'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        item = ShiyanlougitItem()
        for value in response.css('li.col-12'):
            item['name'] = value.css(
                'div.d-inline-block.mb-1 a::text'
            ).extract_first().strip(),
            item['update_time'] = value.css(
                'relative-time::attr(datetime)').extract_first()

            yield item

        for url in response.xpath(
                '//a[contains(@class, "btn-outline")]/@href').extract():
            if 'after' in url:
                yield scrapy.Request(url, callback=self.parse)
