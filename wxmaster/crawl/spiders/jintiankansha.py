#!/usr/bin/env python
# encoding: utf-8

"""
@description: "http://www.jintiankansha.me" 网站的全站爬虫，获取需要关注的公众号信息

@author: BaoQiang
@time: 2017/6/9 15:51
"""

"""
http://www.jintiankansha.me/api/topics?page=3&time=1496995128067
http://www.jintiankansha.me/api/topics/w2y6jDXTLK?page=2&time=1496995182859
"""

import scrapy
from scrapy.http import FormRequest
import time
import json
from wxmaster.pth import FILE_PATH

root_url = 'http://www.jintiankansha.me'

out_file = '{}/kansha/content.json'.format(FILE_PATH)


class Kansha(scrapy.Spider):
    name = 'kansha_spider'

    start_urls = [root_url]
    allow_domains = ['www.jintiankansha.me']

    def parse(self, response):
        classes = response.selector.xpath(
            './/ul[contains(@class,"aside-list")]//li[contains(@class,"home")] | .//ul[contains(@class,"aside-list")]//div[contains(@class,"wchannel-item")]')
        for item in classes:
            url = item.xpath('.//a/@href')[0].extract().strip()
            cate = item.xpath('.//span//text()')[0].extract().strip()

            url = url.replace('/welcome', '')
            yield FormRequest(url_fmt.format(url, 1, get_time()), meta={'url': url, 'current_pg': 0, 'cate': cate},
                              callback=self.parse_cate)

            # print(len(classes))
            # break

    def parse_cate(self, response):
        json_data = json.loads(response.body.decode())

        next_pg = response.meta['current_pg'] + 1
        url = response.meta['url']
        cate = response.meta['cate']

        # if json_data['data'] and next_pg < 3:
        if json_data['data']:
            json_data['url'] = response.url
            json_data['cate'] = cate

            with open(out_file, 'a', encoding='utf-8') as fw:
                json.dump(json_data, fw, ensure_ascii=False, sort_keys=True)
                fw.write('\n')

            yield FormRequest(url_fmt.format(url, next_pg, get_time()), meta={'url': url, 'current_pg': next_pg,'cate':cate},
                              callback=self.parse_cate)


url_fmt = 'http://www.jintiankansha.me/api/topics{}?page={}&time={}'


def get_time():
    return int(time.time() * 1000)


def main():
    print('do sth')


if __name__ == '__main__':
    main()
