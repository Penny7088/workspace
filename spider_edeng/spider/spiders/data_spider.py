# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem,myItem, CustomizeLoad

import sys

import json
from pip._vendor.requests.api import request

# import redis 
# r = redis.Redis(host='127.0.0.1', port=6379,db=0)
# r.lpush('spider_edeng:start_urls', 'http://www.edeng.cn/')    
#    spider_edeng:start_urls http://www.edeng.cn/


class spider(RedisSpider):
    
    name = 'spider_edeng'
    redis_key = 'spider_edeng:start_urls'
    start_urls = ['http://www.edeng.cn/']



    def parse(self, response):
        divs = response.xpath('//div[@class="edhp_center"]/div')
        item = myItem()
        for i in divs:
            foo = i.xpath('*')
            for j in foo:
                if j.root.tag == 'h2':
                    item['bigCate'] = j.xpath('a/text()').extract()[0]
                    print item['bigCate']
                    continue
                if j.xpath('a/text()').extract() != []:
                    item['smallCate'] = j.xpath('a/text()').extract()[0]
                    print item['smallCate']
                    url = j.xpath('a/@href').extract()[0]
                    print url
                    yield Request(url=url, meta={'item':item}, callback=self.parse_city,dont_filter=True)
                    


    # 处理第一页的列表
    def parse_city(self, response):
        # TODO 解析item 列表
        item = myItem()
        item['bigCate']= response.meta['item']['bigCate']
        item['smallCate']= response.meta['item']['smallCate']
        
        print "do"
        item_urls = response.xpath('//div[@class="m-a"]/a/@href').extract()
        for item_url in item_urls:
            print item_url
            item['url']= item_url
            yield Request(item_url, meta={'item':item}, callback=self.parse_item)

        try:
            url = response.xpath('//a[@class="p-r"]/@href').extract()[0]
            yield Request(url=url, meta={'item':item}, callback=self.parse_city,dont_filter=True)
        except:  
            print u"抓取完成!"

    def parse_item(self, response):
        print response.meta['item']['bigCate']
        print response.meta['item']['smallCate']
        print response.meta['item']['url']
        item = SpiderItem()
        item['category'] = response.meta['item']['bigCate']+'-'+response.meta['item']['smallCate']
        item['province'] = response.xpath('//div[@class="mx-cj"]/p[5]/a[1]/text()').extract_first()
        item['city'] = response.xpath('//div[@class="mx-cj"]/p[5]/a[2]/text()').extract_first()
        item['district'] = response.xpath('//div[@class="mx-cj"]/p[5]/a[3]/text()').extract_first()
        item['username'] = response.xpath('//div[@class="mx-cj"]/p[1]/text()').extract_first().strip()
        item['phone'] = response.xpath('//div[@class="mx-cj"]/p[3]/a[2]/text()').extract_first()
        item['wx_number'] = response.xpath('//div[@class="mx-cj"]/p[3]/a[2]/text()').extract_first()
        item['paTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item['url'] = response.meta['item']['url']
        item['otherInfo'] = response.xpath('//div[@class="mx-d2"]/text()').extract_first().strip()
        yield item
