#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爱妮微网 的公众号爬虫

@author: BaoQiang
@time: 2017/6/23 18:44
"""

import scrapy
from scrapy import Request
from wxmaster.crawl.items import MpAnyvItem
from wxmaster.pth import FILE_PATH
import traceback
import json

out_file = '{}/all_mp.json'.format(FILE_PATH)


class MpAnyvSpider(scrapy.Spider):
    name = 'mpanyv_spider'

    root_url = 'http://www.anyv.net/index.php'

    def start_requests(self):
        return [Request(self.root_url, callback=self.parse_cate)]

    def parse_cate(self, response):
        ids = load_ids()

        for i in range(1, 72574):
            if i in ids:
                continue

            yield Request('{}/viewnews-{}'.format(self.root_url, i), callback=self.parse_item, meta={'id': i})

    def parse_item(self, response):
        mp = MpAnyvItem()
        mp['id'] = response.meta['id']
        mp['url'] = response.url

        try:
            mp['name'] = response.selector.xpath('//h1/text()')[0].extract().strip()
            cate = response.selector.xpath('//div[@class="content_top"]//a//text()')
            if len(cate) > 2:
                mp['cate'] = cate[1].extract().strip().replace('微信公众号', '')

            p_lst = response.selector.xpath('//div[contains(@class,"span_3_of_2")]//p//text()')
            for item in p_lst:
                content = item.extract().strip()
                if '微信号:' in content:
                    mp['uid'] = content[content.find('微信号') + 3:].strip().strip(':：')
                if '发布时间：' in content:
                    mp['created_at'] = content[content.find('发布时间') + 4:].strip().strip(':：')

            p_lst2 = response.selector.xpath('//div[@id="article"]/p/text()')
            desc = ''.join([item.extract().strip() for item in p_lst2])
            if '微信介绍：' in desc:
                mp['desc'] = desc[desc.find('微信介绍：') + 5:].strip()

            region = response.selector.xpath('//div[@id="article_summary"]/a/text()')
            mp['region'] = ''.join([item.extract().strip() for item in region])

            img_url = response.selector.xpath('//div[@id="article"]//img/@src')
            if img_url:
                mp['img_src'] = img_url[0].extract().strip()
            else:
                mp['img_src'] = ''
        except Exception as e:
            traceback.print_exc()

        with open(out_file, 'a', encoding='utf-8') as fw:
            fw.write('{}\n'.format(mp))


def load_ids():
    res_list = []
    with open(out_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            json_data = json.loads(line)

            res_list.append(json_data['id'])


def main():
    print('do sth')


if __name__ == '__main__':
    main()
