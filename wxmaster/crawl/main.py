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

def wxmp_spider():
    cmdline.execute('scrapy crawl wxmp_spider'.split())


def run():
    arg = int(sys.argv[1])
    spider_dic[arg]()


spider_dic = {
    1: wxapplet_spider,
    2: wxmp_spider,
}


def main():
    run()


if __name__ == '__main__':
    main()
