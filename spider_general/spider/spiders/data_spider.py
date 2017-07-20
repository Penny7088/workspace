# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem,myItem, CustomizeLoad

import sys
import re

import json
from pip._vendor.requests.api import request

import redis 
from scrapy.spiders.crawl import CrawlSpider
import urllib
r = redis.Redis(host='127.0.0.1', port=6378,db=0)
r.delete('spider_xxx')
r.lpush('spider_xxx', 'http://www.dianping.com/citylist/citylist?citypage=1')


class spider(CrawlSpider):
    
    name = 'spider_xxx'
    redis_key = 'spider_xxx'

    start_urls = ['http://www.dianping.com/citylist/citylist?citypage=1']
    

#  lpush spider_xxx:start_urls http://www.dianping.com/citylist/citylist?citypage=1


    def parse(self, response,dont_filter=True):
        item = myItem()
#         item['laier']= response.meta['item'][4]
        baseurl = 'http://www.dianping.com'
        urls = response.xpath('//@href').extract()
        print 'fuck you'
        for url in urls:
            if url.find('http')==-1 and url.find('www.')==-1:
                url = baseurl+url;
            print url
            if url.find('http://www.dianping.com')==-1:
                continue
#             yield Request(url=url,callback=self.parse_city,dont_filter=True,errback=self.err)
     
    def err(self,response): 
        print 'error'+response.url              

    def test(self,response):
#         item = myItem()
#         layer = response.meta['item']['layer']
        baseUrl = ''
        targetPath=[]
        urls = response.xpath('//@href')
#         t = t -1 
        url = urls.extract()[0]
        for i in range(1,30):
            print urls[i].extract()
            url = urls[i].extract()
        return url    
            
            
    # 处理第一页的列表
    def parse_city(self, response):
        print 'you fuck'
        urls = response.xpath('//@href').extract()
#         baseurl = 'http://www.dianping.com'
#         for url in urls:
#             if url.find('http')==-1:
#                 url = baseurl+url;
#             print url
#             if url.find('http://read.douban.com')==-1:
#                 continue
#             yield Request(url = url,  callback=self.parse_city,dont_filter=True)


    def pase_itemList(self, response):
        item = myItem()
        item['bigCate'] =  response.meta['item']['bigCate']
        item['smallCate'] =  response.meta['item']['smallCate']
        item['url'] =  response.meta['item']['url']
        item['city'] =  response.meta['item']['city']
        item['province'] =  response.meta['item']['province']
        itemList = response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        for i in itemList:
            url = 'http://www.dianping.com' + i.xpath('div/a/@href').extract_first()
            print url
            item['url'] = url
            yield Request(url = url, meta={'item':item}, callback=self.parse_item)
        
        try:
            url = 'http://www.dianping.com' + response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()[0]
            print 'next page url:  '+ url
            yield Request(url=url, meta={'item':item}, callback=self.pase_itemList)
        except:  
            print u"抓取完成!"

    def parse_item(self, response):
        item = SpiderItem()
        item['category'] = response.meta['item']['bigCate']+'-'+response.meta['item']['smallCate']
        item['province'] = response.meta['item']['province']
        item['city'] = response.meta['item']['city']
        item['username'] = response.xpath('//*[@id="basic-info"]/h1/text()').extract_first().strip()
        item['phone'] = response.xpath('//*[@id="basic-info"]/p/span[2]/text()').extract_first()
        item['paTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item['url'] = response.meta['item']['url']
        yield item
