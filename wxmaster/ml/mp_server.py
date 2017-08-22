#!/usr/bin/env python
# encoding: utf-8

"""
@description: 根据关键词匹配到的数据进行的一些推荐

@author: BaoQiang
@time: 2017/8/8 16:53
"""

input_file = 'd:/000/life/sogoump_final.json'
out_file = 'C:\\Users\\BaoQiang\\Desktop\\corpus.txt'

import json
import requests
from flask import Flask, request
import random
from collections import defaultdict

lucene_url = 'http://127.0.0.1:8765/?q={}'

dic = None
name_dic = None

app = Flask(__name__)


def form():
    with open(input_file, 'r', encoding='utf-8') as f, \
            open(out_file, 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())

            if json_data['read_cnt'] < 100 or json_data['month_cnt'] < 10:
                continue

            fw.write('{}\t{}\n'.format(json_data['desc'], json_data['uid']))


def init():
    global dic
    global name_dic

    dic = load_dic()
    name_dic = load_names()


@app.route('/')
def index():
    return 'mp app run'


@app.route('/mp')
def mp_result():
    """
    http://127.0.0.1:5000/mp?req=篮球
    :return: 
    """
    global dic
    global name_dic

    req = request.args.get('req')
    res = ''

    # 先根据全名获取数据
    name_lst = name_dic.get(req, '')
    if name_lst:
        res = dic.get(random.sample(name_lst, 1)[0], '')

    # 如果全名没有的话
    if not res:
        response = requests.get(lucene_url.format(req)).content.decode()
        results = json.loads(response)['results']

        if results:
            results = [item for item in results if item['score'] > 1.5]
            if results:
                res = dic.get(random.sample(results, 1)[0]['answer'], '')

    return app.make_response((json.dumps(useful(res)), 200))


def useful(content):
    if not content:
        return {'data': '', 'code': -1}
    else:
        try:
            content['votes'] = content['read_cnt'] * content['month_cnt']

            del content['url']
            del content['spider_time']
            del content['upt_time']
            del content['latest_article']
            del content['read_cnt']
            del content['month_cnt']
            del content['company']

        except:
            print(content)

        print('response: {}'.format(content))

        return {'data': content, 'code': 0}


def load_dic():
    dic = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            json_data = json.loads(line.strip())

            if json_data['read_cnt'] < 100 or json_data['month_cnt'] < 10:
                continue

            dic[json_data['uid']] = json_data

    return dic


def load_names():
    dic = defaultdict(list)
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            json_data = json.loads(line.strip())

            if json_data['read_cnt'] < 100 or json_data['month_cnt'] < 10:
                continue

            dic[json_data['name']].append(json_data['uid'])

    return dic


def tmp():
    form()


def run():
    init()
    app.run()


def main():
    # tmp()
    run()


if __name__ == '__main__':
    main()

"""
http://127.0.0.1:5000/mp?req=有书
{
"votes": 24000000,
"uid": "youshucc",
"company": "北京万维之道信息技术有限公司",
"name": "有书",
"desc": "有书,读完才是自己的.有书发起“每周共读行动计划”,带你和1000万书友一起,每天早晚读书半小时,一周读完1本好书,一年读完52本好书,成为更好的自己."
}

http://127.0.0.1:5000/mp?req=篮球
{
"votes": 1044,
"uid": "gh_ff3c854938db",
"company": "北流市篮球协会",
"name": "北流市篮球协会",
"desc": "全面负责篮球运动项目管理,研发指定方针政策,发展规划和指导篮球协会工作."
}

http://127.0.0.1:5000/mp?req=你难道不知道我是谁啊
{
"name": "才听说",
"votes": 19756,
"company": "郑州一加一广告有限公司",
"desc": "我知道你不知道的",
"uid": "yjy525hr"
}

"""
