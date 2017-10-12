#!/usr/bin/env python
# encoding: utf-8

"""
@description: 爬取苹果官网的应用

@author: pacman
@time: 2017/10/9 21:45
"""

from scrapy.selector import Selector


def run():
    filename = 'C:\\Users\\BaoQiang\\Desktop\\app-store.html'
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()

    root = Selector(text=data)

    classes = root.xpath('//div[@class="padtit1xia1"]/div')
    for item in classes:
        try:
            href = item.xpath('./a/img/@alt')[0].extract().strip()
            cate = item.xpath('./span[@class="padlan1"][2]//text()').extract()[-1].strip()
            print(href, '\t', cate)
        except Exception as e:
            print(item)


def main():
    run()


if __name__ == '__main__':
    main()
