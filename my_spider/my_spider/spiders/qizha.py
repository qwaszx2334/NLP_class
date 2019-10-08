# -*- coding: utf-8 -*-
import re
from urllib import parse
import sys
import scrapy

from ..items import TiebaItem


class QizhaSpider(scrapy.Spider):
    name = 'qizha'
    allowed_domains = ['https://tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E5%A4%B1%E4%BF%A1']

    def parse(self, response):
        url_list=response.css('.j_th_tit::attr(href)').extract()#页面中帖子的url地址
        for url in url_list:
            #print(url)
            print(parse.urljoin(response.url,url))
            yield scrapy.Request(url=parse.urljoin(response.url,url),callback=self.parse_detial,dont_filter=True)
        next_url=response.css('.next.pagination-item::attr(href)').extract()[0]
        if(next_url):
            yield scrapy.Request(url=parse.urljoin(response.url,next_url),callback=self.parse,dont_filter=True)

    def parse_detial(self,response):
        title=response.css('.core_title_txt.pull-left.text-overflow::text').extract()
        if title:
            user_list=response.css('.p_author_name.j_user_card::text').extract()
            content_list=response.css('.d_post_content.j_d_post_content').extract()
            content_list=self.get_content(content_list)
            time_list,floor_list=self.get_send_time_and_floor(response)
            #print()
            for i in range(len(user_list)):
                tieba_item=TiebaItem()
                tieba_item['title']=title[0]
                tieba_item['author']=user_list[i]
                tieba_item['content']=content_list[i]
                tieba_item['r_time']=time_list[i]
                tieba_item['r_floor']=floor_list[i]

                return tieba_item



    def get_content(self,contents):
        contents_lilst=[]
        for content in contents:
            reg=";\">(.*)</div>"
            result=re.findall(reg,content)[0]
            contents_lilst.append(result)
        return contents_lilst

    def get_send_time_and_floor(self,response):
        temp_list=response.css('.post-tail-wrap span[class=tail-info]::text').extract()
        time_list=[]
        floor_list=[]
        for i in temp_list:
            if(i.find('-')>=0):time_list.append(i)
            elif(i.find('楼')>=0):floor_list.append(i)
        return time_list,floor_list





