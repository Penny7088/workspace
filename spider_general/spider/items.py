# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

import re


class CustomizeLoad(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


# 手机号码正则提取
def parse_phone(value):
    try:
        phone = re.findall('1\d{10}', value, re.S)[0]
        return phone
    except:
        pass


class myItem(Item):
   
    province = Field()
    # 市
    city = Field()
    # 区
    district = Field()
    # 地址
    url = Field()
    
    bigCate = Field()
    
    smallCate = Field()
    



class SpiderItem(Item):
    # 姓名
    username = Field()
    # 行业
    category = Field()
    # 省份
    province = Field()
    # 市
    city = Field()
    # 区
    district = Field()
    # 地址
    address = Field()
    # 电话
    phone = Field(
        input_processor=MapCompose(parse_phone)
    )
    # 公司
    company = Field()
    # 性别
    sex = Field()
    # 年龄
    age = Field()
    # 职业
    profession = Field()
    # 学历
    education = Field()
    # 车牌号
    carnumber = Field()
    # 车品牌
    cartype = Field()
    # 当前时间
    last_update_time = Field()
    # 状态
    status = Field()
    #狗品种
    variety=Field()
    #QQ
    qq_number=Field()
    #微信
    wx_number=Field()
    #小区
    district=Field()
    #经纪人
    broker=Field()
    #城区
    cityProper=Field()
    #爬取时间
    paTime=Field()
    
    url=Field()
    
    otherInfo=Field()
    
    


