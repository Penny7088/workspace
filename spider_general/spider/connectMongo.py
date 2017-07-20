# -*- coding: utf-8 -*-
from pymongo import MongoClient

def connect():
    client = MongoClient('localhost',27017)
#连接所需数据库,test为数据库名
    db=client.test
#连接所用集合，也就是我们通常所说的表，test为表名
    collection=db.test
#接下里就可以用collection来完成对数据库表的一些操作
#查找集合中所有数据
    for item in collection.find({'name':{"$regex":u','}}):
        xx = item['name']
        print xx.encode('gbk')
        xx.replace('男'.decode('gbk'),'abc')
        print xx
#         collection.save(item)
        break
#查找集合中单条数据
#     print collection.find_one() 
#向集合中插入数据
#     collection.insert({'name':'Tom','age':25,'addr':'Cleveland'})
#更新集合中的数据,第一个大括号里为更新条件，第二个大括号为更新之后的内容
#     collection.update({'Name':'Tom'},{'Name':'Tom','age':18})
#     collection.remove()
#     collection.drop()

    

connect()