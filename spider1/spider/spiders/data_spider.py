# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem,myItem, CustomizeLoad

import sys

import json
from pip._vendor.requests.api import request

  


class spider(RedisSpider):
    
    name = 'spider'
    redis_key = 'spider58:start_urls'
    start_urls = ['http://www.58.com/ershoufang/changecity/?PGTID=0d30000c-0000-1b1e-ff53-0f885644a29a&ClickID=1']

#     lpush spider58:start_urls http://www.58.com/ershoufang/changecity/?PGTID=0d30000c-0000-1b1e-ff53-0f885644a29a&ClickID=1

    def parse(self, response):
        provinceNumb = len(response.xpath('//*[@id="clist"]/dt').extract())
        for i in range(2,provinceNumb):
            item = myItem()
            item['province'] = response.xpath('//*[@id="clist"]/dt['+str(i)+']/text()').extract()
            cityNamesAndUrl = response.xpath('//*[@id="clist"]/dd['+str(i)+']/a')
            for city_url in cityNamesAndUrl:
                item['city'] = city_url.xpath('text()').extract()
                url = city_url.xpath('@href').extract()[0]
                yield Request(url=url, meta={'item':item},callback=self.parse_city,dont_filter=True)
        
        re = response.xpath('//*[@id="clist"]/dd[1]/a')
        for j in re:
            item = myItem()
            url = j.xpath('@href').extract()
            zxs = ['北京'.decode('utf-8'),'上海'.decode('utf-8'),'天津'.decode('utf-8'),'重庆'.decode('utf-8')]
            item['city'] = j.xpath('text()').extract()
            if item['city'][0] in zxs:
                item['province'] = '直辖市'
            yield Request(url=url, meta={'item':item},callback=self.parse_city,dont_filter=True)
    # 处理第一页的列表
    def parse_city(self, response):
        # TODO 解析item 列表
        item = myItem()
        item['province']= response.meta['item']['province']
        item['city']= response.meta['item']['city']
        
        print "do"
        item_urls = response.xpath('//h2[@class="title"]/a/@href').extract()
        for item_url in item_urls:
            print item_url
            item['url']= item_url
            yield Request(item_url, meta={'item':item}, callback=self.parse_item)

        try:
            url = response.xpath('//a[@class="next"]/@href').extract()[0]
            yield Request(url=url, meta={'item':item}, callback=self.parse_city,dont_filter=True)
        except:  
            print u"抓取完成!"

    def parse_item(self, response):
        print response.meta['item']['province'][0]
        print response.meta['item']['city'][0]
        print response.meta['item']['url']
        item = SpiderItem()
        item['province'] = response.meta['item']['province'][0]
        item['city'] =response.meta['item']['city'][0]
        item['district'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[2]/a[1]/text()').extract_first()
        item['broker'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/p[1]/span/text()').extract_first()
        item['phone'] = response.xpath('//p[@class="phone-num"]/text()').extract_first()    
        item['cityProper'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[2]/a[1]/text()').extract_first()
        item['paTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item['url'] = response.meta['item']['url']
        yield item
