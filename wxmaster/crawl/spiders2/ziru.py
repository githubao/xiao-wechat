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

from wxmaster.pth import FILE_PATH

out_file = '{}/ziru.json'.format(FILE_PATH)


class ZiruSpider(scrapy.Spider):
    name = 'ziru_spider'

    root_url = 'https://phoenix.ziroom.com'

    def start_requests(self):
        for i in range(1, 3):
            url = url_fmt.format(i)
            yield Request(url, callback=self.parse_cate)

    def parse_cate(self, response):
        data = response.body.decode()

        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(data, fw, sort_keys=True, ensure_ascii=False)
            fw.write('\n')


url_fmt = 'https://phoenix.ziroom.com/v7/room/list.json?app_version=5.4.0&city_code=110000&imei=3544432f10208b2bf30bb34919167ecc992b8179&os=iOS&page={}&sign=ceb3105546af10e20a4467df29bbb2a5&size=20&subway_code=%E6%98%8C%E5%B9%B3%E7%BA%BF&subway_station_code=&timestamp=1509423938&uid=e0d78f30-5d2f-4194-96dc-a82bbc465562'


def main():
    print('do sth')


if __name__ == '__main__':
    main()
