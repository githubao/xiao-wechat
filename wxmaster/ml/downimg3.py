#!/usr/bin/env python
# encoding: utf-8

"""
@description: 线程池下载

@author: BaoQiang
@time: 2017/7/1 10:56
"""

import time
import traceback
from concurrent import futures
from wxmaster.pth import FILE_PATH
import json

input_file = '{}/werank_info.json'.format(FILE_PATH)

import requests

BASE_PATH = '/data/baoqiang/product/doutu/wxmp'


def save_flag(img, filename):
    with open(filename, 'wb') as fw:
        fw.write(img)


def get_flag(url):
    try:
        resp = requests.get(url)
        return resp.content
    except Exception as e:
        print(url)
        traceback.print_exc()


MAX_WORKERS = 10


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, cc_list)

    return len(set(res))


def download_one(dic):
    url = dic['qrcode']
    image = get_flag(url)
    if not image:
        print('download {} err'.format(dic['name']))
        return ''

    posfix = url.split('.')[-1]
    fname = '{}/{}.{}'.format(BASE_PATH, dic['name'], posfix)

    save_flag(image, fname)
    return url


def run():
    t1 = time.time()
    dic_list = load_datas()
    count = download_many(dic_list)
    elasped = time.time() - t1
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elasped))


def load_datas():
    res_lst = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            json_data = json.loads(line)
            dic = {'name': json_data['name'], 'qrcode': json_data['qrcode']}

            res_lst.append(dic)

    return res_lst


def main():
    run()


if __name__ == '__main__':
    main()
