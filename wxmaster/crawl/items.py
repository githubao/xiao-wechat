# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json


class DuoKanItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)


class WeRankItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)


class WxMpItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)


class WxSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MpAnyvItem(dict):
    def __str__(self):
        return json.dumps(self, ensure_ascii=False, sort_keys=True)
