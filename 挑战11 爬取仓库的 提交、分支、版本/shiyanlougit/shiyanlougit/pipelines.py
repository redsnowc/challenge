# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlougit.model import Github, engine
from datetime import datetime


class ShiyanlougitPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
            item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            item['commits'] = int(item['commits'].strip().replace(',', ''))
        except AttributeError:
            item['commits'] = item['commits']

        try:
            item['branches'] = int(item['branches'].strip())
        except AttributeError:
            item['branches'] = item['branches']

        try:
            item['releases'] = int(item['releases'].strip())
        except AttributeError:
            item['releases'] = item['releases']

        self.session.add(Github(**item))

        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
