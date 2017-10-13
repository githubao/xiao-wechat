#!/usr/bin/env python
# encoding: utf-8

"""
@description: ip代理

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: httpproxy.py
@time: 2017/1/19 16:10
"""

import random
from urllib.parse import urlparse
from collections import defaultdict

import time
import os
import requests
import json
from wxmaster.pth import logging

# max_time = 600
max_time = 3000


class HttpProxyMiddleware():
    def __init__(self, proxies, https=False):
        self.proxies = defaultdict(lambda: [])

        self.https = https
        self.scheme = 'http'

        for proxy in proxies:
            self.proxies['http'].append('{}://{}'.format(self.scheme, proxy))
            self.proxies['https'].append('{}://{}'.format(self.scheme, proxy))

        self.start = time.time()

    @classmethod
    def from_crawler(cls, crawler):
        https = crawler.settings.get('USE_HTTPS_PROXIES')

        # return cls(crawler.settings.get('RANDOM_PROXIES'))
        return cls(get_proxy(https), https)

    def process_request(self, request, spider):
        # if 'proxy' in request.meta:
        #     return

        self.check_expire()

        scheme = urlparse(request.url).scheme
        if self.proxies[scheme]:
            proxy = random.choice(self.proxies[scheme])
            logging.info('pid [{}]: request {} using proxy: {}'.format(os.getpid(), request.url, proxy))
            request.meta['proxy'] = proxy

    def check_expire(self):
        end = time.time()
        if (end - self.start) > max_time:
            self.start = end
            self.update_proxy()

    def update_proxy(self):
        proxies = get_proxy(self.https)
        if not proxies:
            return

        logging.error('UPDATING PROXIES LEN: {}'.format(len(proxies)))
        logging.error('NOW AVAILABLE PROXIES: {}'.format(proxies))

        self.proxies = defaultdict(lambda: [])
        for proxy in proxies:
            self.proxies['http'].append('{}://{}'.format(self.scheme, proxy))
            self.proxies['https'].append('{}://{}'.format(self.scheme, proxy))


def get_proxy(https=False):
    if https:
        proxy_str = requests.get('http://192.168.10.195:5000/get_all_https/').content.decode()
    else:
        proxy_str = requests.get('http://192.168.10.195:5000/get_all/').content.decode()
    return json.loads(proxy_str)

class HttpProxyWallMiddleware():
    def __init__(self, proxies):
        self.proxies = defaultdict(lambda: [])

        for proxy in proxies:
            self.proxies['http'].append('http://{}'.format(proxy))
            self.proxies['https'].append('http://{}'.format(proxy))

    @classmethod
    def from_crawler(cls, crawler):
        # return cls(crawler.settings.get('RANDOM_PROXIES'))
        return cls(['127.0.0.1:8123'])

    def process_request(self, request, spider):
        scheme = urlparse(request.url).scheme
        if self.proxies[scheme]:
            proxy = random.choice(self.proxies[scheme])
            logging.info('request {} using proxy: {}'.format(request.url, proxy))
            request.meta['proxy'] = proxy

def main():
    pass


if __name__ == '__main__':
    main()
