#!/usr/bin/env python
# encoding: utf-8

"""
@description:python 的mongo操作接口

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: mymongo.py
@time: 2017/2/8 14:15
"""

from pymongo import MongoClient


class MyMongo():
    url = 'mongodb://admin:password@192.168.10.29:27022'
    auth_db = 'admin'

    def __init__(self):
        self.client = MongoClient(self.url)

    def _get_db(self, db):
        return self.client[db]

    def get_one(self, db, coll, key, value):
        datebase = self._get_db(db)
        collect = datebase[coll]
        # return collect.find_one({key: value}, {'_id': 0})
        return collect.find_one({key: value})

    def get_all(self, db, coll):
        datebase = self._get_db(db)
        collect = datebase[coll]
        rs = collect.find()
        return [item for item in rs]

    def count(self, db, coll):
        datebase = self._get_db(db)
        collect = datebase[coll]
        return collect.count()

    def set_one(self, db, coll, item):
        datebase = self._get_db(db)
        collect = datebase[coll]
        return collect.insert_one(item)

    def upt_all(self, db, coll, find_item,upt_item,upsert=False,multi=False):
        datebase = self._get_db(db)
        collect = datebase[coll]
        return collect.update(find_item,upt_item,upsert=upsert,multi=multi)

    def remove(self,db,coll,key, value):
        datebase = self._get_db(db)
        collect = datebase[coll]
        return collect.delete_one({key: value})

    def close(self):
        self.client.close()


def test_mongo():
    db = 'bigdata'

    # coll = 'test'
    coll = 'songs'

    key = '中文名'
    value = '宋祖英'

    mongo = MyMongo()

    # res = mongo.get_one(db, coll, key, value)
    # res = mongo.get_all(db, coll)
    res = mongo.count(db, coll)

    print(res)


def main():
    test_mongo()


if __name__ == '__main__':
    main()
