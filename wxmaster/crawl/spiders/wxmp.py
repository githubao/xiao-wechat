#!/usr/bin/env python
# encoding: utf-8

"""
@description: 微信公众号爬虫

@author: BaoQiang
@time: 2017/5/26 16:07
"""

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from wxmaster.pth import FILE_PATH
from wxmaster.crawl.items import WxMpItem
import re
import time
import base64
import requests
import traceback
from datetime import datetime

num_pat = re.compile('[\d]+')

input_file = '{}/words.txt'.format(FILE_PATH)
out_file = '{}/sogoump.json'.format(FILE_PATH)


class SogouMpSpider(CrawlSpider):
    name = 'sogoump_spider'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls = get_search_words()

    rules = [
        Rule(LinkExtractor(allow=('/weixin.*query.*',)), callback='parse_item', follow=False,
             process_request='add_header')
    ]

    def add_header(self, request):
        request.replace(headers=get_headers())
        return request

    def parse_item(self, response):
        mp = WxMpItem()
        classes = response.selector.xpath('//ul[@class="news-list2"]/li')
        for item in classes:
            try:
                mp['name'] = ''.join([i.extract().strip() for i in item.xpath('.//p[@class="tit"]//text()')])
                mp['uid'] = item.xpath('.//p[@class="info"]/label/text()')[0].extract().strip()

                mp['month_cnt'] = ''.join([i.extract().strip() for i in item.xpath('.//p[@class="info"]/text()')])
                mp['month_cnt'] = trim_num(mp['month_cnt'])
                # mp['qrcode'] = item.xpath('.//div[@class="ew-pop"]/span/img/@src')[0].extract().strip()
                mp['intro'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[1]/dd//text()')])

                mp['upt_time'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[2]/dd/span/text()')])
                mp['upt_time'] = trim_time(mp['upt_time'])
                mp['spider_time'] = get_current()

                mp['url'] = response.url

            except Exception as e:
                traceback.print_exc()

            with open(out_file, 'a', encoding='utf-8') as fw:
                fw.write('{}\n'.format(mp))


search_fmt = 'http://weixin.sogou.com/weixin?query={}&type=1&page=1'

headers = {
    'Cookie': 'pgv_pvi=1520665600; RK=hf0PpTkeaa; pac_uid=1_779439458; pt2gguin=o0779439458; ptcz=da82dcae41f1c11792f5602d8a39d0447963e6124b8c380525c6e567ebd8ff03; noticeLoginFlag=1; remember_acct=xiaoege01%40gmail.com; pgv_pvid=3203998305; o_cookie=779439458; dm_login_weixin_scan='
}


def get_headers():
    return headers


# time_fmt = "%Y-%m-%d %H:%M:%S"
time_fmt = "%Y-%m-%d"


def get_current():
    return datetime.now().strftime(time_fmt)


def trim_num(text):
    m = num_pat.search(text)
    if m:
        return m.group()
    else:
        return 0


def trim_time(time):
    if '-' in time:
        return time
    else:
        return get_current()


def get_search_words():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f)
        return [search_fmt.format(line) for line in lines]


def main():
    print(time.time())


if __name__ == '__main__':
    main()
