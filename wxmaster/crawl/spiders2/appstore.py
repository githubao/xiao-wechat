#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爬取itunes

@author: pacman
@time: 2017/10/12 19:24
"""

import json
import re
import urllib.parse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxmaster.pth import FILE_PATH

app_pat = re.compile('https://itunes.apple.com/cn/app/(.+)/id([\d]+)\?mt=8')

out_file = FILE_PATH + '/app-store.json'


class AppStoreSpider(CrawlSpider):
    name = 'appstore_spider'

    start_urls = ['https://itunes.apple.com/cn/genre/ios/id36?mt=8']

    rules = [
        Rule(LinkExtractor(allow=('/genre/ios-(.+)/id[\d]+\?mt=8',)), callback='parse_group', follow=False),
        # Rule(LinkExtractor(allow=('/app/(.+)/id[\d]+?mt=8',)), callback='parse_item', follow=False),
    ]

    def parse_group(self, response):
        classes = response.selector.xpath('//div[@id="selectedcontent"]//a/@href')
        for item in classes:
            yield Request(item.extract().strip(), callback=self.parse_item)

    def parse_item(self, response):
        app_dic = {}

        left_xpath = response.selector.xpath('//div[@id="left-stack"]')

        cate_xpath = left_xpath.xpath('.//span[@itemprop="applicationCategory"]/text()')
        app_dic['cate'] = cate_xpath[0].extract().strip()

        date_xpath = left_xpath.xpath('.//span[@itemprop="datePublished"]')
        app_dic['create_at'] = date_xpath.xpath('./@content')[0].extract().strip().split(' ')[0]
        app_dic['update_at'] = date_xpath.xpath('./text()')[0].extract().strip()

        rating_xpath = left_xpath.xpath('.//span[@class="rating-count"]//text()')
        app_dic['total_count'] = app_dic['current_count'] = app_dic['current_score'] = 0
        if len(rating_xpath) == 1:
            app_dic['total_rating'] = int(rating_xpath[0].extract().strip().replace(' 份评分', ''))
        if len(rating_xpath) == 2:
            app_dic['current_rating'] = int(rating_xpath[0].extract().strip().replace(' 份评分', ''))
            app_dic['total_rating'] = int(rating_xpath[1].extract().strip().replace(' 份评分', ''))

            score_xpath = left_xpath.xpath('.//span[@itemprop="ratingValue"]//text()')
            app_dic['current_score'] = float(score_xpath[0].extract().strip())

            app_dic['current_score'] = int()

        url = urllib.parse.unquote(response.url)
        app_dic['url'] = url
        app_dic['name'], app_dic['id'] = parse_url(url)

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(app_dic, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def parse_url(url):
    m = app_pat.match(url)
    return m.group(1), m.group(2)


def main():
    print('do sth')


if __name__ == '__main__':
    main()
