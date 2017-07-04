#!/usr/bin/env python
# encoding: utf-8

"""
@description: 根据出现次数的多少 以及 平均阅读和点赞数量，三个维度处理数据

@author: BaoQiang
@time: 2017/7/4 17:46
"""

import json
from wxmaster.pth import FILE_PATH
from collections import defaultdict

input_file = '{}/werank.json'.format(FILE_PATH)
out_file = '{}/werank_mp_result.txt'.format(FILE_PATH)


def process():
    acc_dic = defaultdict(list)
    with open(input_file, 'r', encoding='utf-8') as f, \
            open(out_file, 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()

            json_data = json.loads(line)

            account = json_data['account_url']
            if len(acc_dic[account]) == 0:
                acc_dic[account].append([])
                acc_dic[account].append([])
                acc_dic[account].append(json_data['account'])
                acc_dic[account].append(json_data['cate'])

            read_cnt = json_data['read_cnt']
            if read_cnt > 100000:
                read_cnt = 100000

            acc_dic[account][0].append(read_cnt)
            acc_dic[account][1].append(json_data['vote_cnt'])

        score_dic = cal_score(acc_dic)

        sorted_dic = sorted(score_dic.items(), key=lambda x: x[1][4], reverse=True)

        for acc, values in sorted_dic:
            fw.write(
                '{}\t{}\t{}\t{:.2f}\t{:.0f}\t{:.0f}\t{}\n'.format(acc, values[2], values[3], values[4],
                                                                  sum(values[0]) / len(values[0]),
                                                                  sum(values[1]) / len(values[1]), len(values[0])))


def cal_score(acc_dic):
    new_dic = {}

    max_read = max(sum(item[0]) / len(item[0]) for item in acc_dic.values())
    max_vote = max(sum(item[1]) / len(item[1]) for item in acc_dic.values())
    max_cnt = max(len(item[0]) for item in acc_dic.values())

    for acc, values in acc_dic.items():
        score = (sum(values[0]) / len(values[0]) / max_read + sum(values[1]) / len(values[1]) / max_vote + len(
            values[0]) / max_cnt) / 3

        new_dic[acc] = values
        new_dic[acc].append(score)

    return new_dic


def main():
    process()


if __name__ == '__main__':
    main()
