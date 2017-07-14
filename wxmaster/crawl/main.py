#!/usr/bin/env python
# encoding: utf-8

"""
@description: 启动爬虫

@author: BaoQiang
@time: 2017/5/8 10:50
"""

from scrapy import cmdline
import sys


def wxapplet_spider():
    cmdline.execute('scrapy crawl wxapplet_spider'.split())


def sogoump_spider():
    cmdline.execute('scrapy crawl sogoump_spider'.split())


def kansha_spider():
    cmdline.execute('scrapy crawl kansha_spider'.split())


def mpanyv_spider():
    cmdline.execute('scrapy crawl mpanyv_spider'.split())


def werank_spider():
    cmdline.execute('scrapy crawl werank_spider'.split())


def werank2_spider():
    cmdline.execute('scrapy crawl werank2_spider'.split())


def duokan_spider():
    cmdline.execute('scrapy crawl duokan_spider'.split())

def sohump_spider():
    cmdline.execute('scrapy crawl sohump_spider'.split())


def run():
    arg = int(sys.argv[1])
    spider_dic[arg]()


spider_dic = {
    1: wxapplet_spider,
    2: sogoump_spider,
    3: kansha_spider,
    4: mpanyv_spider,
    5: werank_spider,
    6: werank2_spider,
    7: duokan_spider,
    8: sohump_spider,
}


def main():
    run()


if __name__ == '__main__':
    main()
