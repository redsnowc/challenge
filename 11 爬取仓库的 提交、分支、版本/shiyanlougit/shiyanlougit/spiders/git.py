# -*- coding: utf-8 -*-
import scrapy
from shiyanlougit.items import ShiyanlougitItem


class GitSpider(scrapy.Spider):
    name = 'git'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for value in response.css('li.col-12'):
            item = ShiyanlougitItem()
            # get name
            item['name'] = value.css(
                'div.d-inline-block.mb-1 a::text').extract_first().strip()
            # get update time
            item['update_time'] = value.css(
                'relative-time::attr(datetime)').extract_first()
            # get url
            git_url = response.urljoin(
                value.css(
                    'div.d-inline-block.mb-1 a::attr(href)').extract_first())

            request = scrapy.Request(git_url, callback=self.parse_others)

            request.meta['item'] = item
            yield request

        url = response.xpath(
            '//div[@class="BtnGroup"]/a/@href').extract()[-1]
        yield response.follow(url, callback=self.parse)

    def parse_others(self, response):

        item = response.meta['item']

        item['commits'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]//li[1]//span[@class="num text-emphasized"]/text()').extract_first()
        item['branches'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]//li[2]//span[@class="num text-emphasized"]/text()').extract_first()
        item['releases'] = response.xpath(
            '//div[@class="stats-switcher-wrapper"]//li[3]//span[@class="num text-emphasized"]/text()').extract_first()

        yield item
