#!/usr/bin/env python
# encoding: utf-8

"""
@description: 运行多线程，分布式任务

@author: BaoQiang
@time: 2017/5/8 13:53
"""

import multiprocessing
import time
from scrapy import cmdline
import sys
import os

def spider_run():
    spider_num = int(sys.argv[1])

    if spider_num == 1:
        cmdline.execute('scrapy crawl sogoump_spider'.split())

def spider_test():
    print('{}: hello'.format(os.getpid()))

def multi_run(process_num):
    pool = multiprocessing.Pool(process_num)
    for i in range(process_num):
        pool.apply_async(spider_run, ())

    pool.close()
    pool.join()


def main():
    process_num = int(sys.argv[2])

    multi_run(process_num)


if __name__ == '__main__':
    main()
