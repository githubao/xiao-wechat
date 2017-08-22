#!/usr/bin/env python
# encoding: utf-8

"""
@description: 咕咚 spider

@author: pacman
@time: 2017/8/22 19:37
"""

import scrapy
from scrapy.http import FormRequest
from wxmaster.pth import FILE_PATH
import json

out_file = '{}/gudong.json'.format(FILE_PATH)


class GudongSpider(scrapy.Spider):
    name = 'gudong_spider'

    root_url = 'https://api.codoon.com/v2/groupmanage/get_my_city_vip_group'

    def start_requests(self):
        requests = []

        # for i in range(1, 101):
        for i in range(1, 4):
            new_data = data.update({'page': i})
            request = FormRequest(self.root_url, callback=self.parse_item,
                                  headers=get_headers(), formdata=new_data, dont_filter=True)
            requests.append(request)

        return requests

    def parse_item(self, response):
        with open(out_file, 'a', encoding='utf-8') as fw:
            json.dump(response.body.decode(), fw, ensure_ascii=False)
            fw.write('\n')


def get_headers():
    return headers


data = {
    "tag_id": 0,
    "city_code": "110108",
    "position": "40.02620806858238,116.3047331104982",
    "limit": 10
}

headers = {
    'Host': 'api.codoon.com',
    'Accept': '*/*',
    'Gaea': 'd76c66f303f31eef2df0a9e8d99e7d93',
    'Davinci': '1',
    'Timestamp': '1503401991',
    'Authorization': 'Bearer 315931164a6ee4a14de50d7c5fef9907',
    'Proxy-Connection': 'keep-alive',
    'Uranus': '7oyqHGYgdHfz5G89TD52UlxZYyrmcYCdn+ID3FWx8FIoW0TMHN4C8ybzQnFWGE6Y',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Content-Length': '2',
    'did': '23-ea173ffb390b9b35aaec0ae735917339',
    'User-Agent': 'CodoonSport(8.1.0 1850;iOS 9.3;iPhone)',
    'Connection': 'keep-alive',
    'Cookie': 'anony_uid=335686386667603361763025; sessionid=faaf15a19323ce61ee5e831570171521',

}


def main():
    print('do sth')


if __name__ == '__main__':
    main()
