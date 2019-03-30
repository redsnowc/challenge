# -*- coding: utf-8 -*-
import redis
import json
from scrapy.exceptions import DropItem


class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['summary'] = item['summary'].replace(
            ' ', '',).replace('\n', '').replace('\u3000', '')
        item['score'] = float(item['score'])
        if item['score'] >= 8.0:
            json_str = json.dumps(dict(item), ensure_ascii=False)
            self.r.lpush('douban_movie:items', json_str)
            return item
        else:
            raise DropItem('Drop %s' % item)

    def open_spider(self, spider):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
