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

input_file = '{}/keywords.txt'.format(FILE_PATH)


class WxMpSpider(CrawlSpider):
    name = 'wxmp_spider'

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls = get_search_words()

    rules = [
        Rule(LinkExtractor(allow=('/.*query.*',)), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        print(response.body.decode())


search_fmt = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={' \
             '}&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2253&sst0=1495786710657&lkt=0%2C0%2C0 '


def get_search_words():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f)
        return [search_fmt.format(line) for line in lines]


def main():
    print('do sth')


if __name__ == '__main__':
    main()
