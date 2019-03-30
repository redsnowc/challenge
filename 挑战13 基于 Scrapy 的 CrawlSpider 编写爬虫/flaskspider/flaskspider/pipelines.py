# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import redis


def rpl(value):
    rp = value.group()
    if '¶' in rp:
        return '¶\n'
    elif '.' in rp:
        return '.\n'
    else:
        return value.group()[0] + ' '


regex = re.compile(r'(.{1})\n+')


class FlaskspiderPipeline(object):
    def process_item(self, item, spider):
        item['text'] = regex.sub(rpl, item['text'])

        json_str = json.dumps(dict(item))
        self.redis.lpush('flask_doc:items', json_str)

        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
