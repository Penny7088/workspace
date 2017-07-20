# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem, myItem, CustomizeLoad

import sys

import json
from pip._vendor.requests.api import request


# import redis
# r = redis.Redis(host='127.0.0.1', port=6379,db=0)
# r.lpush('spider_dianping:start_urls', 'http://www.dianping.com/citylist/citylist?citypage=1')    
# spider_dianping:start_urls http://www.dianping.com/citylist/citylist?citypage=1



class spider(RedisSpider):
    name = 'spider_dianping'
    redis_key = 'spider_dianping:start_urls'
    start_urls = ['http://www.dianping.com/citylist/citylist?citypage=1']

    def parse(self, response):
        divs = response.xpath('//ul[@class="glossary-list gl-region"]/li')
        item = myItem()
        for i in divs:
            if i.xpath('dl/dt/text()').extract() == []:
                foo = i.xpath('div/a')
                for j in foo:
                    item['province'] = ''
                    if j.xpath('strong/text()').extract_first() == None:
                        item['city'] = j.xpath('text()').extract_first()
                    else:
                        item['city'] = j.xpath('strong/text()').extract_first()
                    url = 'http://www.dianping.com' + j.xpath('@href').extract_first()
                    print item['city'] + url
                    yield Request(url=url, meta={'item': item}, callback=self.parse_city)
            else:
                foo = i.xpath('dl')
                for j in foo:
                    item['province'] = j.xpath('dt/text()').extract_first()
                    bar = j.xpath('dd/a')
                    for k in bar:
                        item['city'] = k.xpath('strong/text()').extract_first()
                        url = 'http://www.dianping.com' + k.xpath('@href').extract_first()
                        print item['province'] + item['city'] + url
                        yield Request(url=url, meta={'item': item}, callback=self.parse_city, dont_filter=True)

    # 处理第一页的列表
    def parse_city(self, response):
        # TODO 解析item 列表
        item = myItem()
        item['province'] = response.meta['item']['province']
        item['city'] = response.meta['item']['city']

        cates = response.xpath('//*[@id="index-nav"]/li')
        for k in cates:
            item['bigCate'] = k.xpath('div/a[1]/text()').extract_first()
            itemlen = len(k.xpath('div/a'))
            print itemlen
            for i in range(2, itemlen):
                item['smallCate'] = k.xpath('div/a[' + str(i) + ']/text()').extract_first()
                url = 'http://www.dianping.com' + k.xpath('div/a[' + str(i) + ']/@href').extract_first()
                item['url'] = url
                print item['bigCate'] + item['smallCate'] + ' ----------- ' + url
                yield Request(url=url, meta={'item': item}, callback=self.pase_itemList)

    def pase_itemList(self, response):
        item = myItem()
        item['bigCate'] = response.meta['item']['bigCate']
        item['smallCate'] = response.meta['item']['smallCate']
        item['url'] = response.meta['item']['url']
        item['city'] = response.meta['item']['city']
        item['province'] = response.meta['item']['province']
        itemList = response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        for i in itemList:
            url = 'http://www.dianping.com' + i.xpath('div/a/@href').extract_first()
            print url
            item['url'] = url
            yield Request(url=url, meta={'item': item}, callback=self.parse_item)

        try:
            url = 'http://www.dianping.com' + response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()[
                0]
            print 'next page url:  ' + url
            yield Request(url=url, meta={'item': item}, callback=self.pase_itemList, dont_filter=True)
        except:
            print u"抓取完成!"

    def parse_item(self, response):
        item = SpiderItem()
        item['category'] = response.meta['item']['bigCate'] + '-' + response.meta['item']['smallCate']
        item['province'] = response.meta['item']['province']
        item['city'] = response.meta['item']['city']
        item['username'] = response.xpath('//*[@id="basic-info"]/h1/text()').extract_first().strip()
        item['phone'] = response.xpath('//*[@id="basic-info"]/p/span[2]/text()').extract_first()
        item['paTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['url'] = response.meta['item']['url']
        yield item
