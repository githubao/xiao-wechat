#!/usr/bin/env python
# encoding: utf-8

"""
@description: 京东店铺爬虫

@author: pacman
@time: 2017/9/5 16:01
"""

import scrapy
from scrapy import Request

# url_fmt = 'https://shop.m.jd.com/?shopId=100000127'
url_fmt = 'https://shop.m.jd.com/?shopId=1000{:5d}'

class JdShopSpider(scrapy.Spider):
    name = 'jdshop_spider'

    start_urls = ['https://shop.m.jd.com']

    def parse(self, response):
        for i in range(100000):
            yield Request(url_fmt.format(i),callback=self.parse_item)

    def parse_item(self, response):
        follow_cnt = response.selector.xpath('')




def main():
    print('do sth')


if __name__ == '__main__':
    main()