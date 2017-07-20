# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class ChinaNetItem(scrapy.Item):
    # define the fields for your item here like:
    # NAME
    name = scrapy.Field()
    # 地址
    address = scrapy.Field()

    # 店面面积
    size_of_the_stores = scrapy.Field()

    # 描述
    describe = scrapy.Field()

    # 联系电话
    phone = scrapy.Field()

    # 手机
    mobile = scrapy.Field()

    # 邮箱
    email = scrapy.Field()

    # 电话的图片地址
    phone_img_url = scrapy.Field()
