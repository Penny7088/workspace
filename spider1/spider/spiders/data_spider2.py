# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem,myItem, CustomizeLoad
import urllib
import os

import sys
import re
import json
from pip._vendor.requests.api import request

import redis 
r = redis.Redis(host='127.0.0.1', port=6379,db=0)
r.lpush('baixin_erShouChe:start_urls', 'http://www.baixing.com/?changeLocation=yes&return=%2Fershouqiche%2F%3Fsrc%3Dnew-home-nav')  


class spider(RedisSpider):
    name = 'baixin_erShouChe'
    redis_key = 'baixin_erShouChe:start_urls'
    start_urls = ['http://www.baixing.com/?changeLocation=yes&return=%2Fershouqiche%2F%3Fsrc%3Dnew-home-nav']
    
#     baixin_erShouChe:start_urls http://www.baixing.com/?changeLocation=yes&return=%2F


    def parse(self, response):
        citylistlen = len(response.xpath('//ul[@class="wrapper"]/li').extract())
        print citylistlen
        urlss = []
        item = myItem()
        for i in range(2,citylistlen):
            provinceflist = response.xpath('//ul[@class="wrapper"]/li['+str(i)+']/div')
            for p in provinceflist:
                item['province'] = p.xpath('h5/a/text()').extract()[0]   ##注意和上层xpath的结果之间不要有斜杠，否则会取到空list
                citylist = p.xpath('ul/li/a')
                for cityAndUrl in citylist:
                    url =urllib.unquote('http:'+cityAndUrl.xpath('@href').extract()[0])
                    item['city'] = cityAndUrl.xpath('text()').extract()[0]
                    print item['city']
                    print item['province']
                    print url
                    yield Request(url=url, meta={'item':item},callback=self.parse_city)

    # 处理第一页的列表
    def parse_city(self, response):
        # TODO 解析item 列表
        item = myItem()
        item['province']= response.meta['item']['province']
        item['city']= response.meta['item']['city']
        print "do"
        item_urls = response.xpath('//img[@id="ez-verify-image"]/@src').extract()[0]
        file_path=os.path.join("e:\\pics",'temp9gongge.jpg')
        urllib.urlretrieve(item_urls,file_path)
        for item_url in item_urls:
            print item_url
            yield Request(item_url, meta={'item':item}, callback=self.parse_item)

        try:
            url = response.xpath('//a[@class="next"]/@href').extract()[0]
            yield Request(url=url, meta={'item':item}, callback=self.parse_city)
        except:  
            print u"抓取完成!"

    def parse_item(self, response):
        print response.meta['item']['province'][0]
        print response.meta['item']['city'][0]
        item = SpiderItem()
        item['province'] = response.meta['item']['province'][0]
        item['city'] =response.meta['item']['city'][0]
        item['district'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[2]/a[1]/text()').extract_first()
        item['broker'] = response.xpath('/html/body/div[4]/div[3]/div[1]/div[2]/p[1]/a/text()').extract_first()
        item['phone'] = response.xpath('//p[@class="phone-num"]/text()').extract_first()
        item['cityProper'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[2]/a[1]/text()').extract_first()
        yield item
