#!/usr/bin/env python
# encoding: utf-8

"""
@description: 处理得到的号码数据，选取一个最好的

@author: pacman
@time: 2017/9/21 11:20
"""

import re
import os

root_path = 'C:\\Users\\BaoQiang\\Desktop\\'

pat_1 = re.compile('(\d)\\1')
pat_2 = re.compile('(\d)\\1$')

names = ['010', '0725', '0533', ]


def process():
    with open(os.path.join(root_path, '1.txt'), 'r', encoding='utf-8') as f, \
            open(os.path.join(root_path, '2.txt'), 'w', encoding='utf-8') as fw:
        for line in f:
            line = line.strip()

            if line.startswith('176'):
                continue

            flag1, flag2,flag3 = label(line)

            fw.write('{}\t{}\t{}\t{}\n'.format(line, flag1, flag2,flag3))


def label(num):
    flag1 = flag2 = flag3 = False
    m1 = pat_1.search(num)
    if m1:
        flag1 = True

    m2 = pat_2.search(num)
    if m2:
        flag2 = True

    for item in names:
        if item in num:
            flag3 = True

    return flag1, flag2, flag3


def main():
    process()


def tmp():
    num = '170916435771'
    print(label(num))


if __name__ == '__main__':
    main()
