# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from shiyanlou.items import ShiyanlouItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091']

    link = LinkExtractor(
        allow=r'/subject/\d+/',
        restrict_css='div#recommendations'
    )

    rules = (Rule(link, callback='parse_item', follow=True),)

    def parse_item(self, response):
        print(response.request.headers.get('User-Agent'))
        item = ShiyanlouItem()
        item['url'] = response.url
        item['name'] = response.xpath(
            '//span[@property="v:itemreviewed"]/text()').extract_first()

        summary_all = response.xpath(
            '//span[@class="all hidden"]/text()').extract_first()
        if summary_all != None:
            item['summary'] = ''.join(
                response.xpath(
                    '//span[@class="all hidden"]/text()').extract())
        else:
            item['summary'] = ''.join(
                response.xpath(
                    '//span[@property="v:summary"]/text()').extract())

        item['score'] = response.css(
            'strong.ll.rating_num::text').extract_first()
        yield item
