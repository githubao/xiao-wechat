#!/usr/bin/env python
# encoding: utf-8

"""
@description: 微信热榜 爬虫

@author: BaoQiang
@time: 2017/7/4 15:28
"""

import scrapy
from scrapy import Request
from wxmaster.crawl.items import WeRankItem
from wxmaster.pth import FILE_PATH
import traceback
import json
from scrapy.selector import Selector

out_file = '{}/werank.json'.format(FILE_PATH)


class WeRankSpider(scrapy.Spider):
    name = 'werank_spider'

    root_url = 'http://werank.cn'

    def start_requests(self):
        return [Request(self.root_url, callback=self.parse_cate)]

    def parse_cate(self, response):
        for i in range(1, 927):
        # for i in range(926, 927):
            yield Request('{}/re{}'.format(self.root_url, i), callback=self.parse_item, meta={'id': i})

    def parse_item(self, response):
        # title = response.selector.xpath('.//h2/text()')
        # print(title[0].extract().strip())

        uid = 1
        classes = response.selector.xpath('//div[@class="col-md-10"]/h2')
        for item in classes:
            cate = item.xpath('./text()')[0].extract().strip()

            # following-sibling::*[@class!="anchor-list"][1]
            parent_node = item.xpath('../..')
            next_div_trs = parent_node.xpath('./following-sibling::div[@class="row"][1]//tr')[1:]

            werank_lst = []

            for tr in next_div_trs:
                werank = WeRankItem()

                tds = tr.xpath('./td')
                werank['url'] = response.url
                werank['account'] = tds[0].xpath('./a/text()')[0].extract().strip()
                werank['account_url'] = tds[0].xpath('./a/@href')[0].extract().strip()
                werank['article'] = tds[1].xpath('./a/text()')[0].extract().strip()
                werank['article_url'] = tds[1].xpath('./a/@href')[0].extract().strip()

                werank['read_cnt'] = int(tds[3].xpath('.//text()')[0].extract().strip().replace('10万+', '100000'))
                werank['vote_cnt'] = int(tds[4].xpath('.//text()')[0].extract().strip())
                werank['cate'] = cate
                werank['id'] = uid

                uid += 1
                werank_lst.append(werank)

                # break

            with open(out_file, 'a', encoding='utf-8') as fw:
                for werank in werank_lst:
                    fw.write('{}\n'.format(werank))


def test_xpath():
    html = open("C:\\Users\\BaoQiang\\Desktop\\wx.html", 'r', encoding='utf-8').read()
    root = Selector(text=html)

    uid = 1
    classes = root.xpath('//div[@class="col-md-10"]/h2')
    for item in classes:
        cate = item.xpath('./text()')[0].extract().strip()

        # following-sibling::*[@class!="anchor-list"][1]
        parent_node = item.xpath('../..')
        next_div_trs = parent_node.xpath('./following-sibling::div[@class="row"][1]//tr')[1:]

        results = []

        for tr in next_div_trs:
            werank = WeRankItem()

            tds = tr.xpath('./td')
            werank['url'] = 4
            werank['account'] = tds[0].xpath('./a/text()')[0].extract().strip()
            werank['account_url'] = tds[0].xpath('./a/@href')[0].extract().strip()
            werank['article'] = tds[1].xpath('./a/text()')[0].extract().strip()
            werank['article_url'] = tds[1].xpath('./a/@href')[0].extract().strip()

            werank['read_cnt'] = int(tds[3].xpath('.//text()')[0].extract().strip().replace('10万+', '100000'))
            werank['vote_cnt'] = int(tds[4].xpath('.//text()')[0].extract().strip())
            werank['cate'] = cate
            werank['id'] = uid

            uid += 1
            results.append(werank)

            # break

        with open(out_file, 'a', encoding='utf-8') as fw:
            for werank in results:
                fw.write('{}\n'.format(werank))

                # break


def main():
    test_xpath()


if __name__ == '__main__':
    main()
