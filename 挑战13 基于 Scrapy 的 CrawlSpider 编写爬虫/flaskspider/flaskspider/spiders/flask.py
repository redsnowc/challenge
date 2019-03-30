# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flaskspider.items import FlaskspiderItem


class FlaskSpider(CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']

    link = LinkExtractor(
        allow=('http://flask.pocoo.org/docs/1.0/.*'))
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = FlaskspiderItem()
        item['url'] = response.url
        item['text'] = ' '.join(response.xpath(
            '//div[@class="section"]//text()').extract())
        yield item
