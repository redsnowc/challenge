# -*- coding: utf-8 -*-
import scrapy


class GitSpider(scrapy.Spider):
    '''使用 'scrapy runspider git.py -o xxx.json' 运行'''
    name = 'git'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for value in response.css('li.col-12'):
            yield{
                'name': value.css(
                    'div.d-inline-block.mb-1 a::text'
                ).extract_first().strip(),
                'update_time': value.css(
                    'relative-time::attr(datetime)').extract_first()
            }

        for url in response.xpath(
                '//a[contains(@class, "btn-outline")]/@href').extract():
            if 'after' in url:
                yield scrapy.Request(url, callback=self.parse)
