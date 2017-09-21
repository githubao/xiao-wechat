#!/usr/bin/env python
# encoding: utf-8

"""
@description: 蚂蚁宝卡

@author: pacman
@time: 2017/9/21 10:59
"""

import time
from scrapy import Request,Spider
import json
import re

re_pat = re.compile('jsonp_queryMoreNums\((.*)\);')

class MayiSpider(Spider):
    name = 'mayi_spider'

    def start_requests(self):
        requests = []

        current = int(time.time() * 1000)

        for i in range(10000):
            requests.append(Request(url_fmt.format(current+i)))

        return requests

    def parse(self, response):
        data = response.body.decode()
        results = []

        json_data = json.loads(trim(data))
        for idx,item in enumerate(json_data['numArray']):
            if idx % 12 == 0:
                results.append(item)

        with open('C:\\Users\\BaoQiang\\Desktop\\1.txt','a',encoding='utf-8') as fw:
            for item in results:
                fw.write('{}\n'.format(item))

def trim(res):
    m = re_pat.search(res)
    if m:
        return m.group(1)
    return None


url_fmt = 'http://m.10010.com/NumApp/NumberCenter/qryNum?callback=jsonp_queryMoreNums&provinceCode=11&cityCode=110&monthFeeLimit=0&groupKey=30242833&searchCategory=3&net=01&amounts=200&codeTypeCode=&searchValue=&qryType=02&goodsNet=4&_={}'

def tmp():
    print(time.time())

if __name__ == '__main__':
    tmp()