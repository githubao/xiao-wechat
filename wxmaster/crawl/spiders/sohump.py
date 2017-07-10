#!/usr/bin/env python
# encoding: utf-8

"""
@description: 搜狐公众号爬虫

@author: BaoQiang
@time: 2017/7/10 14:27
"""

import time
import scrapy
from scrapy import Request
import json
from wxmaster.pth import FILE_PATH
from wxmaster.crawl.items import SohuMpItem
import re

output_file = '{}/sohump.json'.format(FILE_PATH)
output2_file = '{}/sohump_new.json'.format(FILE_PATH)

url_fmt = 'http://mp.sohu.com/apiV2/profile/newsListAjax?xpt=c2h1b2JvMTAwQHNvaHUuY29t&pageNumber={}&pageSize=10&categoryId=&_={}'


class SohuMpSpider(scrapy.Spider):
    name = 'sohump_spider'

    def start_requests(self):
        time_stmp = int(time.time() * 1000)
        return [Request(url_fmt.format(i, time_stmp + (i - 1)), callback=self.parse_list) for i in range(1, 120)]
        # return [Request(url_fmt.format(i, int(time.time() * 1000)), callback=self.parse_list) for i in range(1, 2)]

    def parse_list(self, response):
        json_data = json.loads(response.body.decode().replace('\\"', '"')[1:-1])

        for item in json_data['data']:
            url = item['url']
            yield Request('http:{}'.format(url), callback=self.parse_item)

    def parse_item(self, response):
        title = ''.join([i.extract().strip() for i in response.selector.xpath('//h1//text()')])
        if '妹子篇' in title:
            sohump = SohuMpItem()
            sohump['url'] = response.url
            sohump['title'] = title

            with open(output_file, 'a', encoding='utf-8') as fw:
                fw.write('{}\n'.format(sohump))


def main():
    # print(time.time())

    s = '{"a":1}'
    json_data = json.loads(s)
    print(json_data['a'])


def main2():
    title_pat = re.compile('【硕博联谊】妹子篇（第([\d]+)期）')
    lst = []
    with open(output_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            json_data = json.loads(line)

            m = title_pat.search(json_data['title'])
            lst.append({'id': m.group(1), 'url': json_data['url']})

    with open(output2_file, 'w', encoding='utf-8') as fw:
        # json.dump(lst, fw, sort_keys=True, ensure_ascii=False)
        for item in lst:
            fw.write('{}\t{}\n'.format(item['id'],item['url']))


if __name__ == '__main__':
    main2()
