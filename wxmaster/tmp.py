#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: BaoQiang
@time: 2017/7/12 11:20
"""

import requests
import json

def tmp():
    url = ''

def tmp2():
    root_path = 'C:\\Users\\BaoQiang\\Desktop\\'
    with open('{}/1.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/1.txt'.format(root_path), 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()

            json_data = json.loads(line)
            for item in json_data.values():
                value = str(item).replace('\n', '[sep]').replace('\t', '[tab]')
                if value.startswith('\''):
                    value = value[1:]
                if value.startswith('"'):
                    value = value[1:]
                fw.write('{}\t'.format(value))

            fw.write('\n')


def tmp1():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': 'visit-wxb-id=6e505dcc5d341c6caa560977218386be; PHPSESSID=ov4uvqubpuu95tc98q26877r83; IESESSION=alive; pgv_pvi=4971352064; pgv_si=s7572056064; _qddamta_4009981236=3-0; tencentSig=3228599296; wxb_fp_id=3884363302; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1499828836; Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91=1499829441; _qddaz=QD.lcc3jt.9a15p4.j50fd4p4; _qdda=3-1.10ga5x; _qddab=3-paixj9.j50fd4p7',
        'Host': 'data.wxb.com',
        'Referer': 'http://data.wxb.com/rankArticle',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # headers = {}

    url = 'http://data.wxb.com/rank/day/2017-07-10/-1?sort=index_scores+desc&page=100&page_size=20'

    response = requests.get(url, headers=headers)
    print(response.content.decode())


def main():
    tmp()


if __name__ == '__main__':
    main()
