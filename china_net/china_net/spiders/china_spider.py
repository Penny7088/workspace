# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
import time
from china_net.items import ChinaNetItem


# spider_dianping:start_urls http://www.cbe.com.cn/

class china_spider(RedisSpider):
    name = 'china_spider'
    redis_key = 'china_net:start_urls'
    venues_url = ""
    project_url = ""
    project_page_num = 820
    venues_page_num = 363
    venues_first_half_url = '/venues/list/'
    venues_end_half_url = '-of0-ofa0-ba0-cls0-price0-pr0-ci0-area0-dateinfo0-or0-ot0-a0.html'
    project_first_half_url = '/project/list/'
    project_end_half_url = '-cls0-price0-pr0-ci0-area0-dateinfo0-or0-ot0.html'
    lenth = 7
    page = 0
    url_list = []
    start_urls = ['http://www.cbe.com.cn']

    # lpush china_net:start_urls http://www.cbe.com.cn

    def parse(self, response):
        url_list = response.xpath('//div[@class="ClassContent"]/a/@href').extract()
        for url in url_list:
            child_url = self.start_urls[0] + url
            yield Request(url=child_url, callback=self.parse_child)

    def parse_child(self, response):
        restaurant_url = response.xpath('.//*[@id="HotImg"]/div[1]/div[2]/a[2]/@href').extract_first()
        diversion_url = response.xpath('.//*[@id="HotImg"]/div[1]/div[2]/a[2]/@href').extract_first()
        beauty_url = response.xpath('.//*[@id="HotImg"]/div[1]/a/@href').extract_first()
        hotel_url = response.xpath('.//*[@id="HotImg"]/div[1]/a/@href').extract_first()
        project_url = response.xpath('.//*[@id="HotImg"]/div[1]/a/@href').extract_first()
        shop_url = response.xpath('.//*[@id="Ct-Left"]/div[5]/span[2]/a[1]/@href').extract_first()
        cbd_list = response.xpath('.//*[@id="Ct-Left"]/div[5]/span[2]/a[1]/@href').extract_first()
        ware_house_list = response.xpath('.//*[@id="tb2"]/tbody/tr[1]/td/a/@href').extract_first()
        self.list_not_null(restaurant_url)
        self.list_not_null(diversion_url)
        self.list_not_null(beauty_url)
        self.list_not_null(hotel_url)
        self.list_not_null(project_url)
        self.list_not_null(shop_url)
        self.list_not_null(ware_house_list)
        self.list_not_null(cbd_list)
        print len(self.url_list)
        if self.lenth == len(self.url_list):
            for url in self.url_list:
                child_url = response.urljoin(url)
                if 'venues' in child_url:
                    if self.venues_url == "":
                        self.venues_url = child_url
                        yield Request(url=child_url, callback=self.parse_venues)
                elif 'project' in child_url:
                    if self.project_url == "":
                        self.project_url = child_url
                        yield Request(url=child_url, callback=self.parse_project)

    def parse_venues(self, response):
        for i in range(0, self.venues_page_num):
            join_url = self.venues_first_half_url + "pa" + str(i) + self.venues_end_half_url
            venues_url = response.urljoin(join_url)
            print "ven:" + venues_url
            yield Request(url=venues_url, callback=self.parse_venues_item)

    def parse_venues_item(self, response):
        print '==venues===item===child 子目录===='
        items = response.xpath('.//*[@id="tb2"]/tr/td/a/@href').extract()
        for i in items:
            venues_item = response.urljoin(i)
            try:
                yield Request(url=venues_item, callback=self.parse_venues_detail)
            except:
                continue

    def parse_venues_detail(self, response):
        print '==venues======详细信息============='
        item = ChinaNetItem()
        item["address"] = response.xpath('//*[@id="TitleLeft"]/ul/li[1]/text()').extract_first()
        item["size_of_the_stores"] = response.xpath('//*[@id="TitleLeft"]/ul/li[3]/text()').extract_first()
        item["describe"] = response.xpath('//*[@id="Project"]/p/text()').extract_first()
        item["email"] = response.xpath('//*[@id="Project"]/div[4]/span[4]/text()').extract_first()
        item["phone"] = response.urljoin(response.xpath('//*[@id="Project"]/div[4]/img[1]/@src').extract_first())
        item["phone_img_url"] = response.urljoin(
            response.xpath('//*[@id="Project"]/div[4]/img[2]/@src').extract_first())
        item["name"] = response.xpath('//*[@id="Project"]/div[4]/span[2]/text()').extract_first()
        yield item

    def get_end_page(self, page_list):
        if page_list:
            page_num = re.findall(r'\d+', page_list[-1])[0]
            return int(page_num)

    def list_not_null(self, url):
        if url is not None:
            self.url_list.append(url)
            self.url_list = list(set(self.url_list))

    def parse_project(self, response):
        for i in range(0, self.project_page_num):
            join_url = self.project_first_half_url + "pa" + str(i) + self.project_end_half_url
            project_url = response.urljoin(join_url)
            print "project:" + project_url
            yield Request(url=project_url, callback=self.parse_project_item)

    def parse_project_item(self, response):
        print response.url
        project_item = response.xpath('.//*[@id="tb2"]/tr/td/a/@href').extract()
        print project_item
        for i in project_item:
            venues_item = response.urljoin(i)
            try:
                yield Request(url=venues_item, callback=self.parse_project_detail)
            except:
                continue

    def parse_project_detail(self, response):
        print '==project======详细信息============='
        item = ChinaNetItem()
        item["address"] = response.xpath('//*[@id="TitleLeft"]/ul/li[1]/text()').extract_first()
        item["size_of_the_stores"] = response.xpath('//*[@id="TitleLeft"]/ul/li[3]/text()').extract_first()
        describe = response.xpath('//*[@id="Project"]/p/text()').extract_first()
        item["describe"] = describe
        item["mobile"] = response.xpath('//*[@id="Project"]/div[5]/strong/text()').extract_first()
        item["email"] = response.xpath('//*[@id="Project"]/div[5]/span[4]/text()').extract_first()
        item["phone_img_url"] = response.urljoin(response.xpath('//*[@id="Project"]/div[6]/img/@src').extract_first())
        item["name"] = response.xpath('//*[@id="Project"]/div[5]/span[2]/text()').extract_first()
        print item

    def parse_phone(self, value):
        try:
            phone = re.findall('1\d{10}', value, re.S)[0]
            if phone == '':
                return value
            else:
                return phone
        except:
            pass
