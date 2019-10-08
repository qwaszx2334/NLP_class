# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class MySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipline(object):
    def __init__(self, dbpoo=''):
        self.dbpool=dbpoo

    @classmethod
    def from_settings(cls,settings):
        dbaprms=dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbaprms)

        return cls(dbpool)

    def process_item(self,item, spider):
        query=self.dbpool.runInteraction(self.do_insert,item)

    def do_insert(self,cursor,item):
        insert_sql,params=item.get_insert_sql()
        cursor.execute(insert_sql,params)
