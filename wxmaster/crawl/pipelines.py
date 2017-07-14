# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from wxmaster.db.mymongo import MyMongo


class WxSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class SogouMpPipeline:
    def __init__(self):
        self.mongo = MyMongo()

    def process_item(self, item, spider):
        self.mongo.set_one('test', 'sogoump', item)
