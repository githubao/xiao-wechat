#!/usr/bin/env python
# encoding: utf-8

"""
@description: 多看爬虫

@author: BaoQiang
@time: 2017/7/5 13:10
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from wxmaster.pth import FILE_PATH
from wxmaster.crawl.items import DuoKanItem
import sys

out_file = '{}/duokan.json'.format(FILE_PATH)


class DuoKanSpider(CrawlSpider):
    name = 'duokan_spider'

    all_domains = ['duokan.com']

    start_urls = ['http://www.duokan.com']

    rules = [
        Rule(LinkExtractor(allow='/list/[\d_]*'), follow=True),
        Rule(LinkExtractor(allow='/book/[\d]*'), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        duokan = DuoKanItem()

        duokan['url'] = response.url
        duokan['name'] = response.selector.xpath('//div[@class="desc"]/h3/text()')[0].extract().strip()
        duokan['cate'] = response.selector.xpath('//div[@class="u-nav-crumbs"]/a/text()')[-1].extract().strip()
        tags_xpath = '//section[@class="u-taglist"]//li//text()'
        duokan['tags'] = [item.extract().strip() for item in response.selector.xpath(tags_xpath)]
        duokan['vote_cnt'] = int(response.selector.xpath('//span[@itemprop="reviewCount"]/text()')[0].extract().strip())
        duokan['score'] = float(response.selector.xpath('//em[@itemprop="ratingValue"]/text()')[0].extract().strip())
        desc_xpath = '//article[@class="intro"]//text()'
        duokan['desc'] = '\n'.join(item.extract().strip() for item in response.selector.xpath(desc_xpath))

        with open(out_file, 'a', encoding='utf-8') as fw:
            fw.write('{}\n'.format(duokan))


def main():
    print('do sth')


if __name__ == '__main__':
    main()
