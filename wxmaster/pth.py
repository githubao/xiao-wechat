#!/usr/bin/env python
# encoding: utf-8


"""
@description: //TODO 

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: pth.py
@time: 2016/11/1 18:17
"""

import logging
from os.path import dirname, abspath

ROOT_PATH = dirname(abspath(__file__)) + '/'

FILE_PATH = ROOT_PATH + 'file/'
LOG_PATH = ROOT_PATH + 'log/'

MY_PATH = None
LINUX_PATH = '/mnt/home/baoqiang/'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='{}/crawl.log'.format(LOG_PATH),
                    filemode='a'
                    )
