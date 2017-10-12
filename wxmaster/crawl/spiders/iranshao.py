#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爱燃烧，马拉松赛事

@author: pacman
@time: 2017/9/27 16:11
"""

import time
from scrapy import Request, Spider


class IranshaoSpider(Spider):
    name = 'iranshao_spider'

    def start_requests(self):
        return [Request(url_fmt.format(i)) for i in range(1, 11)]

    def parse(self, response):
        results = []

        classes = response.selector.xpath('.//div[contains(@class,"race-search-item")]')

        for item in classes:
            a_url = item.xpath('.//div[@class="itemname"]//a')
            url = a_url.xpath('.//@href')[0].extract().strip()
            url = 'http://iranshao.com{}'.format(url)

            name = a_url.xpath('.//text()')[0].extract().strip()

            cnt = 0
            cnt_items = item.xpath('.//div[@class="attr"]//text()')
            for cnt_item in cnt_items:
                text = cnt_item.extract().strip()
                if '人关注' in text:
                    cnt = int(text.replace('人关注', '').strip())
                    break

            results.append('{}\t{}\t{}'.format(url, name, cnt))

        with open('C:\\Users\\BaoQiang\\Desktop\\1.txt', 'a', encoding='utf-8') as fw:
            for item in results:
                fw.write('{}\n'.format(item))


url_fmt = 'http://iranshao.com/bundled_races?page={}&sort=hot'


def tmp():
    print(time.time())


if __name__ == '__main__':
    tmp()
