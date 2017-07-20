# -*- coding: utf-8 -*-
import time
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider.items import SpiderItem, myItem, CustomizeLoad
from scrapy.spiders.crawl import CrawlSpider
import sys

import json
from pip._vendor.requests.api import request


# import redis
# r = redis.Redis(host='127.0.0.1', port=6378,db=0)
# r.lpush('spider_ganji:', 'http://www.ganji.com/index.htm')    


# lpush spider_ganji http://www.ganji.com/index.htm



class spider(RedisSpider):
    name = 'spider_ganji'
    redis_key = 'spider_ganji'
    start_urls = ['http://www.ganji.com/index.htm']

    def parse(self, response):
        divs = response.xpath('//html/body/div[1]/div[3]/dl/dd/a/@href')
        for i in divs:
            url = i.extract()
            print 'aad url: ' + url
            yield Request(url=url, callback=self.parse_city, dont_filter=True)

    # 处理第一页的列表
    def parse_city(self, response):
        baseurl = response.request.url
        print 'base url: ' + baseurl
        f = response.xpath('//html/body/div[3]/div[2]/div[1]/div[1]/div')
        for i in f:
            url = baseurl + i.xpath('a/@href').extract_first()
            print 'add 2ed layer url: ' + url
            yield Request(url=url, callback=self.pase_itemList, dont_filter=True)
            #         yield Request(url = 'http://cd.ganji.com/fang1/', callback=self.pase_itemList,dont_filter=True)

    def pase_itemList(self, response):
        if response.request.url.find('o2') > 0:
            print 'fuck found   ' + response.request.url
        baseurl = response.request.url.split('com')[0] + 'com'
        print baseurl
        l = response.xpath('//*[@id="f_mew_list"]/div[6]/div/div[3]/div[1]/div')
        for i in l:
            if i.xpath('dl/dd[1]/a/@href').extract_first().find('http://') == 0:
                url = i.xpath('dl/dd[1]/a/@href').extract_first()
            else:
                url = baseurl + i.xpath('dl/dd[1]/a/@href').extract_first()
            print 'add 3th layer url: ' + url
            yield Request(url=url, callback=self.parse_item)

        try:
            url = baseurl + response.xpath(
                '//*[@id="f_mew_list"]/div[6]/div/div[4]/div/div/ul/li[11]/a/@href').extract_first()
            print 'next page url:  ' + url
            yield Request(url=url, callback=self.pase_itemList, dont_filter=True)
        except:
            print u"抓取完成!"

    def parse_item(self, response):
        item = SpiderItem()
        item['category'] = response.xpath('//*[@class="f-crumbs f-w1190"]/a[2]/text()').extract_first().strip()
        item['province'] = \
            response.xpath('/html/head/meta[4]/@content').extract_first().strip().split(';')[0].split('=')[1]
        item['city'] = response.xpath('/html/head/meta[4]/@content').extract_first().strip().split(';')[1].split('=')[1]
        item['username'] = response.xpath('//*[@class="name"]/text()').extract_first().strip()
        if response.xpath('//*[@id="full_phone_show"]/@data-phone').extract_first() == None:
            print 'fuck'
            item['phone'] = 'meiyou phone'
        else:
            item['phone'] = response.xpath('//*[@id="full_phone_show"]/@data-phone').extract_first().replace(' ', '')
        item['paTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['url'] = response.request.url
        print item['username'] + '  ' + item['phone'] + '  ' + item['url']
        yield item
