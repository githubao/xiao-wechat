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
import time

out_file = '{}/gudong.json'.format(FILE_PATH)


class GudongSpider(scrapy.Spider):
    name = 'gudong_spider'

    root_url = 'https://api.codoon.com/api/get_group_sports_member'

    handle_httpstatus_list = [400,401]

    def start_requests(self):
        requests = []

        # for i in range(1, 101):
        for i in range(1, 2):
            new_data = data.update({'page': i})

            head = get_headers()
            head.update({'Timestamp':str(int(time.time()))})

            request = FormRequest(self.root_url, callback=self.parse_item,
                                  headers=head,formdata=new_data, dont_filter=True)

            requests.append(request)

        return requests

    def parse_item(self, response):
        with open(out_file, 'a', encoding='utf-8') as fw:
            # json_data= json.loads(response.body.decode().strip())
            json_data= response.body.decode().strip()
            json.dump(json_data, fw, ensure_ascii=False)
            fw.write('\n')


def get_headers():
    return headers


data = {
    "group_id": "83358",
    "position": "40.07632752186443,116.4187576244568",
    "limit": 50
}

headers2 = {}

headers = {
    'Host': 'api.codoon.com',
    'Accept': '*/*',
    'Gaea': '3d4085e0637268008e122782de46e997',
    'Davinci': '1',
    # 'Timestamp': '1503818016',
    'Authorization': 'Bearer 083d41a26acabef7b4ef1a880597562c',
    # 'Proxy-Connection': 'keep-alive',
    'Uranus': 'vg3U2lyJDqMBNzguavqLIlMguZXBYFStQk8FeFguEA+CJOhYxTrMqRKugO6809gM',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    # 'Content-Length': 89,
    'did': '23-ea173ffb390b9b35aaec0ae735917339',
    'User-Agent': 'CodoonSport(8.2.1 1870;iOS 9.3;iPhone)',
    # 'Connection': 'keep-alive',
}


def main():
    print('do sth')


if __name__ == '__main__':
    main()
