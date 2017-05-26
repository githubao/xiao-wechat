#!/usr/bin/env python
# encoding: utf-8

"""
@description: user agent 代理

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: useragent.py
@time: 2017/1/19 16:01
"""

import random


class UserAgentMiddleware():
    def __init__(self, user_agent_pool):
        self.user_agent_pool = user_agent_pool

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings.get('USER_AGENT_POOL', None))
        return obj

    def process_request(self, request, spider):
        if self.user_agent_pool:
            random_user_agent = random.choice(self.user_agent_pool)
            request.headers['User-Agent'] = random_user_agent
