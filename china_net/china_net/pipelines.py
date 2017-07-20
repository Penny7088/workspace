# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy.conf import settings
import pymongo

class ChinaNetPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        db = settings['MONGODB_DB']
        port = settings['MONGODB_PORT']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db]
        self.post = tdb['china_net']
        self.ids_seen = set()

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
