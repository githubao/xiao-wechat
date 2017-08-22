#!/usr/bin/env python
# encoding: utf-8

"""
@description: 公众号的阅读总数 排名

@author: BaoQiang
@time: 2017/7/24 17:00
"""

import json

root_path = 'C:\\Users\\BaoQiang\\Desktop\\'


def run():
    processed_id = set()
    datas = []
    with open('{}/sogou_mp.json'.format(root_path), 'r', encoding='utf-8') as f, \
            open('{}/sogoump_final.json'.format(root_path), 'w', encoding='utf-8') as fw:
        for line in f:
            json_data = json.loads(line.strip())
            if len(json_data) != 11:
                continue

            uid = json_data['uid']
            if uid not in processed_id:
                datas.append(json_data)
                processed_id.add(uid)

        datas.sort(key=lambda x: x['read_cnt'] * x['month_cnt'], reverse=True)

        for item in datas:
            del item['_id']
            json.dump(item, fw, ensure_ascii=False, sort_keys=True)
            fw.write('\n')


def main():
    run()


if __name__ == '__main__':
    main()
