# -*- coding: utf-8 -*-
import scrapy
from seiya.spider.items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = [
            'https://www.lagou.com/zhaopin/%s/' %(i) for i in range(1,31)]

    def parse(self, response):
        print(response.request.headers.get('User-Agent'))
        item = JobItem()
        for value in response.xpath(
                '//li[@class="con_list_item default_list"]'):
            item['title'] = value.css(
                'div.list_item_top h3::text').extract_first()
            city = value.css('span.add em::text').extract_first()
            if '·' in city:
                item['city'] = city.split('·')[0]
            else:
                item['city'] = city
            item['salary_lower'] = value.css(
                'span.money::text').re_first('(\d+)')
            item['salary_upper'] = value.css(
                'span.money::text').re_first('-(\d+)')
            experience_list = value.css('div.li_b_l::text').re('(\d+)')
            if len(experience_list) == 2:
                item['experience_lower'] = experience_list[0]
                item['experience_upper'] = experience_list[1]
            elif len(experience_list) == 1:
                item['experience_lower'] = 0
                item['experience_upper'] = experience_list[0]
            else:
                item['experience_lower'] = 0
                item['experience_upper'] = 0
            item['education'] = value.css(
                'div.li_b_l::text').re_first('/(.+)').strip()
            item['tags'] = ' '.join(value.css(
                    'div.list_item_bot div.li_b_l span::text').extract())
            item['company'] = value.css(
                'div.company_name a::text').extract_first()
            yield item

        
