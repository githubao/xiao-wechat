#!/usr/bin/env python
# encoding: utf-8

"""
@description: 微信公众号爬虫

@author: BaoQiang
@time: 2017/5/26 16:07
"""

import re
import time
import traceback
from datetime import datetime
from urllib.parse import unquote

import requests
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from wxmaster.crawl.items import WxMpItem
from wxmaster.pth import FILE_PATH

num_pat = re.compile('[\d]+')

input_file = '{}/words.txt'.format(FILE_PATH)
out_file = '{}/sogoump.json'.format(FILE_PATH)

root_url = 'http://weixin.sogou.com'

time_fmt = "%Y-%m-%d %H:%M:%S"


# time_fmt = "%Y-%m-%d"

class SogouMpSpider(CrawlSpider):
    name = 'sogoump_spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'wxmaster.crawl.pipelines.SogouMpPipeline': 300,
        }
    }

    # rules = [
    #     Rule(LinkExtractor(allow=('/weixin.*query.*',)), callback='parse_item', follow=True,
    #          process_request='add_header')
    # ]

    def add_header(self, request):
        request.replace(headers=get_headers())
        return request

    def start_requests(self):
        return [Request(root_url, callback=self.parse_list,dont_filter=True)]

    def parse_list(self, response):
        urls = get_search_words()

        for url in urls:
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        month_url = get_month_url(response.body.decode())
        if month_url:
            try:
                json_data = requests.get(month_url).json()
                msg_dic = json_data['msg']
            except:
                msg_dic = {}
        else:
            msg_dic = {}

        mp_list = []
        classes = response.selector.xpath('//ul[@class="news-list2"]/li')
        for item in classes:
            mp = WxMpItem()
            try:
                mp['name'] = ''.join([i.extract().strip() for i in item.xpath('.//p[@class="tit"]//text()')])
                mp['uid'] = item.xpath('.//p[@class="info"]/label/text()')[0].extract().strip()

                # 二维码
                # mp['qrcode'] = item.xpath('.//div[@class="ew-pop"]/span/img/@src')[0].extract().strip()

                # 简介
                mp['desc'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[1]/dd//text()')])

                # 公司名称
                company_url = ''.join([i.extract().strip() for i in item.xpath('.//dl[2]/dt//text()')])
                if company_url and '认证' in company_url:
                    mp['company'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[2]/dd//text()')])
                else:
                    mp['company'] = ''

                # 最新文章
                mp['latest_article'] = ''.join([i.extract().strip() for i in item.xpath('.//dl[last()]/dd/a//text()')])

                # 更新时间
                upt_url = ''.join([i.extract().strip() for i in item.xpath('.//dl[last()]/dd/span//text()')])
                mp['upt_time'] = get_upt_time(upt_url)
                mp['spider_time'] = get_current()

                # 阅读总数
                li_url = item.xpath('./@d')[0].extract().strip()
                mp['month_cnt'] = int(msg_dic.get(li_url, '0,0').split(',')[0])
                mp['read_cnt'] = int(msg_dic.get(li_url, '0,0').split(',')[1])

                mp['url'] = unquote(response.url)

            except Exception as e:
                traceback.print_exc()

            mp_list.append(mp)

        # 保存数据
        with open(out_file, 'a', encoding='utf-8') as fw:
            for mp in mp_list:
                # fw.write('{}\n'.format(mp))
                yield mp


def get_month_url(url):
    m = month_pat.search(url)
    if m:
        return '{}{}'.format(root_url, m.group(1))
    else:
        return None


def get_headers():
    return headers


def get_current():
    return datetime.now().strftime(time_fmt)


def trim_num(text):
    m = num_pat.search(text)
    if m:
        return m.group()
    else:
        return 0


def trim_time(time):
    if not time:
        return ''
    elif '-' in time:
        return time
    else:
        return get_current()


def get_upt_time(src):
    m = upt_pat.search(src)
    if m:
        upt_time = time.localtime(int(m.group(1)))
        return time.strftime(time_fmt, upt_time)
    else:
        return ''


def get_search_words():
    res_list = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            attr = line.split('\t')
            if len(attr) != 2:
                continue

            res_list.append(search_fmt.format(attr[0]))

    return res_list


search_fmt = 'http://weixin.sogou.com/weixin?query={}&type=1&page=1'

headers = {
    'Cookie': 'pgv_pvi=1520665600; RK=hf0PpTkeaa; pac_uid=1_779439458; pt2gguin=o0779439458; ptcz=da82dcae41f1c11792f5602d8a39d0447963e6124b8c380525c6e567ebd8ff03; noticeLoginFlag=1; remember_acct=xiaoege01%40gmail.com; pgv_pvid=3203998305; o_cookie=779439458; dm_login_weixin_scan='
}

month_pat = re.compile('account_anti_url[ =]+?"(.+)?"')
upt_pat = re.compile('(\d)+')


def tmp1():
    print(time.time())


def tmp():
    s = 'b326815a'
    print(type(upt_pat.search(s).group()))


def main():
    tmp()


if __name__ == '__main__':
    main()
