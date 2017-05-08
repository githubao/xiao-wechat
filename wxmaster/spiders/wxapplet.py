#!/usr/bin/env python
# encoding: utf-8

"""
@description: 小程序爬虫

@author: BaoQiang
@time: 2017/5/8 10:48
"""

import scrapy
from scrapy import Request


class WxAppletSpider(scrapy.Spider):
    name = 'wxapplet_spider'

    def start_requests(self):
        return [Request('https://wx.qq.com', callback=self.parse_item)]

    def parse_item(self, response):
        print(response.body.decode())


def main():
    print('do sth')


if __name__ == '__main__':
    main()
