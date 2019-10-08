# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TiebaItem(scrapy.Item):
    title=scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    r_time = scrapy.Field()
    r_floor = scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
            insert into baidu_tieba(title,author,content,r_time,r_floor)
            values(%s,%s,%s,%s,%s)
        """
        params=(self['title'],self['author'],self['content'],self['r_time'],self['r_floor'])
        return insert_sql,params

