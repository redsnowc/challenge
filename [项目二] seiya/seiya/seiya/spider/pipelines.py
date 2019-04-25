# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from seiya.db.job import session, Job


class SeiyaPipeline(object):
    def process_item(self, item, spider):
        item['salary_lower'] = int(item['salary_lower'])
        item['salary_upper'] = int(item['salary_upper'])
        item['experience_lower'] = int(item['experience_lower'])
        item['experience_upper'] = int(item['experience_upper'])

        session.add(Job(**item))
        return item

    def close_spider(self, spider):
        session.commit()
        session.close()

