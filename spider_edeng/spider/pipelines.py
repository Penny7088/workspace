# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
# import pymysql.cursors
# import MySQLdb.cursors
import pymongo
from scrapy.conf import settings
# import MySQLdb
from twisted.enterprise import adbapi



class SpiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        db = settings['MONGODB_DB']
        port = settings['MONGODB_PORT']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db]
        self.post = tdb['www.edeng.cn']
        self.ids_seen = set()

    def process_item(self, item, spider):
        data = dict(item)
        # if item['telPhone'] in self.ids_seen:
        #     raise DropItem("Duplicate item found: %s" % item)
        # else:
        #     self.ids_seen.add(item['telPhone'])
        self.post.insert(data)
        return item
    


# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(host=settings['MYSQL_HOST'],
#                        db=settings['MYSQL_DBNAME'],
#                        user=settings['MYSQL_USER'],
#                        passwd=settings['MYSQL_PASSWORD'],
#                        charset='utf8',
#                        cursorclass=MySQLdb.cursors.DictCursor,
#                        use_unicode=True,
#                        )
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error,item,spider)
#
#     def do_insert(self, cursor, item):
#         insert_sql = """insert into source_data_table(username,address,last_update_time)
#                                      VALUES (%s,%s,now())
#                              """
#         cursor.execute(insert_sql, (item['username'], item['address']))
#
#     def handle_error(self, failure,item,spider):
#         print failure
