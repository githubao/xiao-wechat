#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爬取公众号的信息

@author: BaoQiang
@time: 2017/7/4 18:20
"""

import scrapy
from scrapy import Request

from wxmaster.crawl.items import WeRankItem
from wxmaster.pth import FILE_PATH

input_file = '{}/werank_sort.txt'.format(FILE_PATH)
out_file = '{}/werank_info.json'.format(FILE_PATH)


class WeRank2Spider(scrapy.Spider):
    name = 'werank2_spider'

    root_url = 'http://chuansong.me'

    def start_requests(self):
        return [Request(self.root_url, callback=self.parse_cate)]

    def parse_cate(self, response):
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                attr = line.split('\t')
                if len(attr) != 7:
                    continue

                url, name, cate, score, *_ = attr

                yield Request(url, callback=self.parse_item, meta={'name': name, 'cate': cate, 'score': score})

                # break

    def parse_item(self, response):
        werank = WeRankItem()
        werank['url'] = response.url
        werank['name'] = response.meta['name']
        werank['cate'] = response.meta['cate']
        werank['score'] = response.meta['score']

        werank['id'] = response.selector.xpath('//div[contains(@class,"section_top")]/h3/div/text()')[
            0].extract().strip().strip('微信ID:')
        werank['qrcode'] = response.selector.xpath('//div[contains(@class,"related_topics")]//img/@src')[
            0].extract().strip()

        desc_div = '//div[@class="section"]//div[@class=" inline_editor_content"]//text()'
        werank['desc'] = ''.join(item.extract().strip() for item in response.selector.xpath(desc_div))

        with open(out_file, 'a', encoding='utf-8') as fw:
            fw.write('{}\n'.format(werank))


def main():
    print('do sth')


if __name__ == '__main__':
    main()
