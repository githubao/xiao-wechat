#!/usr/bin/env python
# encoding: utf-8

"""
@description: 自如租房

@author: pacman
@time: 2017/10/31 12:12
"""

import scrapy
from scrapy import Request
import json
import re

from wxmaster.pth import FILE_PATH

out_file = '{}/ziru.json'.format(FILE_PATH)
out_file2 = '{}/ziru.txt'.format(FILE_PATH)

re_pat = re.compile('距(.*)线(.*)站([\d]+)米')


class ZiruSpider(scrapy.Spider):
    name = 'ziru_spider'

    def start_requests(self):
        for i in range(1, 1001):
            url = url_fmt.format(i)
            yield Request(url, callback=self.parse_cate)

    def parse_cate(self, response):
        data = response.body.decode()

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(json.loads(data), fw, sort_keys=True, ensure_ascii=False)
            fw.write('\n')


# ALL-2000元-224 * 20 个房间
url_fmt = 'https://phoenix.ziroom.com/v7/room/list.json?app_version=5.4.0&city_code=110000&imei=3544432f10208b2bf30bb34919167ecc992b8179&os=iOS&page={}&price=%2C2000&sign=f02d59d5d364b61f6736153433da7c13&size=10&timestamp=1509426842&uid=e0d78f30-5d2f-4194-96dc-a82bbc465562'


def process():
    with open(out_file, 'r', encoding='utf-8') as f, \
            open(out_file2, 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())

            for item in json_data['data']['rooms']:
                subinfo = get_subinfo(item['subway_station_info'])
                floor = '{}/{}'.format(item['floor'], item['floor_total'])
                area = item['area'].replace('约', '')

                fw.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                         .format(item['id'], item['name'], area, floor, item['bedroom'], subinfo[0], subinfo[1],
                                 subinfo[2],item['price'], item['face']))


def get_subinfo(txt):
    m = re_pat.match(txt)
    if m:
        return m.groups()
    else:
        return (txt, txt, txt)


def main():
    process()


if __name__ == '__main__':
    main()
