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

num_pat = re.compile('[\d]+')

input_file = '{}/keywords.txt'.format(FILE_PATH)
out_file = '{}/wxmp.json'.format(FILE_PATH)


class WxMpSpider(CrawlSpider):
    name = 'wxmp_spider'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls = get_search_words()

    rules = [
        Rule(LinkExtractor(allow=('/weixin.*query.*',)), callback='parse_item', follow=False)
    ]

    def parse_item(self, response):
        mp = WxMpItem()
        classes = response.selector.xpath('//ul[@class="news-list2"]/li')
        for item in classes:
            mp['title'] = ''.join([i.extract().strip() for i in item.xpath('.//p[@class="tit"]//text()')])
            mp['name'] = item.xpath('.//p[@class="info"]/label/text()')[0].extract().strip()
            mp['month_cnt'] = ''.join([i.extract().strip() for i in item.xpath('.//p[@class="info"]/text()')])
            mp['month_cnt'] = trim_num(mp['month_cnt'])
            mp['qrcode'] = item.xpath('.//div[@class="ew-pop"]/span/img/@src')[0].extract().strip()
            mp['intro'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[1]/dd//text()')])
            mp['company'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[2]/dt//text()')])

            with open(out_file, 'a', encoding='utf-8') as fw:
                fw.write('{}\n'.format(mp))


search_fmt = 'http://weixin.sogou.com/weixin?query={}&_sug_type_=&sut=2253&lkt=0%2C0%2C0+&s_from=input&_sug_=y&type=1&sst0={}&ie=utf8&w=01019900&dr=1'


def trim_num(text):
    m = num_pat.search(text)
    if m:
        return m.group()
    else:
        return text


def get_search_words():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f)
        return [search_fmt.format(line, int(time.time() * 1000)) for line in lines]


def main():
    print('do sth')


if __name__ == '__main__':
    main()
